"""first migration

Revision ID: 8d9c0a2b78b3
Revises: 
Create Date: 2026-01-11 16:54:32.670700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d9c0a2b78b3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('description', sa.String(), nullable=False)
    )

    op.create_table(
        'claims',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true())
    )

    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('updated_at', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'])
    )

    op.create_table(
        'user_claims',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('claim_id', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'claim_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['claim_id'], ['claims.id'], ondelete='CASCADE')
    )


def downgrade():
    op.drop_table('user_claims')
    op.drop_table('users')
    op.drop_table('claims')
    op.drop_table('roles')