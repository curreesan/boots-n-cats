from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.core.database import get_session
from app.core.rate_limit import rate_limit_login
from app.core.security import hash_password, verify_password, create_token, decode_token
from app.dependencies.auth import get_current_user
from app.models.user import User, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(SQLModel):
    """Request body for POST /auth/login — keeps the password out of the URL/query string."""
    email: str
    password: str


def _set_auth_cookies(response: Response, user_id: str) -> None:
    """
    Shared helper called by both register and login, since both end the
    same way: the user is now logged in, so both cookies get issued.
    Not a route itself (no @router decorator) — just a plain function
    the routes below call so this logic isn't written twice.
    """
    access_token = create_token(user_id, "access")
    refresh_token = create_token(user_id, "refresh")

    # httpOnly: JavaScript can never read this cookie, even from an
    #           injected script — this is the XSS protection we discussed.
    # secure: only sent over https — driven by ENVIRONMENT so it's False
    #         for local http://localhost dev and True once deployed.
    # samesite="lax": sent on normal navigation, blocked on most
    #           cross-site requests — a reasonable default CSRF guard.
    response.set_cookie("access_token", access_token, httponly=True, secure=settings.is_production, samesite="lax")
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=settings.is_production, samesite="lax")


@router.post("/register", response_model=UserRead)
async def register(data: UserCreate, response: Response, session: AsyncSession = Depends(get_session)):
    """
    Creates a new user. Rejects the request if the email's already taken,
    hashes the password before it ever touches the database, then logs
    the new user in immediately by issuing cookies — no separate "please
    log in now" step required right after signing up.
    """
    existing = await session.exec(select(User).where(User.email == data.email))
    if existing.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=data.email, name=data.name, password_hash=hash_password(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    _set_auth_cookies(response, str(user.id))
    return user


@router.post("/login", response_model=UserRead, dependencies=[Depends(rate_limit_login)])
async def login(data: LoginRequest, response: Response, session: AsyncSession = Depends(get_session)):
    """
    Verifies credentials and, if correct, issues fresh cookies. Deliberately
    returns the exact same error for "no account with this email" and
    "wrong password" — revealing which one it was would let an attacker
    check which emails are registered, one guess at a time.
    """
    result = await session.exec(select(User).where(User.email == data.email))
    user = result.first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    _set_auth_cookies(response, str(user.id))
    return user


@router.post("/logout")
async def logout(response: Response):
    """Clears both auth cookies. Nothing to check first — logging out an
    already-logged-out browser is harmless, so no auth dependency here."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}


@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(get_current_user)):
    """
    Returns the currently logged-in user's own profile. Notice this
    function's body is a single line — get_current_user already did all
    the actual work (reading the cookie, verifying the token, loading the
    user); this route just returns what it was handed.
    """
    return user


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    """
    Mints a new access token cookie from a still-valid refresh token,
    without requiring the user to type their password again. This is
    what the frontend calls silently when a request comes back 401'd
    because the short-lived access token expired.

    Reads the refresh token from its httpOnly cookie rather than accepting
    it as a request param — the cookie is httpOnly specifically so
    frontend JS can never read its value to pass back.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = create_token(payload["sub"], "access")
    response.set_cookie("access_token", new_access_token, httponly=True, secure=settings.is_production, samesite="lax")
    return {"detail": "Token refreshed"}