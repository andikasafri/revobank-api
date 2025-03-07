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
        'username': 'testuser',
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

def test_delete_user(test_client, init_database, auth_tokens):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.delete('/api/auth/users/me', headers=headers)
    assert response.status_code == 204