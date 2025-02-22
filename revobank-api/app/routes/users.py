from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app import db, bcrypt
from app.models import User

users_ns = Namespace('users', description='User operations')

# Request/Response schema for Swagger docs
user_model = users_ns.model('User', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

@users_ns.route('')
class UserList(Resource):
    @users_ns.expect(user_model)
    def post(self):
        """Create a new user"""
        data = users_ns.payload

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email already registered"}, 400

        # Hash password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Create user
        new_user = User(
            email=data['email'],
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

@users_ns.route('/me')
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        """Get current user profile"""
        # You'll implement this later after authentication
        return {"message": "User profile endpoint"}, 200