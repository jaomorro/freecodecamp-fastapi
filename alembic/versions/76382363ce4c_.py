"""empty message

Revision ID: 76382363ce4c
Revises: cf75466b6455
Create Date: 2023-01-09 07:39:28.951593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76382363ce4c'
down_revision = 'cf75466b6455'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('val', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_table')
    # ### end Alembic commands ###
