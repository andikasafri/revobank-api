Below is a sample README file that documents the user and authentication endpoints based on your output and code. You can copy and adjust this as needed.

---

# Revobank API - User & Authentication

This API provides endpoints for user registration, login, profile retrieval, updates, and deletion in the Revobank application.

## Table of Contents

- [User Registration](#user-registration)
- [User Login](#user-login)
- [Get Current User Details](#get-current-user-details)
- [Update Current User](#update-current-user)
- [Delete Current User](#delete-current-user)
- [Models & Implementation Details](#models--implementation-details)
- [Notes](#notes)

## User Registration

**Endpoint:**  
`POST /api/auth/users`

**Description:**  
Creates a new user account. The endpoint requires a `username`, `email`, and `password`. The password must be at least 8 characters long and include at least one uppercase letter and one special character (e.g., `!@#$%^&*()`).

**Example Command (HTTPie):**

```bash
http POST http://localhost:5000/api/auth/users username=user1 email=user1@example.com password=SecurePass123!
```

**Expected Response:**

```json
{
  "message": "User created successfully"
}
```

You can also create another user:

```bash
http POST http://localhost:5000/api/auth/users username=user2 email=user2@example.com password=AnotherPass123!
```

**Expected Response:**

```json
{
  "message": "User created successfully"
}
```

## User Login

**Endpoint:**  
`POST /api/auth/login`

**Description:**  
Authenticates a user using their email and password. On success, returns an access token that must be used to authenticate subsequent requests.

**Example Command for User1:**

```bash
http POST http://localhost:5000/api/auth/login email=user1@example.com password=SecurePass123!
```

**Expected Response (sample):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTU0MDQ4MSwianRpIjoiZTU4NmI0NjQtMWI0NS00Y2Y5LTkyYzEtMjU2MmViMjdkZjRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNzQxNTQwNDgxLCJjc3JmIjoiYmIyOGMyN2YtZjMxNi00MWMzLTgwN2YtZDVmNTg2ZWQ0YjgwIiwiZXhwIjoxNzQxNTQxMzgxfQ.i87_-HyGtK3yywxcYedqmUegQz1rPuwyNsQ1HnzTjX8"
}
```

For User2, run:

```bash
http POST http://localhost:5000/api/auth/login email=user2@example.com password=AnotherPass123!
```

**Expected Response (sample):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTU0MDUxNiwianRpIjoiNjBmNzA0MWItNzBiMi00YTNkLTk2MTAtZDAzYTcyMmI0MDU4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNzQxNTQwNTE2LCJjc3JmIjoiMGM4ZTIzMGMtNmU4YS00M2ZlLWEwZWMtYWY1Mjg0NzRmOTQyIiwiZXhwIjoxNzQxNTQxNDE2fQ.4DMfXXgQ9hLNMeOW1PXySw403YjFOy3KNfiha0h8YuE"
}
```

## Get Current User Details

**Endpoint:**  
`GET /api/auth/users/me`

**Description:**  
Retrieves the authenticated user’s profile information. You must include a valid access token in the `Authorization` header.

**Required Header:**  
`Authorization: Bearer <access_token>`

**Example Command (HTTPie):**

```bash
http GET http://localhost:5000/api/auth/users/me "Authorization: Bearer <TOKEN>"
```

**Expected Response for User1 (sample):**

```json
{
  "id": 3,
  "username": "user1",
  "email": "user1@example.com",
  "created_at": "2025-03-10T00:12:07"
}
```

**Expected Response for User2 (sample):**

```json
{
  "id": 4,
  "username": "user2",
  "email": "user2@example.com",
  "created_at": "2025-03-10T00:13:24"
}
```

## Update Current User

**Endpoint:**  
`PUT /api/auth/users/me`

**Description:**  
Updates the authenticated user’s profile information. You can update the `email` or `password`. A valid access token is required in the header.

**Required Header:**  
`Authorization: Bearer <access_token>`

**Example Command to Update Email:**

```bash
http PUT http://localhost:5000/api/auth/users/me "Authorization: Bearer <TOKEN>" email=newuser1@gmail.com
```

**Response:**

```json
{
  "message": "User updated successfully"
}
```

**Example Command to Update Password:**

```bash
http PUT http://localhost:5000/api/auth/users/me "Authorization: Bearer <TOKEN>" password=UpdatedPass123!
```

**Response:**

```json
{
  "message": "User updated successfully"
}
```

## Delete Current User

**Endpoint:**  
`DELETE /api/auth/users/me`

**Description:**  
Deletes the authenticated user’s account. Note that the deletion will only succeed if the user does not have active accounts associated with them.

**Required Header:**  
`Authorization: Bearer <access_token>`

**Example Command (HTTPie):**

```bash
http DELETE http://localhost:5000/api/auth/users/me "Authorization: Bearer <TOKEN>"
```

**Expected Response:**  
HTTP status code 204 No Content (with no response body).

## Models & Implementation Details

### User Model (models/user.py)

- **id:** Integer, Primary Key
- **username:** String (unique, not null)
- **email:** String (unique, not null)
- **password_hash:** String (not null)
- **created_at:** DateTime, defaults to the current timestamp
- **updated_at:** DateTime, auto-updates on changes
- **accounts:** Relationship to the `Account` model (with cascade delete)

The model includes methods to set and validate passwords. The password requirements are:

- Minimum 8 characters.
- At least one uppercase letter.
- At least one special character (e.g., `!@#$%^&*()`).

### Router (router/auth.py)

The authentication-related endpoints are implemented in the `router/auth.py` file, including:

- **Register:** `POST /api/auth/users`
- **Login:** `POST /api/auth/login`
- **Get Current User:** `GET /api/auth/users/me`
- **Update Current User:** `PUT /api/auth/users/me`
- **Delete Current User:** `DELETE /api/auth/users/me`

Error handling is included for missing required fields, duplicate entries, and unauthorized access.

## Notes

- **JWT Tokens:**  
  Tokens are generated using Flask-JWT-Extended. The `generate_token` helper ensures the user ID is converted to a string (i.e., `create_access_token(identity=str(user_id))`) so that the JWT’s subject claim meets expected requirements.

- **Security:**  
  Registration and login validate that required fields are provided. Passwords must meet complexity rules.

- **Account Deletion:**  
  Users with active accounts (as defined by the associated `Account` relationship) cannot be deleted.

- **Testing:**  
  Use HTTPie (or a similar tool) with the provided commands to interact with the API endpoints.
