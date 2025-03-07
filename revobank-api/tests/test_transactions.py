def test_deposit(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'deposit',
        'to_account_id': 1,
        'amount': 500.00
    }, headers=headers)
    assert response.status_code == 201
    assert response.json['type'] == 'deposit'

def test_insufficient_funds(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'withdrawal',
        'from_account_id': 1,
        'amount': 2000.00
    }, headers=headers)
    assert response.status_code == 400

def test_transaction_history(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.get('/api/transactions?account_id=1', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)