"""add default to users.created_at

Revision ID: 9bdc397cb883
Revises: 8d9c0a2b78b3
Create Date: 2026-01-11 17:14:37.432247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bdc397cb883'
down_revision: Union[str, None] = '8d9c0a2b78b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "created_at",
        server_default=sa.text("CURRENT_DATE"),
        existing_type=sa.Date(),
        nullable=False
    )

def downgrade():
    op.alter_column(
        "users",
        "created_at",
        server_default=None,
        existing_type=sa.Date(),
        nullable=False
    )
