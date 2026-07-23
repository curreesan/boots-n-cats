import time
from collections import defaultdict

from fastapi import HTTPException, Request

WINDOW_SECONDS = 300  # 5 minutes
MAX_ATTEMPTS = 5

_attempts: dict[str, list[float]] = defaultdict(list)


def rate_limit_login(request: Request) -> None:
    """
    Simple in-memory fixed-window rate limiter keyed by client IP — caps
    login attempts to MAX_ATTEMPTS per WINDOW_SECONDS, closing the
    brute-force gap on /auth/login. In-memory only: resets on server
    restart and doesn't share state across multiple worker processes —
    fine for this app's single-process deployment, but would need a
    shared store like Redis to scale to multiple workers/instances.
    """
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    attempts = _attempts[client_ip]
    attempts[:] = [t for t in attempts if now - t < WINDOW_SECONDS]

    if len(attempts) >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Try again in a few minutes.",
        )

    attempts.append(now)
