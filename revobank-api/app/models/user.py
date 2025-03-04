from app import db  
from werkzeug.security import generate_password_hash, check_password_hash  

class User(db.Model):  
    __tablename__ = "users"  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(255), unique=True, nullable=False)  
    email = db.Column(db.String(255), unique=True, nullable=False)  
    password_hash = db.Column(db.String(255), nullable=False)  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  

    # Password handling  
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  

    def check_password(self, password):  
        return check_password_hash(self.password_hash, password)  