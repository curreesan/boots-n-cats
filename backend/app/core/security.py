from datetime import datetime, timedelta, timezone
from typing import Literal

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Takes a plain-text password and returns a one-way bcrypt hash.
    Called once, during registration, before the password ever touches
    the database — we store this hash, never the original password.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Checks a plain-text password (what the user just typed at login)
    against the stored hash. Returns True if they match.
    You can never reverse a hash back into the original password — this
    works by hashing the input the same way and comparing the results.
    """
    return pwd_context.verify(plain_password, password_hash)


def create_token(user_id: str, token_type: Literal["access", "refresh"]) -> str:
    """
    Builds a signed JWT containing the user's id, a token type, and an
    expiry time. `token_type` controls how long it lasts:
      - "access"  -> short-lived (minutes), used on every request
      - "refresh" -> long-lived (days), used only to mint new access tokens
    Embedding the type in the payload also stops a refresh token from
    being replayed as if it were an access token.
    """
    if token_type == "access":
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    else:
        expires_delta = timedelta(days=settings.refresh_token_expire_days)

    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": user_id, "type": token_type, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict | None:
    """
    Verifies a JWT's signature and expiry, and returns its payload if valid.
    Returns None if the token is expired, tampered with, or malformed —
    callers just check for None rather than needing to catch an exception.
    """
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None