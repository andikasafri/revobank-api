from app import db
from datetime import datetime

class Bill(db.Model):
    __tablename__ = 'bills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    biller_name = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    user = db.relationship('User', backref=db.backref('bills', lazy=True))
    account = db.relationship('Account', backref=db.backref('bills', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_id': self.account_id,
            'biller_name': self.biller_name,
            'due_date': self.due_date.isoformat(),
            'amount': str(self.amount),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
