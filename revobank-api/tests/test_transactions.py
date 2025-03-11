import pytest
from decimal import Decimal
from app.models.account import Account
from app.models.user import User
from app.models.transaction import Transaction
from app import db

def test_deposit(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'deposit',
        'to_account_id': 1,
        'amount': 500.00
    }, headers=headers)
    
    assert response.status_code == 201
    assert response.json['type'] == 'deposit'
    assert response.json['amount'] == '500.00'
    
    # Verify account balance updated
    account = db.session.get(Account, 1)  
    assert account.balance == Decimal('1500.00')

def test_insufficient_funds(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'withdrawal',
        'from_account_id': 1,
        'amount': 2000.00
    }, headers=headers)
    
    assert response.status_code == 400
    assert 'Insufficient funds' in response.json['description']  
    
    # Verify balance remains unchanged
    account = db.session.get(Account, 1)
    assert account.balance == Decimal('1000.00')

def test_create_transfer_success(test_client, auth_tokens, init_database):
    # Create second account for same user
    account2 = Account(
        user_id=1,
        account_type='checking',
        account_number='ACC-654321',
        balance=500.00
    )
    db.session.add(account2)
    db.session.commit()
    
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'transfer',
        'from_account_id': 1,
        'to_account_id': 2,
        'amount': 200.00
    }, headers=headers)
    
    assert response.status_code == 201
    assert response.json['type'] == 'transfer'
    
    # Verify balances using correct session
    from_account = db.session.get(Account, 1)
    to_account = db.session.get(Account, 2)
    assert from_account.balance == Decimal('800.00')
    assert to_account.balance == Decimal('700.00')

def test_transfer_insufficient_funds(test_client, auth_tokens, init_database):
    # Create second account
    account2 = Account(
        user_id=1,
        account_type='checking',
        account_number='ACC-654321',
        balance=500.00
    )
    db.session.add(account2)
    db.session.commit()
    
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'transfer',
        'from_account_id': 1,
        'to_account_id': 2,
        'amount': 1500.00
    }, headers=headers)
    
    assert response.status_code == 400
    assert 'Insufficient funds' in response.json['description']  # Corrected key

def test_transfer_to_other_user(test_client, auth_tokens, init_database):
    # Create another user and account
    user2 = User(username='user2', email='user2@example.com')
    user2.set_password('Pass123!')
    account2 = Account(
        user_id=2,
        account_type='savings',
        account_number='ACC-OTHER',
        balance=500.00
    )
    db.session.add_all([user2, account2])
    db.session.commit()
    
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'transfer',
        'from_account_id': 1,
        'to_account_id': 2,
        'amount': 200.00
    }, headers=headers)
    
    assert response.status_code == 201
    # Verify balances using correct session
    from_account = db.session.get(Account, 1)
    to_account = db.session.get(Account, 2)
    assert from_account.balance == Decimal('800.00')
    assert to_account.balance == Decimal('700.00')

def test_negative_amount(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'deposit',
        'to_account_id': 1,
        'amount': -100.00
    }, headers=headers)
    
    assert response.status_code == 400
    assert 'Amount must be positive' in response.json['description']

    # Verify balances
    from_account = Account.db.session.get(1)
    to_account = Account.db.session.get(2)
    assert from_account.balance == Decimal('800.00')
    assert to_account.balance == Decimal('700.00')

def test_invalid_transaction_type(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'loan',
        'from_account_id': 1,
        'amount': 100.00
    }, headers=headers)
    
    assert response.status_code == 400
    assert 'Invalid transaction type' in response.json['description']

def test_missing_required_fields(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    
    # Missing to_account_id for deposit
    response = test_client.post('/api/transactions', json={
        'type': 'deposit',
        'amount': 100.00
    }, headers=headers)
    assert response.status_code == 400
    
    # Missing from_account_id for withdrawal
    response = test_client.post('/api/transactions', json={
        'type': 'withdrawal',
        'amount': 100.00
    }, headers=headers)
    assert response.status_code == 400
    
    # Missing from/to for transfer
    response = test_client.post('/api/transactions', json={
        'type': 'transfer',
        'amount': 100.00
    }, headers=headers)
    assert response.status_code == 400

def test_get_transaction_details(test_client, auth_tokens, init_database):
    # Create a transaction
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'deposit',
        'to_account_id': 1,
        'amount': 500.00
    }, headers=headers)
    transaction_id = response.json['id']
    
    # Retrieve transaction
    response = test_client.get(f'/api/transactions/{transaction_id}', headers=headers)
    assert response.status_code == 200
    assert response.json['id'] == transaction_id
    assert response.json['type'] == 'deposit'
    assert response.json['amount'] == '500.00'

def test_access_other_users_transaction(test_client, auth_tokens, init_database):
    # Create another user and transaction
    user2 = User(username='user2', email='user2@example.com')
    user2.set_password('Pass123!')
    account2 = Account(
        user_id=2,
        account_type='savings',
        account_number='ACC-USER2',
        balance=500.00
    )
    db.session.add_all([user2, account2])
    db.session.commit()
    
    # Create transaction for user2
    transaction = Transaction(
        type='deposit',
        amount=100.00,
        to_account_id=2
    )
    db.session.add(transaction)
    db.session.commit()
    
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.get(f'/api/transactions/{transaction.id}', headers=headers)
    assert response.status_code == 403

def test_transaction_date_filtering(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    
    # Create transaction with known date
    test_client.post('/api/transactions', json={
        'type': 'deposit',
        'to_account_id': 1,
        'amount': 500.00
    }, headers=headers)
    
    start_date = '2023-01-01T00:00:00'
    end_date = '2030-01-01T00:00:00'
    
    response = test_client.get(
        f'/api/transactions?start_date={start_date}&end_date={end_date}',
        headers=headers
    )
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_negative_amount(test_client, auth_tokens, init_database):
    headers = {'Authorization': f'Bearer {auth_tokens["access_token"]}'}
    response = test_client.post('/api/transactions', json={
        'type': 'deposit',
        'to_account_id': 1,
        'amount': -100.00
    }, headers=headers)
    
    assert response.status_code == 400
    assert 'Amount must be positive' in response.json['description']