# Revobank API

A Flask-based REST API for banking operations—securely handling user data, account details, and transaction history using SQLAlchemy and JWT. The API is deployed on Koyeb, connected to a Supabase PostgreSQL database, and auto-updates via GitHub and Docker.

## Overview

Revobank API is the backbone of the RevoBank application. It provides endpoints to:

- **Manage Users:** Register, authenticate (with JWT), retrieve profiles, update, and delete users.
- **Manage Accounts:** Create and manage bank accounts.
- **Handle Transactions:** Perform deposits, withdrawals, transfers, and view transaction histories.
- **Database Enhancements:** The updated database schema now includes Bills, Transaction Categories, and Budgets. (New routes for these models and middleware are coming soon.)

### Database Schema & Relationships

The database (deployed on Supabase) includes the following tables:

- **Users:**

  - `id` (INT, PK)
  - `username` (VARCHAR(255), Unique)
  - `email` (VARCHAR(255), Unique)
  - `password_hash` (VARCHAR(255))
  - `created_at` (DATETIME)
  - `updated_at` (DATETIME)

- **Accounts:**

  - `id` (INT, PK)
  - `user_id` (INT, FK → Users.id)
  - `account_type` (VARCHAR(255))
  - `account_number` (VARCHAR(255), Unique)
  - `balance` (DECIMAL(10, 2))
  - `created_at` (DATETIME)
  - `updated_at` (DATETIME)

- **Transactions:**

  - `id` (INT, PK)
  - `from_account_id` (INT, FK → Accounts.id, optional)
  - `to_account_id` (INT, FK → Accounts.id, optional)
  - `amount` (DECIMAL(10, 2))
  - `type` (VARCHAR(255))
  - `description` (VARCHAR(255))
  - `created_at` (DATETIME)
  - `category_id` (INT, FK → TransactionCategories.id) _(optional)_

- **Bills:**

  - Stores billing information for users.

- **Transaction Categories:**

  - Defines categories for transactions.

- **Budgets:**
  - Enables users to manage their budgeting limits.

**Relationships:**

- One user can have many accounts.
- One account can have many transactions.
- Transactions can link accounts as sender and receiver.
- Bills, Transaction Categories, and Budgets are integrated into the schema for future expansion.

![Visual Overview of the Schema](public/db_schema.png)

