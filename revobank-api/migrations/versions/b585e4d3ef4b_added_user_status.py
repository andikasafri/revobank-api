"""Add status column to accounts

Revision ID: b585e4d3ef4b
Revises: e9a57901ca7d
Create Date: 2025-04-07 16:20:30.252798

"""
from alembic import op
import sqlalchemy as sa

revision = 'b585e4d3ef4b'
down_revision = 'e9a57901ca7d'

def upgrade():
    # Add status column to accounts table
    op.add_column('accounts',
        sa.Column('status',
            sa.String(20),
            nullable=False,
            server_default=sa.text("'active'::character varying")
        )
    )

    # Add check constraint for valid status values
    op.create_check_constraint(
        'valid_status',
        'accounts',
        sa.text("status IN ('active', 'deactivated')")
    )

def downgrade():
    # Drop check constraint
    op.drop_constraint('valid_status', 'accounts')
    
    # Drop status column
    op.drop_column('accounts', 'status')