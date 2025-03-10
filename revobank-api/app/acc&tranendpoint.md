### **Accounts Endpoints**

#### ✅ **Working Endpoints**

1. **Create Account**  
   **Input:**

   ```bash
   http POST http://localhost:5000/api/accounts \
     Authorization:"Bearer <JWT_TOKEN>" \
     account_type="savings" \
     account_number="ACC-12345"
   ```

   **Output:**

   ```json
   HTTP/1.1 201 CREATED
   {
     "account_number": "ACC-12345",
     "account_type": "savings",
     "balance": "0.00",
     "id": 1,
     "user_id": 5
   }
   ```

2. **Get All Accounts**  
   **Input:**

   ```bash
   http GET http://localhost:5000/api/accounts \
     Authorization:"Bearer <JWT_TOKEN>"
   ```

   **Output:**

   ```json
   HTTP/1.1 200 OK
   [
     {
       "account_number": "ACC-12345",
       "account_type": "checking",
       "balance": "0.00",
       "id": 1,
       "user_id": 5
     }
   ]
   ```

3. **Get Single Account**  
   **Input:**

   ```bash
   http GET http://localhost:5000/api/accounts/1 \
     Authorization:"Bearer <JWT_TOKEN>"
   ```

   **Output:**

   ```json
   HTTP/1.1 200 OK
   {
     "account_number": "ACC-12345",
     "account_type": "checking",
     "balance": "0.00",
     "id": 1,
     "user_id": 5
   }
   ```

4. **Update Account**  
   **Input:**
   ```bash
   http PUT http://localhost:5000/api/accounts/1 \
     Authorization:"Bearer <JWT_TOKEN>" \
     account_type="checking" \
     account_number="ACC-1234567"
   ```
   **Output:**
   ```json
   HTTP/1.1 200 OK
   {
     "account_number": "ACC-1234567",
     "account_type": "checking",
     "balance": "0.00",
     "id": 1,
     "user_id": 5
   }
   ```

### **Transactions Endpoints**

#### ✅ **Working Endpoints**

1. **Deposit**  
   **Input:**

   ```bash
   http POST http://localhost:5000/api/transactions \
     Authorization:"Bearer <JWT_TOKEN>" \
     type="deposit" \
     amount=1000.00 \
     to_account_id=1 \
     description="Initial deposit"
   ```

   **Output:**

   ```json
   HTTP/1.1 201 CREATED
   {
     "amount": "1000.00",
     "type": "deposit",
     "to_account_id": 1,
     "id": 1
   }
   ```

2. **Withdrawal**  
   **Input:**

   ```bash
   http POST http://localhost:5000/api/transactions \
     Authorization:"Bearer <JWT_TOKEN>" \
     type="withdrawal" \
     amount=200.00 \
     from_account_id=1 \
     description="ATM withdrawal"
   ```

   **Output:**

   ```json
   HTTP/1.1 201 CREATED
   {
     "amount": "200.00",
     "type": "withdrawal",
     "from_account_id": 1,
     "id": 2
   }
   ```

3. **Transfer**  
   **Input:**

   ```bash
   http POST http://localhost:5000/api/transactions \
     Authorization:"Bearer <JWT_TOKEN>" \
     type="transfer" \
     amount=300.00 \
     from_account_id=1 \
     to_account_id=2 \
     description="Funds transfer"
   ```

   **Output:**

   ```json
   HTTP/1.1 201 CREATED
   {
     "amount": "300.00",
     "type": "transfer",
     "from_account_id": 1,
     "to_account_id": 2,
     "id": 3
   }
   ```

4. **Get Transaction History**  
   **Input:**
   ```bash
   http GET http://localhost:5000/api/transactions \
     Authorization:"Bearer <JWT_TOKEN>"
   ```
   **Output:**
   ```json
   HTTP/1.1 200 OK
   [
     {
       "amount": "1000.00",
       "type": "deposit",
       "to_account_id": 1,
       "id": 1
     },
     {
       "amount": "200.00",
       "type": "withdrawal",
       "from_account_id": 1,
       "id": 2
     }
   ]
   ```

---

#### ❌ **Issues Found**

1. **Insufficient Funds (400 Error)**  
   **Input:**

   ```bash
   http POST http://localhost:5000/api/transactions \
     Authorization:"Bearer <JWT_TOKEN>" \
     type="withdrawal" \
     amount=100000.00 \
     from_account_id=1
   ```

   **Output:**

   ```json
   HTTP/1.1 400 BAD REQUEST
   {
     "error": "Insufficient funds"
   }
   ```

2. **Invalid Account Number (400 Error)**  
   **Input:**
   ```bash
   http POST http://localhost:5000/api/accounts \
     Authorization:"Bearer <JWT_TOKEN>" \
     account_type="savings" \
     account_number="INVALID-123"
   ```
   **Output:**
   ```json
   HTTP/1.1 400 BAD REQUEST
   {
     "error": "Account numbers must start with 'ACC-'"
   }
   ```

---

### **Summary of Issues to Fix**

| Endpoint               | Issue                         | Error Code | Root Cause                  |
| ---------------------- | ----------------------------- | ---------- | --------------------------- |
| POST /api/accounts     | Invalid account number format | 400        | Missing "ACC-" prefix       |
| POST /api/transactions | Insufficient funds            | 400        | Balance < withdrawal amount |
