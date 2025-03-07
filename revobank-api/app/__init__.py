import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    load_dotenv()  # Load environment variables
    
     # Debug: Print to check if the key is loaded
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret:
        raise ValueError("JWT_SECRET_KEY is not loading. Check your .env file!")
    
    print(f"✅ Loaded JWT_SECRET_KEY: {jwt_secret}")

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config['JWT_SECRET_KEY'] = jwt_secret
    # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import models for flask migrate to detect them
    from app.models.user import User
    from app.models.account import Account
    from app.models.transaction import Transaction

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.accounts import accounts_bp
    from app.routes.transactions import transactions_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(accounts_bp, url_prefix='/api/accounts')
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(accounts_bp)
    app.register_blueprint(transactions_bp)

    return app