from sqlalchemy import create_engine
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlmodel import SQLModel

from app.core.config import settings
from app.models import user, product, pet, cart, order, consultation  # noqa: F401

url = settings.database_url.replace("+asyncpg", "")
engine = create_engine(url)

with engine.connect() as conn:
    context = MigrationContext.configure(conn)
    diff = compare_metadata(context, SQLModel.metadata)
    print(f"Number of differences found: {len(diff)}")
    for item in diff:
        print(item)