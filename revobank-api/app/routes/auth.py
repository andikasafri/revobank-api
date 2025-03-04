# User Management
# from flask import Blueprint, request, jsonify  
# from app.models.user import User  
# from app import db  
# from werkzeug.exceptions import BadRequest  

# auth_bp = Blueprint('auth', __name__)  

# @auth_bp.route('/users', methods=['POST'])  
# def create_user():  
#     data = request.get_json()  
#     required_fields = ['username', 'email', 'password']  
#     if not all(field in data for field in required_fields):  
#         raise BadRequest("Missing required fields")  

#     # Check for existing user  
#     if User.query.filter_by(username=data['username']).first():  
#         return jsonify({"error": "Username already exists"}), 409  
#     if User.query.filter_by(email=data['email']).first():  
#         return jsonify({"error": "Email already exists"}), 409  

#     # Create user  
#     new_user = User(  
#         username=data['username'],  
#         email=data['email']  
#     )  
#     new_user.set_password(data['password'])  
#     db.session.add(new_user)  
#     db.session.commit()  

#     return jsonify({"message": "User created successfully"}), 201  

# User Management
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db
from werkzeug.exceptions import BadRequest, Unauthorized

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# Register a new user
@auth_bp.route('/users', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'email', 'password']  
    if not all(field in data for field in required_fields):  
        raise BadRequest("Missing required fields")  
    
# Check for existing user

@auth_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat(),
        # 'updated_at': user.updated_at.isoformat()
    }), 200
    
# Update the current user
@auth_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    data = request.get_json()
    
    if 'email' in data:
        if user.query.filter(User.email == data['email'], user.id != current_user_id).first():
            return jsonify({"error": "Email already in use"}), 409
        user.email = data['email']
    
    if 'password' in data:
        user.set_password(data['password'])
        
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200