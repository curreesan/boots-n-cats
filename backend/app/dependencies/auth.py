import uuid

from fastapi import Request, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.security import decode_token
from app.models.user import User


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Reads the access_token cookie off the incoming request, verifies it,
    and loads the matching user from the database.

    Any route that declares `user: User = Depends(get_current_user)` gets
    this run automatically BEFORE the route's own code executes — if it
    raises an HTTPException, the route body never runs at all.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await session.get(User, uuid.UUID(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


async def require_staff(user: User = Depends(get_current_user)) -> User:
    """
    Builds on top of get_current_user — first confirms the user is logged
    in at all, then checks their role. Attach this (not get_current_user)
    to any /admin/* route.
    """
    if user.role != "staff":
        raise HTTPException(status_code=403, detail="Staff access required")
    return user