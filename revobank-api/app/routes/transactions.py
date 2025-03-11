from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account import Account
from app.models.transaction import Transaction
from app import db
from werkzeug.exceptions import NotFound, Forbidden, BadRequest
from datetime import datetime
from decimal import Decimal

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('', methods=['GET'])
@jwt_required()
def get_all_transactions():
    current_user_id = int(get_jwt_identity())
    args = request.args

    # Base query to find transactions where user owns either account
    query = Transaction.query.join(Account, (
        (Account.id == Transaction.from_account_id) | 
        (Account.id == Transaction.to_account_id)
    )).filter(Account.user_id == current_user_id)

    # Apply filters if provided
    if 'account_id' in args:
        account_id = int(args['account_id'])
        query = query.filter(
            (Transaction.from_account_id == account_id) | 
            (Transaction.to_account_id == account_id)
        )
    
    if 'start_date' in args:
        start_date = datetime.fromisoformat(args['start_date'])
        query = query.filter(Transaction.created_at >= start_date)
    
    if 'end_date' in args:
        end_date = datetime.fromisoformat(args['end_date'])
        query = query.filter(Transaction.created_at <= end_date)

    transactions = query.all()
    return jsonify([t.serialize() for t in transactions]), 200

@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    current_user_id = int(get_jwt_identity())
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None:
        raise NotFound("Transaction not found")

    # Check if user owns at least one related account
    has_access = False
    if transaction.from_account:
        has_access = transaction.from_account.user_id == current_user_id
    if transaction.to_account:
        has_access = has_access or transaction.to_account.user_id == current_user_id

    if not has_access:
        raise Forbidden("You don't have access to this transaction")

    return jsonify(transaction.serialize()), 200

@transactions_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    # Validate required fields
    required = ['type', 'amount']
    if not all(field in data for field in required):
        raise BadRequest("Missing required fields")

    # Validate transaction type
    if data['type'] not in ['deposit', 'withdrawal', 'transfer']:
        raise BadRequest("Invalid transaction type")

    # Validate accounts based on type
    from_account = None
    to_account = None

    if data['type'] == 'transfer':
        if not data.get('from_account_id') or not data.get('to_account_id'):
            raise BadRequest("Both from_account_id and to_account_id required for transfers")
    elif data['type'] == 'withdrawal':
        if not data.get('from_account_id'):
            raise BadRequest("from_account_id required for withdrawals")
    elif data['type'] == 'deposit':
        if not data.get('to_account_id'):
            raise BadRequest("to_account_id required for deposits")

    # Load and validate accounts
    if 'from_account_id' in data:
        from_account = db.session.get(Account, data['from_account_id'])
        if from_account is None:
            raise NotFound("Source account not found")
        if from_account.user_id != current_user_id:
            raise Forbidden("You don't own the source account")

    if 'to_account_id' in data:
        to_account = db.session.get(Account, data['to_account_id'])
        if to_account is None:
            raise NotFound("Destination account not found")
        # Allow transfers to other users' accounts but deposits must be to your own account
        if data['type'] != 'transfer' and to_account.user_id != current_user_id:
            raise Forbidden("Invalid destination account")

    # Check sufficient funds for withdrawals or transfers
    if data['type'] in ['withdrawal', 'transfer']:
        if from_account.balance < Decimal(data['amount']):
            raise BadRequest("Insufficient funds")

    # Convert amount from string to Decimal for arithmetic
    amount = Decimal(data['amount'])

    # Create transaction and update balances
    try:
        transaction = Transaction(
            type=data['type'],
            amount=amount,
            from_account_id=data.get('from_account_id'),
            to_account_id=data.get('to_account_id'),
            description=data.get('description')
        )
        db.session.add(transaction)

        if data['type'] == 'deposit':
            to_account.balance += amount
        elif data['type'] == 'withdrawal':
            from_account.balance -= amount
        elif data['type'] == 'transfer':
            from_account.balance -= amount
            to_account.balance += amount

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise BadRequest(f"Transaction failed: {str(e)}")

    return jsonify(transaction.serialize()), 201