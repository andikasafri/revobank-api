from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_restx import Api
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
api = Api()  # Initialize Flask-RESTx

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    # Configure app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)  # Attach Flask-RESTx to the app

    # Import models (for table creation)
    from app.models import User, Account, Transaction

    # Import and register namespaces (API routes)
    from app.routes.users import users_ns
    api.add_namespace(users_ns)

    return app