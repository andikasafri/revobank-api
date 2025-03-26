"""Add Budget model

Revision ID: ac008f075d44
Revises: 6394f7fd54e9
Create Date: 2025-03-27 01:56:19.139337

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ac008f075d44'
down_revision = '6394f7fd54e9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'budgets',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('amount', sa.NUMERIC(10, 2), nullable=False),
        sa.Column('start_date', sa.DATE(), nullable=False),
        sa.Column('end_date', sa.DATE(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='budgets_pkey')
    )


def downgrade():
    op.drop_table('budgets')
