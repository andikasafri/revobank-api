def test_create_account(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/accounts', json={
        'account_type': 'savings',
        'account_number': 'ACC-654321'
    }, headers=headers)
    assert response.status_code == 201
    assert 'account_number' in response.json

def test_get_accounts(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.get('/api/accounts', headers=headers)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_delete_account_with_balance(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.delete('/api/accounts/1', headers=headers)
    assert response.status_code == 400