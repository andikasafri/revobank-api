from app import db
from sqlalchemy import CheckConstraint, ForeignKey
from datetime import datetime, timezone
from app.models.account import Account

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, transfer
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    from_account_id = db.Column(db.Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=True)
    to_account_id = db.Column(db.Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    from_account = db.relationship('Account', foreign_keys=[from_account_id])
    to_account = db.relationship('Account', foreign_keys=[to_account_id])

    __table_args__ = (
        CheckConstraint('amount > 0', name='positive_amount'),
    )

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'amount': str(self.amount),  # Preserve decimal precision
            'from_account_id': self.from_account_id,
            'to_account_id': self.to_account_id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }