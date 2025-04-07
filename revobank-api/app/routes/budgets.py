from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.budget import Budget
from app import db
from werkzeug.exceptions import BadRequest, NotFound, Forbidden

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('', methods=['POST'])
@jwt_required()
def create_budget():
    """Create a new budget for a specific category."""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    required_fields = ['name', 'amount', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        raise BadRequest("Missing required fields")
    try:
        new_budget = Budget(
            user_id=current_user_id,
            name=data['name'],
            amount=data['amount'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        db.session.add(new_budget)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise BadRequest(f"Error creating budget: {str(e)}")
    return jsonify(new_budget.serialize()), 201

@budgets_bp.route('', methods=['GET'])
@jwt_required()
def get_budgets():
    """Retrieve all budgets created by the user."""
    current_user_id = int(get_jwt_identity())
    budgets = Budget.query.filter_by(user_id=current_user_id).all()
    return jsonify([b.serialize() for b in budgets]), 200

@budgets_bp.route('/<int:budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    """Update an existing budget."""
    current_user_id = int(get_jwt_identity())
    budget = db.session.get(Budget, budget_id)
    if not budget:
        raise NotFound("Budget not found")
    if budget.user_id != current_user_id:
        raise Forbidden("Access denied")
    data = request.get_json()
    if not data:
        raise BadRequest("No update data provided")
    for field in ['name', 'amount', 'start_date', 'end_date']:
        if field in data:
            setattr(budget, field, data[field])
    db.session.commit()
    return jsonify(budget.serialize()), 200
