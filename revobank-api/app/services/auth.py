# JWT helper functions
from datetime import timedelta
from flask_jwt_extended import create_access_token

def generate_token(user_id):
    return create_access_token(identity=str(user_id),expires_delta=timedelta(hours=3))