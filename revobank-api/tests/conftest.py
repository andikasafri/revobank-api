import pytest
from app import create_app, db
from app.models.user import User
from app.models.account import Account
from sqlalchemy import event

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for tests."""
    app = create_app('testing')  # Pass 'testing' to use SQLite
    with app.app_context():
        # Set up SQLite foreign key support if using SQLite
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            @event.listens_for(db.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        yield app

@pytest.fixture(scope='function')
def test_client(app):
    """Create a test client for making HTTP requests."""
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Create test user
        user = User(
            username='testuser',
            email='test@revobank.com',
        )
        user.set_password('TestPass123!')
        db.session.add(user)
        db.session.commit()
        
        # Create test account
        account = Account(
            user_id=user.id,
            account_type='savings',
            account_number='ACC-123456',
            balance=1000.00
        )
        db.session.add(account)
        db.session.commit()
        
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def auth_tokens(test_client, init_database):
    """Get JWT tokens for authenticated requests."""
    response = test_client.post('/api/auth/login', json={
        'email': 'test@revobank.com',
        'password': 'TestPass123!'
    })
    return {
        'access_token': response.json['access_token']
    }