# accounts.py - Account Management Routes
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account import Account
from app import db
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from sqlalchemy.exc import IntegrityError

# Initialize Blueprint for account routes
accounts_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')

# Valid account types allowed for creation/update
ALLOWED_TYPES = {'savings', 'checking', 'investment'}

@accounts_bp.route('', methods=['GET'])
@jwt_required()
def get_all_accounts():
    """Retrieve all accounts for authenticated user
    
    Security: Requires valid JWT token
    Response: List of user's accounts in JSON format
    """
    current_user_id = int(get_jwt_identity())
    accounts = Account.query.filter_by(user_id=current_user_id).all()
    return jsonify([acc.serialize() for acc in accounts]), 200

@accounts_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_single_account(account_id):
    """Retrieve specific account details
    
    Args:
        account_id: ID of the account to retrieve
        
    Security: Requires ownership of the account
    Response: Account details in JSON format
    """
    current_user_id = int(get_jwt_identity())
    account = Account.query.get_or_404(account_id)
    
    if account.user_id != current_user_id:
        raise Forbidden("You don't have access to this account")
    
    return jsonify(account.serialize()), 200

@accounts_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    """Create a new bank account
    
    Required fields:
        account_type: Must be one of ALLOWED_TYPES
        account_number: Unique identifier starting with 'ACC-'
        
    Security: Automatically sets user_id from JWT
    Response: Created account details
    """
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    # Validate required fields
    required_fields = ['account_type', 'account_number']
    if not all(field in data for field in required_fields):
        raise BadRequest(f"Missing required fields: {required_fields}")

    # Validate account type
    if data['account_type'] not in ALLOWED_TYPES:
        raise BadRequest(f"Invalid account type. Allowed: {ALLOWED_TYPES}")

    # Validate account number format
    if not data['account_number'].startswith('ACC-'):
        raise BadRequest("Account numbers must start with 'ACC-'")

    try:
        new_account = Account(
            user_id=current_user_id,
            account_type=data['account_type'],
            account_number=data['account_number']
        )
        db.session.add(new_account)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise BadRequest("Account number already exists")

    return jsonify(new_account.serialize()), 201

@accounts_bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    """Update account details
    
    Allowed updates:
        account_type: Change account type (within ALLOWED_TYPES)
        account_number: Update unique identifier starting with 'ACC-'
        
    Security: Requires account ownership
    """
    current_user_id = int(get_jwt_identity())
    account = Account.query.get_or_404(account_id)
    
    if account.user_id != current_user_id:
        raise Forbidden("You don't have access to this account")
    
    data = request.get_json()
    if not data:
        raise BadRequest("No update data provided")

    # Validate at least one field to update
    if not any(field in data for field in ['account_type', 'account_number']):
        raise BadRequest("No valid fields to update")

    # Update account type if provided
    if 'account_type' in data:
        if data['account_type'] not in ALLOWED_TYPES:
            raise BadRequest(f"Invalid account type. Allowed: {ALLOWED_TYPES}")
        account.account_type = data['account_type']

    # Update account number with format and uniqueness checks
    if 'account_number' in data:
        # Format validation
        if not data['account_number'].startswith('ACC-'):
            raise BadRequest("Account numbers must start with 'ACC-'")
            
        # Uniqueness check
        existing = Account.query.filter_by(account_number=data['account_number']).first()
        if existing and existing.id != account.id:
            raise BadRequest("Account number already in use")
        account.account_number = data['account_number']

    db.session.commit()
    return jsonify(account.serialize()), 200

# @accounts_bp.route('/<int:account_id>', methods=['DELETE'])
# @jwt_required()
# def delete_account(account_id):
#     """Permanently delete an account
    
#     Restrictions:
#         - Requires account ownership
#         - Account balance must be zero
        
#     Response: 204 No Content
#     """
#     current_user_id = int(get_jwt_identity())
#     account = Account.query.get_or_404(account_id)
    
#     if account.user_id != current_user_id:
#         raise Forbidden("You don't have access to this account")
    
#     if account.balance != 0:
#         raise BadRequest("Cannot delete account with non-zero balance")

#     db.session.delete(account)
#     db.session.commit()
#     return "", 204  # Proper 204 response with empty body
@accounts_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    current_user_id = int(get_jwt_identity())
    account = Account.query.get_or_404(account_id)
    
    if account.user_id != current_user_id:
        raise Forbidden("You don't have access to this account")
    
    if account.balance != 0:
        raise BadRequest("Cannot delete account with non-zero balance")

    # try:
    db.session.delete(account)
    db.session.commit()
    # except IntegrityError as e:
    #     db.session.rollback()
    #     if "foreign key constraint" in str(e.orig).lower():
    #         raise Conflict("Account has associated transactions - delete them first")
    #     raise InternalServerError("Database error occurred")
    
    return "", 204