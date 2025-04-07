import os
import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

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
        ssl_mode = os.getenv('DB_SSL_MODE', 'require')
        connection_str = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
            f"?sslmode={ssl_mode}"
        )
        app.config['SQLALCHEMY_DATABASE_URI'] = connection_str
        app.logger.info(f"Connecting to database at {os.getenv('DB_HOST')} with SSL mode: {ssl_mode}")

    # Global error handlers
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        return jsonify({
            'description': e.description,
            'code': e.code
        }), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.exception(e)
        return jsonify({
            'description': 'An internal error occurred.',
            'code': 500
        }), 500

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Import models in proper order
    from app.models.user import User
    from app.models.account import Account
    from app.models.transaction_category import TransactionCategory
    from app.models.transaction import Transaction
    from app.models.budget import Budget
    from app.models.bill import Bill

    # Initialize migrations after models are imported
    migrate.init_app(app, db)

    # Register blueprints (existing and new endpoints)
    from app.routes.auth import auth_bp
    from app.routes.accounts import accounts_bp
    from app.routes.transactions import transactions_bp
    from app.routes.budgets import budgets_bp      # New: Budget Management endpoints
    from app.routes.bills import bills_bp          # New: Bill Payment Management endpoints
    from app.routes.transaction_categories import transaction_categories_bp  # New: Transaction Categories endpoints

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(accounts_bp, url_prefix='/api/accounts')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(budgets_bp, url_prefix='/api/budgets')
    app.register_blueprint(bills_bp, url_prefix='/api/bills')
    app.register_blueprint(transaction_categories_bp, url_prefix='/api/transactions/categories')

    # Add middleware (example: logging each request)
    @app.before_request
    def before_request_middleware():
        app.logger.info(f"Incoming request: {request.method} {request.path}")

    # Root route
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Revobank API!"})

    # Health check endpoint
    @app.route('/health')
    def health_check():
        try:
            db.session.execute('SELECT 1')
            return jsonify({"status": "healthy"}), 200
        except Exception as e:
            return jsonify({"status": "unhealthy"}), 500

    return app

# Expose the app for Gunicorn
app = create_app()

# Use Gunicorn's logger if not running as __main__
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
