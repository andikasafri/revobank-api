from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.bill import Bill
from app.models.account import Account
from app import db
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from decimal import Decimal

bills_bp = Blueprint('bills', __name__)

@bills_bp.route('', methods=['POST'])
@jwt_required()
def create_bill():
    """Schedule a bill payment for a specific biller."""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    required_fields = ['biller_name', 'due_date', 'amount', 'account_id']
    if not all(field in data for field in required_fields):
        raise BadRequest("Missing required fields")
    
    account = db.session.get(Account, data['account_id'])
    if not account or account.user_id != current_user_id:
        raise NotFound("Account not found or access denied")
    
    try:
        amount = Decimal(data['amount'])
    except Exception:
        raise BadRequest("Invalid amount format")
    
    new_bill = Bill(
        user_id=current_user_id,
        account_id=data['account_id'],
        biller_name=data['biller_name'],
        due_date=data['due_date'],
        amount=amount
    )
    db.session.add(new_bill)
    db.session.commit()
    return jsonify(new_bill.serialize()), 201

@bills_bp.route('', methods=['GET'])
@jwt_required()
def get_bills():
    """Retrieve all scheduled bill payments."""
    current_user_id = int(get_jwt_identity())
    bills = Bill.query.filter_by(user_id=current_user_id).all()
    return jsonify([bill.serialize() for bill in bills]), 200

@bills_bp.route('/<int:bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(bill_id):
    """Update the details of a scheduled bill payment."""
    current_user_id = int(get_jwt_identity())
    bill = db.session.get(Bill, bill_id)
    if not bill:
        raise NotFound("Bill not found")
    if bill.user_id != current_user_id:
        raise Forbidden("Access denied")
    data = request.get_json()
    if not data:
        raise BadRequest("No update data provided")
    for field in ['biller_name', 'due_date', 'amount', 'account_id']:
        if field in data:
            setattr(bill, field, data[field])
    db.session.commit()
    return jsonify(bill.serialize()), 200

@bills_bp.route('/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    """Cancel a scheduled bill payment."""
    current_user_id = int(get_jwt_identity())
    bill = db.session.get(Bill, bill_id)
    if not bill:
        raise NotFound("Bill not found")
    if bill.user_id != current_user_id:
        raise Forbidden("Access denied")
    db.session.delete(bill)
    db.session.commit()
    return '', 204
