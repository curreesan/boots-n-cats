import sys
from pathlib import Path
from logging.config import fileConfig

from sqlmodel import SQLModel
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Make `app` importable when alembic is run from the project root.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.config import settings

# Import every model module so its table registers on SQLModel.metadata —
# alembic can only "see" a table if it's been imported somewhere by the
# time this file runs. If you add a new model file later, add it here too.
from app.models import user, product, pet, order, consultation  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# autogenerate compares the live DB against this metadata to build migrations
target_metadata = SQLModel.metadata

# Alembic's migration runner is sync, but our app uses the async asyncpg
# driver everywhere else. Rather than making migrations async too, we
# swap in the plain sync driver here — same DB, same URL, different driver.
sync_url = settings.database_url.replace("+asyncpg", "")
config.set_main_option("sqlalchemy.url", sync_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode — generates SQL without a live DB connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode — connects to the real DB and runs directly."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()