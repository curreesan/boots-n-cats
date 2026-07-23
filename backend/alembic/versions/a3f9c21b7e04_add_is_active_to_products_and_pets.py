"""add is_active to products and pets

Revision ID: a3f9c21b7e04
Revises: eb569465b7d2
Create Date: 2026-07-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a3f9c21b7e04'
down_revision: Union[str, Sequence[str], None] = 'eb569465b7d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # server_default='true' so existing rows backfill as active without a
    # separate UPDATE — Postgres applies it to every existing row as part
    # of adding the NOT NULL column.
    op.add_column('products', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('pets', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('pets', 'is_active')
    op.drop_column('products', 'is_active')
