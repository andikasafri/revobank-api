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
    updated_account = db.session.get(Account, 1)
    assert updated_account.account_type == 'checking'

def test_update_account_number_success(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.put('/api/accounts/1', json={
        'account_number': 'ACC-UPDATED'
    }, headers=headers)
    assert response.status_code == 200
    updated_account = db.session.get(Account, 1)
    assert updated_account.account_number == 'ACC-UPDATED'

def test_update_non_existent_account(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.put('/api/accounts/999', json={
        'account_type': 'checking'
    }, headers=headers)
    assert response.status_code == 404

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
    assert new_account.user_id == 1

@pytest.fixture
def account_data():
    return {
        "account_type": "savings",
        "account_number": "ACC-TEST123"
    }

def test_create_account(test_client, auth_tokens, account_data):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    res = test_client.post("/api/accounts", json=account_data, headers=headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data["account_number"] == account_data["account_number"]
    assert data["account_type"] == account_data["account_type"]
    assert data["status"] == "active"

def test_get_all_accounts(test_client, auth_tokens):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    res = test_client.get("/api/accounts", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_single_account(test_client, auth_tokens, init_database):
    account = Account(user_id=1, account_type="checking", account_number="ACC-GET1")
    db.session.add(account)
    db.session.commit()

    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    res = test_client.get(f"/api/accounts/{account.id}", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["account_number"] == "ACC-GET1"

def test_update_account(test_client, auth_tokens, init_database):
    account = Account(user_id=1, account_type="savings", account_number="ACC-OLD123")
    db.session.add(account)
    db.session.commit()

    update_data = {"account_type": "investment", "account_number": "ACC-NEW123"}
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    res = test_client.put(f"/api/accounts/{account.id}", json=update_data, headers=headers)
    assert res.status_code == 200
    updated = res.get_json()
    assert updated["account_type"] == "investment"
    assert updated["account_number"] == "ACC-NEW123"

def test_deactivate_account(test_client, auth_tokens, init_database):
    account = Account(user_id=1, account_type="checking", account_number="ACC-DEACT0", balance=0)
    db.session.add(account)
    db.session.commit()

    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    res = test_client.post(f"/api/accounts/{account.id}/deactivate", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Account deactivated successfully"

def test_delete_account(test_client, auth_tokens, init_database):
    account = Account(user_id=1, account_type="checking", account_number="ACC-DELETE0", balance=0, status="deactivated")
    db.session.add(account)
    db.session.commit()

    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    res = test_client.delete(f"/api/accounts/{account.id}", headers=headers)
    assert res.status_code == 204