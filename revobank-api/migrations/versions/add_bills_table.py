"""add bills table

Revision ID: add_bills_table
Revises: initial_setup
Create Date: 2025-03-27 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_bills_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'bills',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('account_id', sa.INTEGER(), nullable=False),
        sa.Column('biller_name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('due_date', sa.DATE(), nullable=False),
        sa.Column('amount', sa.NUMERIC(precision=10, scale=2), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('bills')