## Installation & Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/revou-fsse-oct24/milestone-3-andikasafri.git
   cd revobank-api
   ```

2. **Download Required Files:**

   Ensure that all necessary files (including the Flask project, Dockerfile, and configuration files) are inside the `revobank-api/revobank-api` directory.

3. **Set Environment Variables:**

   Create a `.env` file in the repository root with the following variables (adjust values as needed):

   ```bash
   DB_HOST=<your_supabase_db_host>
   DB_NAME=<your_supabase_db_name>
   DB_USER=<your_supabase_db_user>
   DB_PASSWORD=<your_supabase_db_password>
   JWT_SECRET_KEY=<your_jwt_secret_key>
   FLASK_ENV=production
   DB_SSL_MODE=require
   ```

4. **Run Database Migrations:**

   From the root of your repository, execute:

   ```bash
   flask db upgrade
   ```

   This will update the schema on your Supabase database based on the latest models (Users, Accounts, Transactions, Bills, Transaction Categories, and Budgets).

## Docker Deployment

The repository includes a `docker-compose.yml` file to streamline deployment.

1. **Start the Application with Docker Compose:**

   ```bash
   docker-compose up
   ```

   This command builds the Docker images, runs the containers, and launches the API service.

2. **Auto-Deployment:**

   The project is set up for auto-deployment using GitHub. Every push triggers a Docker build and deployment update so that the live API on Koyeb is updated in real time.

## Deployed API

The live API is accessible at:
[https://vocal-katherine-andika-safri-69a23cb3.koyeb.app/](https://vocal-katherine-andika-safri-69a23cb3.koyeb.app/)

## SQLAlchemy & JWT Integration

### SQLAlchemy

- **Model Definitions:**
  All tables (Users, Accounts, Transactions, Bills, Transaction Categories, and Budgets) are defined as SQLAlchemy models in the `app/models` directory.

- **Database Session:**
  Interactions with the database are handled via `db.session` (e.g., retrieving a user with `db.session.get(User, current_user_id)`).

- **Relationships:**
  Relationships (such as one-to-many between Users and Accounts) are established using SQLAlchemy's `relationship` function.

### JWT Authentication

- **JWT Setup:**
  Flask-JWT-Extended is used for secure authentication. Tokens are generated with a 3-hour expiry. For example, in `services/auth.py`:

  ```python
  from datetime import timedelta
  from flask_jwt_extended import create_access_token

  def generate_token(user_id):
      return create_access_token(identity=str(user_id), expires_delta=timedelta(hours=3))
  ```

- **Protected Routes:**
  Endpoints, such as the route for fetching the current user, are protected using the `@jwt_required()` decorator. See `routes/auth.py` for an example:

  ```python
  @auth_bp.route('/users/me', methods=['GET'])
  @jwt_required()
  def get_current_user():
      current_user_id = get_jwt_identity()
      user = db.session.get(User, current_user_id)
      if user is None:
          raise NotFound("User not found")
      return jsonify({
          'id': user.id,
          'username': user.username,
          'email': user.email,
          'created_at': user.created_at.isoformat(),
      }), 200
  ```

## API Documentation

For testing all available endpoints (including headers, body, and parameters), please refer to the detailed guide here:
[https://flask-api-endpoints.netlify.app/](https://flask-api-endpoints.netlify.app/)

### Endpoints Overview

#### User Management

- **User Registration:** `POST /api/auth/users`
  Create a new user account.
  _Example:_ Use HTTPie or Postman to provide `username`, `email`, and `password`.

- **User Login:** `POST /api/auth/login`
  Authenticate and receive a JWT access token.

- **Get Current User:** `GET /api/auth/users/me`
  Requires header: `Authorization: Bearer <ACCESS_TOKEN>`

#### Account Management

- **Get All Accounts:** `GET /api/accounts`
- **Get Single Account:** `GET /api/accounts/:id`
- **Create Account:** `POST /api/accounts`
- **Update Account:** `PUT /api/accounts/:id`
- **Delete Account:** `DELETE /api/accounts/:id`

#### Transaction Management

- **Get All Transactions:** `GET /api/transactions`
- **Get Single Transaction:** `GET /api/transactions/:id`
- **Create Transaction:** `POST /api/transactions`
  _Note:_ Include the proper account IDs for deposits, withdrawals, or transfers. Optionally provide `category_id` for transaction categorization.

## Additional Notes

- **Model Updates:**
  The database schema now includes Bills, Transaction Categories, and Budgets. Although there are no new routes for these models yet, the models and migrations have been updated for future expansion.

- **Future Enhancements:**
  New endpoints and middleware will be added soon to extend functionality and improve request handling.

- **Deployment & Logging:**
  The application uses Flask's error handlers and logging to capture issues. Deployment is managed via Docker and auto-deployed on Koyeb, ensuring the live API is continuously updated.

## Deliverables & Grading Component

- **Database Connection:**
  The project connects to a Supabase PostgreSQL database using SQLAlchemy.

- **Schema Design:**
  The database schema is implemented as described, with all required tables and relationships.

- **CRUD Operations:**
  All CRUD operations for Users, Accounts, and Transactions have been implemented and validated.

- **Flask Authentication:**
  Secure user authentication using JWT is in place.

- **Deployed API & Documentation:**
  The live API is deployed on Koyeb and documented with instructions for testing endpoints at [https://flask-api-endpoints.netlify.app/](https://flask-api-endpoints.netlify.app/).

- **Source Code Repository:**
  The complete codebase is available on GitHub with integrated SQLAlchemy and auto-deployment via Docker.
