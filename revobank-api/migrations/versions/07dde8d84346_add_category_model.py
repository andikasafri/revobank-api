"""add category model

Revision ID: 07dde8d84346
Revises: ac008f075d44
Create Date: 2025-03-27 02:22:18.992695

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '07dde8d84346'
down_revision = 'ac008f075d44'
branch_labels = None
depends_on = None

def upgrade():
    # Create only the new transaction_categories table
    op.create_table(
        'transaction_categories',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Add category_id to existing transactions table
    op.add_column('transactions',
        sa.Column('category_id', sa.INTEGER(), nullable=True)
    )
    
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_transactions_category',
        'transactions', 'transaction_categories',
        ['category_id'], ['id'],
        ondelete='SET NULL'
    )

def downgrade():
    # Remove foreign key first
    op.drop_constraint('fk_transactions_category', 'transactions', type_='foreignkey')
    
    # Remove category_id column
    op.drop_column('transactions', 'category_id')
    
    # Drop the categories table
    op.drop_table('transaction_categories')
