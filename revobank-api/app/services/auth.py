# JWT helper functions

from flask_jwt_extended import create_access_token

def generate_token(user_id):
    return create_access_token(identity=user_id)