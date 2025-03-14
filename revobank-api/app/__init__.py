# import os
# import logging
# from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate
# from dotenv import load_dotenv
# from werkzeug.exceptions import HTTPException

# db = SQLAlchemy()
# jwt = JWTManager()
# migrate = Migrate()

# def create_app(config_name=None):
#     app = Flask(__name__)
#     load_dotenv()

#     # Base configuration
#     app.config.update(
#         SQLALCHEMY_TRACK_MODIFICATIONS=False,
#         JWT_ALGORITHM="HS256",
#         JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
#     )

#     # Database configuration
#     if config_name == 'testing':
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         app.config['TESTING'] = True
#     else:
#         app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
#             'DATABASE_URL',
#             f"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
#             f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
#         )

#     @app.errorhandler(HTTPException)
#     def handle_exception(e):
#         return jsonify({
#             'description': e.description,
#             'code': e.code
#         }), e.code

#     @app.errorhandler(Exception)
#     def handle_generic_exception(e):
#         app.logger.error(f"An error occurred: {str(e)}")
#         return jsonify({
#             'description': 'An internal error occurred.',
#             'code': 500
#         }), 500

#     # Initialize extensions
#     db.init_app(app)
#     jwt.init_app(app)
#     migrate.init_app(app, db)

#     # Import models for Flask-Migrate
#     from app.models.user import User
#     from app.models.account import Account
#     from app.models.transaction import Transaction

#     # Register blueprints
#     from app.routes.auth import auth_bp
#     from app.routes.accounts import accounts_bp
#     from app.routes.transactions import transactions_bp
    
#     app.register_blueprint(auth_bp, url_prefix='/api/auth')
#     app.register_blueprint(accounts_bp, url_prefix='/api/accounts')
#     app.register_blueprint(transactions_bp)

#     # Add a root route
#     @app.route('/')
#     def home():
#         return jsonify({"message": "Welcome to Revobank API!"})

#     return app

# # Expose the app for Gunicorn
# app = create_app()

# # Configure logging
# if __name__ != '__main__':
#     gunicorn_logger = logging.getLogger('gunicorn.error')
#     app.logger.handlers = gunicorn_logger.handlers
#     app.logger.setLevel(gunicorn_logger.level)

import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    load_dotenv()  # Load variables from .env if available

    # Base configuration
    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_ALGORITHM="HS256",
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
    )

    # Database configuration
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        # Get individual DB parameters from the environment
        db_user = os.getenv('DB_USER', 'default_user')
        db_password = os.getenv('DB_PASSWORD', 'default_password')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_name = os.getenv('DB_NAME', 'default_db')

        # Build the connection string
        connection_str = f"mysql+mysqldb://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4"
        # Allow DATABASE_URL to override, if provided.
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', connection_str)

        # Log the final DB URI (without exposing sensitive info)
        app.logger.info("Connecting to database at host: " + db_host + " using database: " + db_name)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({
            'description': e.description,
            'code': e.code
        }), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({
            'description': 'An internal error occurred.',
            'code': 500
        }), 500

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import models for Flask-Migrate
    from app.models.user import User
    from app.models.account import Account
    from app.models.transaction import Transaction

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.accounts import accounts_bp
    from app.routes.transactions import transactions_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(accounts_bp, url_prefix='/api/accounts')
    app.register_blueprint(transactions_bp)

    # Add a root route
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Revobank API!"})

    return app

# Expose the app for Gunicorn
app = create_app()

# Configure logging to use Gunicorn's logger if not running as __main__
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
