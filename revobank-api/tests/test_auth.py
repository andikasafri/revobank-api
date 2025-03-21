import pytest
from app import create_app, db
from app.models.user import User
from app.models.account import Account

def test_register_user(test_client, init_database):
    response = test_client.post('/api/auth/users', json={
        'username': 'newuser',
        'email': 'new@revobank.com',
        'password': 'NewPass123!'
    })
    assert response.status_code == 201
    assert 'message' in response.json

def test_register_duplicate_email(test_client, init_database):
    response = test_client.post('/api/auth/users', json={
        'username': 'anotheruser',
        'email': 'test@revobank.com',
        'password': 'TestPass123!'
    })
    assert response.status_code == 409
    assert 'error' in response.json

def test_login_valid(test_client, init_database):
    response = test_client.post('/api/auth/login', json={
        'email': 'test@revobank.com',
        'password': 'TestPass123!'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid(test_client, init_database):
    response = test_client.post('/api/auth/login', json={
        'email': 'wrong@revobank.com',
        'password': 'WrongPass123!'
    })
    assert response.status_code == 401

def test_delete_user(test_client, init_database):
    # Register a new user
    register_response = test_client.post('/api/auth/users', json={
        'username': 'deleteuser',
        'email': 'delete@revobank.com',
        'password': 'DeletePass123!'
    })
    assert register_response.status_code == 201, "User registration failed"

    # Log in to get access token
    login_response = test_client.post('/api/auth/login', json={
        'email': 'delete@revobank.com',
        'password': 'DeletePass123!'
    })
    assert login_response.status_code == 200, "User login failed"
    access_token = login_response.json['access_token']

    # Delete the user
    headers = {'Authorization': f'Bearer {access_token}'}
    delete_response = test_client.delete('/api/auth/users/me', headers=headers)
    assert delete_response.status_code == 204, "User deletion failed"


# Test registration with missing fields (covers line 24 and triggers line 12)
def test_register_missing_fields(test_client, init_database):
    response = test_client.post('/api/auth/users', json={
        'username': 'missing',
        'email': 'missing@revobank.com'  # No password
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Missing required fields' in response.json['error']

# Test registration with duplicate username (covers line 29)
def test_register_duplicate_username(test_client, init_database):
    # First registration
    test_client.post('/api/auth/users', json={
        'username': 'duplicate',
        'email': 'dup1@revobank.com',
        'password': 'Duplicate123!'
    })
    # Second registration with same username
    response = test_client.post('/api/auth/users', json={
        'username': 'duplicate',
        'email': 'dup2@revobank.com',
        'password': 'Duplicate123!'
    })
    assert response.status_code == 409
    assert 'error' in response.json
    assert 'Username already exists' in response.json['error']

# Test registration with invalid passwords (covers lines 35-36 in auth.py and 16, 18, 20 in user.py)
def test_register_invalid_password(test_client, init_database):
    # Password too short
    response = test_client.post('/api/auth/users', json={
        'username': 'shortpass',
        'email': 'short@revobank.com',
        'password': 'Short1!'  # Less than 8 characters
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'at least 8 characters' in response.json['error']

    # No uppercase letter
    response = test_client.post('/api/auth/users', json={
        'username': 'noupper',
        'email': 'noupper@revobank.com',
        'password': 'noupper1!'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'one uppercase letter' in response.json['error']

    # No special character
    response = test_client.post('/api/auth/users', json={
        'username': 'nospecial',
        'email': 'nospecial@revobank.com',
        'password': 'NoSpecial123'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'one special character' in response.json['error']

# Test getting current user (covers lines 45-47)
def test_get_current_user(test_client, init_database):
    # Register and login
    test_client.post('/api/auth/users', json={
        'username': 'getuser',
        'email': 'get@revobank.com',
        'password': 'GetPass123!'
    })
    login_response = test_client.post('/api/auth/login', json={
        'email': 'get@revobank.com',
        'password': 'GetPass123!'
    })
    access_token = login_response.json['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    # Get user details
    response = test_client.get('/api/auth/users/me', headers=headers)
    assert response.status_code == 200
    assert response.json['username'] == 'getuser'
    assert response.json['email'] == 'get@revobank.com'

# Test updating user email successfully (covers part of lines 57-73)
def test_update_user_email(test_client, init_database):
    # Register and login
    test_client.post('/api/auth/users', json={
        'username': 'updateuser',
        'email': 'update@revobank.com',
        'password': 'Update123!'
    })
    login_response = test_client.post('/api/auth/login', json={
        'email': 'update@revobank.com',
        'password': 'Update123!'
    })
    access_token = login_response.json['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    # Update email
    response = test_client.put('/api/auth/users/me', headers=headers, json={
        'email': 'newemail@revobank.com'
    })
    assert response.status_code == 200
    assert 'message' in response.json
    assert 'User updated successfully' in response.json['message']

# Test updating user email to an existing one (covers email conflict in lines 57-73)
def test_update_user_email_conflict(test_client, init_database):
    # Register two users
    test_client.post('/api/auth/users', json={
        'username': 'user1',
        'email': 'user1@revobank.com',
        'password': 'User1Pass123!'
    })
    test_client.post('/api/auth/users', json={
        'username': 'user2',
        'email': 'user2@revobank.com',
        'password': 'User2Pass123!'
    })
    # Login as user1
    login_response = test_client.post('/api/auth/login', json={
        'email': 'user1@revobank.com',
        'password': 'User1Pass123!'
    })
    access_token = login_response.json['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    # Try to update to user2's email
    response = test_client.put('/api/auth/users/me', headers=headers, json={
        'email': 'user2@revobank.com'
    })
    assert response.status_code == 409
    assert 'error' in response.json
    assert 'Email already in use' in response.json['error']

# Test updating user with invalid password (covers password validation in lines 57-73)
def test_update_user_invalid_password(test_client, init_database):
    # Register and login
    test_client.post('/api/auth/users', json={
        'username': 'updatepass',
        'email': 'updatepass@revobank.com',
        'password': 'UpdatePass123!'
    })
    login_response = test_client.post('/api/auth/login', json={
        'email': 'updatepass@revobank.com',
        'password': 'UpdatePass123!'
    })
    access_token = login_response.json['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    # Update with invalid password
    response = test_client.put('/api/auth/users/me', headers=headers, json={
        'password': 'short'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'at least 8 characters' in response.json['error']

# Test login with missing fields (covers line 80)
def test_login_missing_fields(test_client, init_database):
    response = test_client.post('/api/auth/login', json={
        'email': 'test@revobank.com'  # No password
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Email and password required' in response.json['error']

# Test deleting user with active accounts (covers line 100)
def test_delete_user_with_accounts(test_client, init_database):
    # Register and login
    test_client.post('/api/auth/users', json={
        'username': 'userwithacc',
        'email': 'userwithacc@revobank.com',
        'password': 'UserAcc123!'
    })
    login_response = test_client.post('/api/auth/login', json={
        'email': 'userwithacc@revobank.com',
        'password': 'UserAcc123!'
    })
    access_token = login_response.json['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    # Add an account manually (since accounts_bp isn’t fully tested)
    with test_client.application.app_context():
        user = User.query.filter_by(email='userwithacc@revobank.com').first()
        account = Account(user_id=user.id, account_type='savings', account_number='ACC-1001', balance=0)
        db.session.add(account)
        db.session.commit()
    # Attempt to delete
    response = test_client.delete('/api/auth/users/me', headers=headers)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Cannot delete user with active accounts' in response.json['error']