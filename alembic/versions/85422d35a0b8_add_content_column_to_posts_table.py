"""add content column to posts table

Revision ID: 85422d35a0b8
Revises: a97de15f2007
Create Date: 2022-12-27 05:40:54.319401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85422d35a0b8'
down_revision = 'a97de15f2007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
