# filepath: migrations/versions/6394f7fd54e9_initial_migration.py
"""Initial migration"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql  

# Revision identifiers, used by Alembic.
revision = '6394f7fd54e9'
down_revision = None  # Update this if there is a previous revision
branch_labels = None
depends_on = None

def upgrade():
    # Add your schema changes here
    op.create_table(
        'users',
        sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('password_hash', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name='users_pkey'),
        sa.UniqueConstraint('email', name='users_email_key'),
        sa.UniqueConstraint('username', name='users_username_key'),
        postgresql_ignore_search_path=False
    )
    op.create_table(
        'accounts',
        sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('accounts_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('account_type', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('balance', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.Column('account_number', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
        sa.CheckConstraint("account_number::text ~~ 'ACC-%%%%%%%%'::text", name='account_number_format'),
        sa.CheckConstraint('balance >= 0.0', name='non_negative_balance'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='accounts_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='accounts_pkey'),
        sa.UniqueConstraint('account_number', name='accounts_account_number_key'),
        postgresql_ignore_search_path=False
    )
    op.create_table(
        'transactions',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('type', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column('amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False),
        sa.Column('from_account_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('to_account_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.CheckConstraint('amount > 0::numeric', name='positive_amount'),
        sa.ForeignKeyConstraint(['from_account_id'], ['accounts.id'], name='transactions_from_account_id_fkey', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['to_account_id'], ['accounts.id'], name='transactions_to_account_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='transactions_pkey')
    )
    op.create_table(
        'budgets',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('amount', sa.NUMERIC(precision=10, scale=2), nullable=False),
        sa.Column('start_date', sa.DATE(), nullable=False),
        sa.Column('end_date', sa.DATE(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    )


def downgrade():
    # Add proper downgrade implementation
    op.drop_table('transactions')
    op.drop_table('accounts')
    op.drop_table('users')