# test_accounts.py
import pytest
from app.models.account import Account
from app.models.user import User
from app import db

def test_get_single_account_success(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.get('/api/accounts/1', headers=headers)
    assert response.status_code == 200
    assert response.json['account_number'] == 'ACC-123456'

def test_get_non_existent_account(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.get('/api/accounts/999', headers=headers)
    assert response.status_code == 404

def test_update_account_type_success(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.put('/api/accounts/1', json={
        'account_type': 'checking'
    }, headers=headers)
    assert response.status_code == 200
    updated_account = Account.query.get(1)
    assert updated_account.account_type == 'checking'

def test_update_account_number_success(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.put('/api/accounts/1', json={
        'account_number': 'ACC-UPDATED'
    }, headers=headers)
    assert response.status_code == 200
    updated_account = Account.query.get(1)
    assert updated_account.account_number == 'ACC-UPDATED'

def test_update_non_existent_account(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.put('/api/accounts/999', json={
        'account_type': 'checking'
    }, headers=headers)
    assert response.status_code == 404

def test_delete_account_success(test_client, auth_tokens, init_database):
    new_account = Account(
        user_id=1,
        account_type='checking',
        account_number='ACC-DELETE',
        balance=0.00
    )
    db.session.add(new_account)
    db.session.commit()
    
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.delete(f'/api/accounts/{new_account.id}', headers=headers)
    assert response.status_code == 204
    assert Account.query.get(new_account.id) is None

def test_delete_non_existent_account(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.delete('/api/accounts/999', headers=headers)
    assert response.status_code == 404

def test_create_account_ignores_user_id(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/accounts', json={
        'account_type': 'savings',
        'account_number': 'ACC-IGNOREUSERID',
        'user_id': 999
    }, headers=headers)
    assert response.status_code == 201
    new_account = Account.query.filter_by(account_number='ACC-IGNOREUSERID').first()
    assert new_account.user_id == 1  # Assuming test user has ID 1