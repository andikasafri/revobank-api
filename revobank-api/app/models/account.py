from app import db
from sqlalchemy import CheckConstraint
from datetime import datetime

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')

    __table_args__ = (
        CheckConstraint(balance >= 0.00, name='non_negative_balance'),
        CheckConstraint("account_number LIKE 'ACC-%%'", name='account_number_format'),
        CheckConstraint("status IN ('active', 'deactivated')", name='valid_status')
    )
    
    def deactivate(self):
        """Deactivate account if balance is zero"""
        if self.balance != 0:
            raise ValueError("Cannot deactivate account with non-zero balance")
        self.status = 'deactivated'
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_type': self.account_type,
            'account_number': self.account_number,
            'balance': str(self.balance),  
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status,
        }
