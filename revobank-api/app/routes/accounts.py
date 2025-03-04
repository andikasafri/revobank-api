# Account Management
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account import Account
from app.models.user import User
from app import db
from werkzeug.exceptions import BadRequest, NotFound, Forbidden

accounts_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')

@accounts_bp.route('', methods=['GET'])
@jwt_required()
def get_all_accounts():
    current_user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=current_user_id).all()
    return jsonify([acc.serialize() for acc in accounts]), 200

@accounts_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_single_account(account_id):
    current_user_id = get_jwt_identity()
    account = Account.query.get_or_404(account_id)
    
    if account.user_id != current_user_id:
        raise Forbidden("You don't have access to this account")
    
    return jsonify(account.serialize()), 200

@accounts_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    new_account = Account(
        user_id=current_user_id,
        account_type=data['account_type'],
        account_number=data['account_number'],
        balance=data.get('balance', 0.00)
    )
    
    db.session.add(new_account)
    db.session.commit()
    return jsonify(new_account.serialize()), 201