from app import db
from sqlalchemy import CheckConstraint

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    __table_args__ = (
        CheckConstraint(balance >= 0.00, name='non_negative_balance'),
    )
    
    def serialize(self):
        return {
            'id': self.id,
            # 'user_id': self.user_id,
            'account_type': self.account_type,
            'account_number': self.account_number,
            'balance': float(self.balance),
            'created_at': self.created_at,
            # 'updated_at': self.updated_at
        }
        