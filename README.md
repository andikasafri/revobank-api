# RevoBank Activity Diagrams Documentation

**Module 6 Assignment | Deadline: 21 February 2025**

---

## Diagram Key / Legend

Before diving into the details, please note the following symbols used in the diagrams:

- **Start Event:** Represented by a filled circle; this marks the beginning of the process.
- **End Event:** Represented by a circle with a thick border; this marks the conclusion of the process.
- **Activity (Rectangle):** Used for actions or steps performed by either the user or the system.
- **Decision (Diamond):** Indicates a point where a choice must be made (e.g., Yes/No), which directs the flow into different branches.

This legend ensures that the diagrams are easy to understand, even if you are not familiar with UML notation.

---

## 1. User Authentication Activity Diagram

**SVG File:**  
![User Authentication Diagram](/Public/userauthentication.svg)

<!-- _User Authentication Diagram - [View Full Size](/public/userauthentication.svg)_ -->

### Diagram Overview

This diagram visualizes the secure login workflow for RevoBank, including error handling, token generation, and password recovery.

### Key Steps & Processes

- **Start Node:** Initiates the authentication process.
- **Input Credentials:**  
  _User enters username/password (User action, Rectangle)._
- **Verify Credentials:**  
  _System checks validity (System action, Rectangle)._
- **Decision: Valid Credentials?** _(Diamond)_
  - **Yes:**
    - **Generate Token:**  
      _System issues a JWT/security token (System, Rectangle)._
    - **Login Successful:**  
      _User gains access (User, Rectangle)._
  - **No:**
    - **Display Error:**  
      _System shows "Invalid Credentials" (System, Rectangle)._
    - **Inform User:**  
      _Additional warning about attempts (System, Rectangle)._
    - **Decision: Exceeded Max Attempts?** _(Diamond)_
      - **Yes:**  
        _Prevent Further Login (System locks account, Rectangle)._
      - **No:**  
        _User chooses Retry or Forgot Password (Decision Diamond)._
        - **Retry:** Loops back to **Input Credentials**.
        - **Forgot Password:**
          - **Enter Last Email:**  
            _User provides recovery email (User, Rectangle)._
          - **Send Recovery Link:**  
            _System emails reset instructions (System, Rectangle)._
          - **Reset Password:**  
            _User creates a new password (System, Rectangle)._
          - **Loop Back:**  
            _User must re-enter credentials for verification (Security compliance)._

### Covered Requirements

- ✅ **Login, Password Verification, Token Generation**
- ✅ **Error Handling:** Invalid credentials, max attempts, recovery flow.
- ✅ **Actors:** User (input actions) and System (verification, security).

---

## 2. Transaction Handling Activity Diagram

**SVG File:**  
![Transaction Handling Diagram](/Public/handletransaction.svg)

<!-- _Transaction Handling Diagram - [View Full Size](/public/handletransaction.svg)_ -->

### Diagram Overview

This diagram maps transaction initiation, balance checks, payment confirmation, and error recovery.

### Key Steps & Processes

- **Start Node:** User begins a transaction.
- **Authenticate User:** _(Decision)_
  - **Yes:**  
    _Proceed to transaction type selection._
  - **No:**
    - **Send Authenticator Email:**  
      _System triggers 2FA (System, Rectangle)._
    - **Verify Authentication:** _(Decision)_
      - **Yes:**  
        _Proceed to Select Transaction Type._
      - **No:**  
        _Retry Authenticator loops back to authentication._
- **Select Transaction Type:**  
  _(User selects the type of transaction, Rectangle)_
  - **Credit Card:**  
    _User inputs card details (Rectangle)._
  - **Virtual Account:**
    - **Choose Bank:**  
      _User selects bank (Rectangle)._
    - **Generate Virtual Account:**  
      _System creates a temporary account (System, Rectangle)._
- **Check Account Balance:** _(Decision)_
  - **Yes:**
    - **Process Transaction:**  
      _Funds transfer (System, Rectangle)._
    - **Update Balance:**  
      _Adjust account (System, Rectangle)._
    - **Record History:**  
      _Log transaction (System, Rectangle)._
    - **Confirm Success:**  
      _User receives confirmation (User, Rectangle)._
  - **No:**
    - **Display Insufficient Funds:**  
      _(System, Rectangle)._
    - **Retry Transaction:**  
      _User adjusts inputs (Loop back to Select Transaction Type)._
- **Check Payment Confirmation:** _(Decision)_
  - **Yes:**  
    _Transaction ends successfully._
  - **No:**
    - **Retry Payment:**  
      _System re-initiates payment (Rectangle)._
    - **Wait Confirmation:**  
      _System pauses for external validation (Rectangle)._
    - **Loop Back:**  
      _Re-checks confirmation status._

### Covered Requirements

- ✅ **Transaction Initiation:** Credit card and virtual account paths.
- ✅ **Verification:** Balance checks, authentication, payment confirmation.
- ✅ **Error Handling:** Insufficient funds, authentication retries.
- ✅ **Actors:** User (selections/inputs) and System (processing/security).

---

## UML Standards Compliance

### Shapes

- **Rectangles:** All actions (e.g., Input Credentials, Generate Token).
- **Diamonds:** Decisions (e.g., Valid Credentials?, Exceeded Max Attempts?).
- **Start/End Nodes:** Clearly labeled.

### Actors

- Differentiated between User (gray) and System (blue) actions.

### Flow Logic

- Loops (e.g., authentication retries) use connectors, not ambiguous jumps.
- All decision paths terminate at an End Node.

---

Activate revobank-api virtual environment: ".\venv\Scripts\activate.ps1"
To go into the Postgresssql "psql -d postgres -U postgres"
