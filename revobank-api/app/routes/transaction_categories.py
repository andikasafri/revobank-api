from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.transaction_category import TransactionCategory

transaction_categories_bp = Blueprint('transaction_categories', __name__)

@transaction_categories_bp.route('', methods=['GET'])
@jwt_required()
def get_transaction_categories():
    """Retrieve a list of transaction categories for budgeting purposes."""
    categories = TransactionCategory.query.all()
    return jsonify([cat.serialize() for cat in categories]), 200
