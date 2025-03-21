from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.services.auth import generate_token
from app.models.account import Account
from app import db
from werkzeug.exceptions import BadRequest, NotFound

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e.description)), 400

@auth_bp.errorhandler(404)
def handle_not_found(e):
    return jsonify(error="Resource not found"), 404

@auth_bp.route('/users', methods=['POST'])
def register():
    try:
        current_app.logger.info("Attempting to register new user")
        data = request.get_json()
        current_app.logger.debug(f"Received registration data: {data}")
        
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        # Validate email format
        if '@' not in data['email']:
            raise BadRequest("Invalid email format")

        # Check existing user with better error messages
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists", "field": "username"}), 409
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists", "field": "email"}), 409

        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        
        current_app.logger.info(f"Creating new user with username: {data['username']}")
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"Successfully created user in database. User ID: {new_user.id}")
        
        response_data = {
            "message": "User created successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "created_at": new_user.created_at.isoformat()
            }
        }
        current_app.logger.info(f"Sending response: {response_data}")
        return jsonify(response_data), 201

    except ValueError as e:
        # Password validation errors
        return jsonify({"error": str(e), "field": "password"}), 400
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Failed to create user"}), 500

@auth_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if user is None:
        raise NotFound("User not found")
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat(),
    }), 200

@auth_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if user is None:
        raise NotFound("User not found")
    data = request.get_json()

    if 'email' in data:
        if User.query.filter(User.email == data['email'], User.id != current_user_id).first():
            return jsonify({"error": "Email already in use"}), 409
        user.email = data['email']
    
    if 'password' in data:
        try:
            user.set_password(data['password'])
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        raise BadRequest("Email and password required")
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = generate_token(user.id)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/users/me', methods=['DELETE'])
@jwt_required()
def delete_current_user():
    """Delete authenticated user's account if no active accounts exist"""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if user is None:
        raise NotFound("User not found")
    
    if db.session.query(Account).filter_by(user_id=current_user_id).first():
        raise BadRequest("Cannot delete user with active accounts")
    
    db.session.delete(user)
    db.session.commit()
    return "", 204