# Detailed Explanation of `account.py` and `accounts.py`

## **1. `account.py` - Database Model**

This file defines the structure of the `accounts` table in the database using SQLAlchemy ORM. It ensures proper data integrity and serialization for API responses.

### **Class Definition**

```python
class Account(db.Model):
    __tablename__ = 'accounts'
```

- **Purpose**: Defines a table named `accounts` in the database.
- **Why**: Helps organize all account-related data efficiently.

### **Columns**

#### **Primary Key**

```python
id = db.Column(db.Integer, primary_key=True)
```

- **Purpose**: Unique identifier for each account.
- **Why**: Ensures each account has a unique reference, allowing efficient database operations.

#### **Foreign Key: User ID**

```python
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```

- **Purpose**: Links the account to a specific user.
- **Why**: Enforces that every account belongs to an existing user, preventing orphaned data.

#### **Account Type**

```python
account_type = db.Column(db.String(255), nullable=False)
```

- **Purpose**: Stores the type of account (e.g., "savings", "checking").
- **Why**: Allows categorization of accounts based on type.

#### **Balance**

```python
balance = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
```

- **Purpose**: Stores the current balance of the account.
- **Why**: `Numeric(10,2)` ensures precision and prevents rounding errors in financial transactions.

#### **Timestamps**

```python
created_at = db.Column(db.DateTime, server_default=db.func.now())
updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
```

- **Purpose**: Track account creation and modification times.
- **Why**: Helps in auditing changes over time.

#### **Account Number**

```python
account_number = db.Column(db.String(20), unique=True, nullable=False)
```

- **Purpose**: A unique identifier for each account.
- **Why**: Ensures no duplicate account numbers.

### **Constraints**

```python
__table_args__ = (
    CheckConstraint(balance >= 0.00, name='non_negative_balance'),
    CheckConstraint("account_number LIKE 'ACC-%%'", name='account_number_format')
)
```

- **Purpose**:
  - Prevent negative balances.
  - Ensure account numbers start with `ACC-`.
- **Why**: Enforce business rules at the database level.

### **Serialization Method**

```python
def serialize(self):
    return {
        'id': self.id,
        'user_id': self.user_id,
        'account_type': self.account_type,
        'account_number': self.account_number,
        'balance': str(self.balance),
        'created_at': self.created_at.isoformat() if self.created_at else None,
        'updated_at': self.updated_at.isoformat() if self.updated_at else None
    }
```

- **Purpose**: Converts database objects to JSON format.
- **Why**:
  - String conversion for `balance` prevents precision loss.
  - `isoformat()` standardizes date formatting.

---

## **2. `accounts.py` - API Routes**

This file defines API endpoints for account management, using Flask and JWT authentication.

### **Blueprint Setup**

```python
accounts_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')
ALLOWED_TYPES = {'savings', 'checking', 'investment'}
```

- **Purpose**: Registers account-related routes under `/api/accounts`.
- **Why**: Keeps the application modular and structured.

### **GET All Accounts**

```python
@accounts_bp.route('', methods=['GET'])
@jwt_required()
def get_all_accounts():
    current_user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=current_user_id).all()
    return jsonify([acc.serialize() for acc in accounts]), 200
```

- **Purpose**: Retrieves all accounts for the logged-in user.
- **Why**: Ensures users only access their own data.

### **GET Single Account**

```python
@accounts_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_single_account(account_id):
    current_user_id = get_jwt_identity()
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user_id:
        raise Forbidden("You don't have access to this account")
    return jsonify(account.serialize()), 200
```

- **Purpose**: Fetches a specific account if the user owns it.
- **Why**: Prevents unauthorized access to other users’ accounts.

### **POST Create Account**

```python
@accounts_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if data['account_type'] not in ALLOWED_TYPES:
        raise BadRequest(f"Invalid account type. Allowed: {ALLOWED_TYPES}")

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
```

- **Purpose**: Creates a new account.
- **Why**:
  - Validates `account_type` and `account_number`.
  - Ensures unique account numbers.
  - Uses `jwt_required()` to associate accounts with authenticated users.

### **PUT Update Account**

```python
@accounts_bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    current_user_id = get_jwt_identity()
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user_id:
        raise Forbidden("You don't have access to this account")

    data = request.get_json()
    if 'account_type' in data and data['account_type'] in ALLOWED_TYPES:
        account.account_type = data['account_type']

    if 'account_number' in data and data['account_number'].startswith('ACC-'):
        account.account_number = data['account_number']

    db.session.commit()
    return jsonify(account.serialize()), 200
```

- **Purpose**: Updates account type or number.
- **Why**: Enforces validation and ownership checks.

### **DELETE Account**

```python
@accounts_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    current_user_id = get_jwt_identity()
    account = Account.query.get_or_404(account_id)
    if account.user_id != current_user_id:
        raise Forbidden("You don't have access to this account")
    if account.balance != 0:
        raise BadRequest("Cannot delete account with non-zero balance")

    db.session.delete(account)
    db.session.commit()
    return "", 204
```

- **Purpose**: Deletes an account if balance is zero.
- **Why**: Prevents accidental deletion of active accounts.

---

### **Summary**

- `account.py` defines the database model.
- `accounts.py` handles API requests.
- Security checks ensure users can only access their own accounts.
- Database constraints enforce data integrity.

Testing Checklist

    POST /api/accounts
        ✅ Creates account with valid data
        ❌ Rejects invalid account types
        ❌ Rejects duplicate account numbers
        ❌ Enforces account number format


    PUT /api/accounts/:id
        ✅ Updates allowed fields
        ❌ Rejects invalid account types
        ❌ Prevents duplicate account numbers


    DELETE /api/accounts/:id
        ✅ Deletes account with zero balance
        ❌ Blocks deletion with non-zero balance


