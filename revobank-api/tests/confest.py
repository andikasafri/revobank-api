import pytest
from app import create_app, db
from app.models.user import User
from app.models.account import Account

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'mysql+mysqldb://testuser:testpass@localhost/revobank_test',
        'JWT_SECRET_KEY': 'test_secret_key'
    })
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture(scope='module')
def init_database(test_app):
    with test_app.app_context():
        db.create_all()
        
        # Create test user
        user = User(
            username='testuser',
            email='test@revobank.com',
        )
        user.set_password('TestPass123!')
        db.session.add(user)
        
        # Create test account
        account = Account(
            user_id=1,
            account_type='checking',
            account_number='ACC-123456',
            balance=1000.00
        )
        db.session.add(account)
        
        db.session.commit()
        yield db
        db.drop_all()

@pytest.fixture(scope='module')
def auth_tokens(test_client):
    # Get JWT token
    response = test_client.post('/api/auth/login', json={
        'email': 'test@revobank.com',
        'password': 'TestPass123!'
    })
    return {
        'access_token': response.json['access_token']
    }