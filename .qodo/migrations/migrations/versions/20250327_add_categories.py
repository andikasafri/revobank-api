"""add transaction categories

Revision ID: 20250327_add_categories
Revises: 
Create Date: 2025-03-27 03:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250327_add_categories'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create transaction_categories table
    op.create_table(
        'transaction_categories',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Add category_id to existing transactions table if it doesn't exist
    try:
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
    except Exception as e:
        print(f"Column may already exist: {e}")

def downgrade():
    try:
        # Remove foreign key first
        op.drop_constraint('fk_transactions_category', 'transactions', type_='foreignkey')
        # Remove category_id column
        op.drop_column('transactions', 'category_id')
    except Exception as e:
        print(f"Constraint or column may not exist: {e}")
    
    # Drop the categories table
    op.drop_table('transaction_categories')
