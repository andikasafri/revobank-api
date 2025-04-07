from flask import Blueprint, request, jsonify
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
    data = request.get_json()
    required_fields = ['username', 'email', 'password']
    
    if not all(field in data for field in required_fields):
        raise BadRequest("Missing required fields")

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409

    new_user = User(username=data['username'], email=data['email'])
    
    try:
        new_user.set_password(data['password'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
        
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

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
    """Delete authenticated user's account if all accounts are deactivated"""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if user is None:
        raise NotFound("User not found")
    
    # Check for active accounts
    active_accounts = Account.query.filter_by(
        user_id=current_user_id,
        status='active'
    ).first()
    
    if active_accounts:
        raise BadRequest("Cannot delete user with active accounts. Please deactivate all accounts first.")
    
    db.session.delete(user)
    db.session.commit()
    return "", 204