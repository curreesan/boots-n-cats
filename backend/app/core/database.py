from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from app.core.config import settings

# One engine for the whole app's lifetime — manages the actual connection
# pool to Postgres. Not a function, so no docstring, but this line only
# ever runs once, when this file is first imported.
engine = create_async_engine(settings.database_url, echo=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that hands a route a fresh DB session, borrowed from
    the shared engine's connection pool, and guarantees it's closed
    afterwards — even if the route raises an exception partway through.

    This is a generator (uses `yield`, not `return`): FastAPI calls this,
    receives the session at the `yield` point, lets the route run, then
    resumes this function afterward so the `async with` block can close
    the session as cleanup.

    Usage in a route: `session: AsyncSession = Depends(get_session)`
    """
    async with AsyncSession(engine) as session:
        yield session


async def init_db():
    """
    Dev convenience only, not used once Alembic migrations are set up.
    Looks at every SQLModel class with `table=True` and creates matching
    tables directly in Postgres — no migration history, no version
    tracking. Useful for quickly spinning up a throwaway local DB to test
    something, but Alembic (coming up soon) is the real way we'll manage
    schema changes going forward.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)