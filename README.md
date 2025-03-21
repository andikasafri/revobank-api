# Revobank API

A Flask-based REST API for banking operations.

## Features

- User Authentication (JWT)
- Account Management
- Transaction Processing
- PostgreSQL Database (Supabase)

## Deployment

1. Set environment variables in Koyeb
2. Enable auto-deployment from GitHub
3. Configure health checks
4. Set up proper logging

## Environment Variables Required

- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `JWT_SECRET_KEY`
- `FLASK_ENV`

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [API Documentation](#api-documentation)
  - [User Management](#user-management)
    - [User Registration](#user-registration)
    - [User Login](#user-login)
    - [Get Current User Details](#get-current-user-details)
    - [Update Current User](#update-current-user)
    - [Delete Current User](#delete-current-user)
  - [Account Management](#account-management)
    - [Get All Accounts](#get-all-accounts)
    - [Get Single Account](#get-single-account)
    - [Create New Account](#create-new-account)
    - [Update Account](#update-account)
    - [Delete Account](#delete-account)
  - [Transaction Management](#transaction-management)
    - [Get All Transactions](#get-all-transactions)
    - [Get Single Transaction](#get-single-transaction)
    - [Create Transaction](#create-transaction)
- [Additional Notes](#additional-notes)
- [Deployment](#deployment)
- [Grading Component (Module 7 Assignment)](#grading-component-module-7-assignment)

## Overview

Revobank API acts as the backbone for the RevoBank application by providing secure and efficient endpoints for:

- **User Management:** Creating users, authentication, profile retrieval, updates, and deletion.
- **Account Management:** Creating and managing bank accounts.
- **Transaction Management:** Deposits, withdrawals, transfers, and transaction history retrieval.

## Features

- **Secure Authentication:** Uses JWT via Flask-JWT-Extended.
- **Robust Error Handling:** Validations for required fields, authorization checks, and proper HTTP status codes.
- **RESTful Endpoints:** CRUD operations on users, accounts, and transactions.
- **Data Integrity:** Enforced foreign key constraints and balance checks in transactions.

## Installation & Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/revobank-api.git
   cd revobank-api
   ```

2. **Create a Virtual Environment and Install Dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**

   Create a `.env` file or set your environment variables as needed:

   ```bash
   export DB_USER=<your_db_user>
   export DB_PASSWORD=<your_db_password>
   export DB_HOST=<your_db_host>
   export DB_NAME=revobank
   export DATABASE_URL="mysql+mysqldb://<your_db_user>:<your_db_password>@<your_db_host>/revobank?charset=utf8mb4"
   export SECRET_KEY=<your_secret_key>
   ```

4. **Run Migrations:**

   ```bash
   flask db upgrade
   ```

5. **Start the Application:**

   ```bash
   flask run
   ```

## API Documentation

### User Management

#### User Registration

- **Endpoint:** `POST /api/auth/users`
- **Description:** Creates a new user account. Required fields: `username`, `email`, and `password`.
- **Password Requirements:** Minimum 8 characters, one uppercase letter, and one special character (e.g., `!@#$%^&*()`).

**Example (HTTPie):**

```bash
http POST http://localhost:5000/api/auth/users \
  username=user1 \
  email=user1@example.com \
  password=SecurePass123!
```

**Expected Response:**

```json
{
  "message": "User created successfully"
}
```

You can create another user similarly:

```bash
http POST http://localhost:5000/api/auth/users \
  username=user2 \
  email=user2@example.com \
  password=AnotherPass123!
```

#### User Login

- **Endpoint:** `POST /api/auth/login`
- **Description:** Authenticates a user and returns an access token.

**Example (HTTPie for User1):**

```bash
http POST http://localhost:5000/api/auth/login \
  email=user1@example.com \
  password=SecurePass123!
```

**Expected Response (sample):**

```json
{
  "access_token": "<ACCESS_TOKEN>"
}
```

#### Get Current User Details

- **Endpoint:** `GET /api/auth/users/me`
- **Description:** Retrieves the authenticated user’s profile.
- **Header:** `Authorization: Bearer <ACCESS_TOKEN>`

**Example (HTTPie):**

```bash
http GET http://localhost:5000/api/auth/users/me "Authorization: Bearer <ACCESS_TOKEN>"
```

**Expected Response (User1 sample):**

```json
{
  "id": 3,
  "username": "user1",
  "email": "user1@example.com",
  "created_at": "2025-03-10T00:12:07"
}
```

#### Update Current User

- **Endpoint:** `PUT /api/auth/users/me`
- **Description:** Updates the authenticated user’s profile (e.g., email, password).

**Example (Update Email):**

```bash
http PUT http://localhost:5000/api/auth/users/me \
  "Authorization: Bearer <ACCESS_TOKEN>" \
  email=newuser1@gmail.com
```

**Expected Response:**

```json
{
  "message": "User updated successfully"
}
```

#### Delete Current User

- **Endpoint:** `DELETE /api/auth/users/me`
- **Description:** Deletes the authenticated user’s account if no active accounts exist.

**Example (HTTPie):**

```bash
http DELETE http://localhost:5000/api/auth/users/me "Authorization: Bearer <ACCESS_TOKEN>"
```

**Expected Response:**
HTTP 204 No Content.

### Account Management

#### Get All Accounts

- **Endpoint:** `GET /api/accounts`
- **Description:** Retrieves all accounts belonging to the authenticated user.

**Example (HTTPie):**

```bash
http GET http://localhost:5000/api/accounts "Authorization: Bearer <ACCESS_TOKEN>"
```

**Expected Response:**
A JSON array of account objects.

#### Get Single Account

- **Endpoint:** `GET /api/accounts/:id`
- **Description:** Retrieves details for a specific account (requires ownership).

**Example (HTTPie):**

```bash
http GET http://localhost:5000/api/accounts/1 "Authorization: Bearer <ACCESS_TOKEN>"
```

**Expected Response:**
Account details in JSON if the account belongs to the authenticated user.

#### Create New Account

- **Endpoint:** `POST /api/accounts`
- **Description:** Creates a new bank account for the authenticated user.
- **Required Fields:** `account_type` (must be one of `savings`, `checking`, or `investment`), and `account_number` (must start with `"ACC-"`).

**Example (HTTPie):**

```bash
http POST http://localhost:5000/api/accounts \
  "Authorization: Bearer <ACCESS_TOKEN>" \
  account_type=savings \
  account_number="ACC-1001"
```

**Expected Response:**
The new account details in JSON with HTTP 201 Created.

#### Update Account

- **Endpoint:** `PUT /api/accounts/:id`
- **Description:** Updates an account’s details (requires ownership).

**Example (HTTPie):**

```bash
http PUT http://localhost:5000/api/accounts/1 \
  "Authorization: Bearer <ACCESS_TOKEN>" \
  account_type=checking \
  account_number="ACC-12345"
```

**Expected Response:**
Updated account details in JSON.

#### Delete Account

- **Endpoint:** `DELETE /api/accounts/:id`
- **Description:** Deletes an account (requires ownership). Note that the account balance must be zero.

**Example (HTTPie):**

```bash
http DELETE http://localhost:5000/api/accounts/1 \
  "Authorization: Bearer <ACCESS_TOKEN>"
```

**Expected Response:**
HTTP 204 No Content on success.

### Transaction Management

#### Get All Transactions

- **Endpoint:** `GET /api/transactions`
- **Description:** Retrieves all transactions for the authenticated user's accounts. Supports optional filters: `account_id`, `start_date`, and `end_date`.

**Example (HTTPie):**

```bash
http GET http://localhost:5000/api/transactions "Authorization: Bearer <ACCESS_TOKEN>"
```

**Expected Response:**
A JSON array of transaction objects.

#### Get Single Transaction

- **Endpoint:** `GET /api/transactions/:id`
- **Description:** Retrieves details of a specific transaction (requires ownership of a related account).

**Example (HTTPie):**

```bash
http GET http://localhost:5000/api/transactions/1 "Authorization: Bearer <ACCESS_TOKEN>"
```

**Expected Response:**
Transaction details in JSON if authorized.

#### Create Transaction

- **Endpoint:** `POST /api/transactions`
- **Description:** Initiates a new transaction. Transaction types can be `deposit`, `withdrawal`, or `transfer`.
  - For a **deposit**, provide `to_account_id`.
  - For a **withdrawal**, provide `from_account_id`.
  - For a **transfer**, provide both `from_account_id` and `to_account_id`.

**Example (Deposit Transaction using HTTPie):**

```bash
http POST http://localhost:5000/api/transactions \
  "Authorization: Bearer <ACCESS_TOKEN>" \
  type=deposit \
  amount=1000.00 \
  to_account_id=1 \
  description="Initial deposit"
```

**Expected Response:**
Transaction details in JSON with updated account balance.

## Additional Notes

- **JWT Tokens:**
  Tokens are generated using Flask-JWT-Extended. The helper function converts user IDs to strings during token creation.
- **Security & Validation:**
  Endpoints enforce authorization checks to ensure that only resource owners can perform certain actions. Required fields and value formats are validated, and meaningful error messages with appropriate HTTP status codes are returned.
- **Database Migrations:**
  Use `flask db upgrade` to apply schema changes.
- **Type Conversions:**
  For financial calculations, amounts are converted to Decimal to ensure precision.
