"""Initial upgrade with proper models

Revision ID: e9a57901ca7d
Revises: 
Create Date: 2025-04-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e9a57901ca7d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=255), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'))
    )

    op.create_table('accounts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('account_type', sa.String(length=255), nullable=False),
        sa.Column('balance', sa.Numeric(10, 2), nullable=False),
        sa.Column('account_number', sa.String(length=20), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.CheckConstraint("account_number LIKE 'ACC-%'", name='account_number_format'),
        sa.CheckConstraint('balance >= 0.0', name='non_negative_balance')
    )

    op.create_table('transaction_categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'))
    )

    op.create_table('transactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('from_account_id', sa.Integer(), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=True),
        sa.Column('to_account_id', sa.Integer(), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('transaction_categories.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.CheckConstraint('amount > 0.0', name='positive_amount')
    )

    op.create_table('budgets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'))
    )

    op.create_table('bills',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('biller_name', sa.String(length=255), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'))
    )

def downgrade():
    op.drop_table('bills')
    op.drop_table('budgets')
    op.drop_table('transactions')
    op.drop_table('transaction_categories')
    op.drop_table('accounts')
    op.drop_table('users')
