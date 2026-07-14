Yes. Here is a cleaner, more professional README you can paste over the current one.

```markdown
# Budget Ledger API Checkpoint

A small backend API for tracking income and expense transactions.

This project is an independent backend rebuild checkpoint using **FastAPI**, **SQLite**, and **pytest**. It stores transactions in a local SQLite database and exposes routes for creating, reading, filtering, updating, deleting, counting, summarizing, and listing recent transactions.

---

## Purpose

The goal of this project is to practice core backend fundamentals:

- separating API logic from database logic
- validating user input
- using SQLite with parameterized SQL queries
- converting raw database rows into JSON responses
- writing direct database tests
- writing API tests through `TestClient`
- understanding common HTTP status codes: `200`, `201`, `400`, `404`, and `422`

---

## Tech Stack

- **Python**
- **FastAPI**
- **SQLite**
- **pytest**
- **FastAPI TestClient**
- **Uvicorn**

---

## Project Structure

```text
.
├── db_functions.py
├── main.py
├── test_db_functions.py
├── test_api.py
├── README.md
└── .gitignore
```

---

## File Overview

### `db_functions.py`

Contains the database layer.

Responsibilities:

- defines the SQLite database name
- creates the `transactions` table
- validates business rules
- inserts transactions
- reads transactions
- filters transactions by kind
- updates transaction amounts
- deletes transactions
- returns recent transactions
- returns transaction count
- calculates income, expense, and balance summary

The database layer returns raw Python values such as tuples, lists, integers, dictionaries, or `None`.

### `main.py`

Contains the FastAPI application.

Responsibilities:

- defines the FastAPI app
- defines Pydantic request models
- defines API routes
- converts raw database rows into JSON-ready dictionaries
- converts business validation errors into HTTP `400` responses
- converts missing resources into HTTP `404` responses
- returns JSON responses to the client

### `test_db_functions.py`

Tests the database layer directly.

These tests check:

- temporary test database isolation
- valid transaction insertion
- invalid description, amount, and kind validation
- listing transactions
- filtering by kind
- getting transactions by ID
- updating transactions
- deleting transactions
- recent transaction ordering
- invalid recent limits
- transaction count
- income, expense, and balance summary

### `test_api.py`

Tests the API layer through FastAPI `TestClient`.

These tests check:

- successful transaction creation
- missing required fields returning `422`
- invalid business input returning `400`
- listing transactions as JSON
- filtering transactions by kind
- getting transactions by ID
- missing IDs returning `404`
- updating transactions
- deleting transactions
- recent transactions with query parameters
- invalid recent limits
- static routes not being captured by dynamic ID routes

### `.gitignore`

Prevents runtime and generated files from being committed, including:

- SQLite database files
- virtual environment folders
- Python cache folders
- pytest cache folders

---

## Transaction Model

Each transaction has the following fields:

| Field | Type | Rule |
|---|---|---|
| `id` | integer | Primary key |
| `description` | text | Required, non-empty |
| `amount` | real number | Required, positive, not bool |
| `kind` | text | Must be `income` or `expense` |

---

## API Endpoints

### Home

```http
GET /
```

Returns a simple welcome message.

Example response:

```json
{
  "message": "Budget ledger checkpoint"
}
```

---

### Create Transaction

```http
POST /transactions
```

Example request body:

```json
{
  "description": "Salary",
  "amount": 5000,
  "kind": "income"
}
```

Example response:

```json
{
  "status": "ok",
  "id": 1
}
```

---

### List Transactions

```http
GET /transactions
```

Returns all transactions.

Example response:

```json
{
  "status": "ok",
  "transactions": [
    {
      "id": 1,
      "description": "Salary",
      "amount": 5000.0,
      "kind": "income"
    }
  ]
}
```

---

### Filter Transactions by Kind

```http
GET /transactions?kind=income
GET /transactions?kind=expense
```

Returns only transactions matching the selected kind.

---

### Get Transaction by ID

```http
GET /transactions/{transaction_id}
```

Example:

```http
GET /transactions/1
```

Example response:

```json
{
  "status": "ok",
  "transaction": {
    "id": 1,
    "description": "Salary",
    "amount": 5000.0,
    "kind": "income"
  }
}
```

---

### Update Transaction Amount

```http
PATCH /transactions/{transaction_id}
```

Example request body:

```json
{
  "amount": 8000
}
```

Example response:

```json
{
  "status": "ok"
}
```

---

### Delete Transaction

```http
DELETE /transactions/{transaction_id}
```

Example response:

```json
{
  "status": "ok"
}
```

---

### Count Transactions

```http
GET /transactions/count
```

Example response:

```json
{
  "status": "ok",
  "count": 3
}
```

---

### Summary

```http
GET /transactions/summary
```

Returns total income, total expense, and balance.

Example response:

```json
{
  "status": "ok",
  "summary": {
    "total_income": 15000.0,
    "total_expense": 200.0,
    "balance": 14800.0
  }
}
```

---

### Recent Transactions

```http
GET /transactions/recent?limit=2
```

Returns the newest transactions first.

Example response:

```json
{
  "status": "ok",
  "recent_transactions": [
    {
      "id": 4,
      "description": "Travels",
      "amount": 150.0,
      "kind": "expense"
    },
    {
      "id": 3,
      "description": "Trading",
      "amount": 10000.0,
      "kind": "income"
    }
  ]
}
```

---

## Status Codes

| Status Code | Meaning |
|---|---|
| `200` | Request succeeded |
| `201` | Transaction created |
| `400` | Business validation failed |
| `404` | Transaction ID was valid but not found |
| `422` | FastAPI/Pydantic rejected the request shape or type |

Examples:

| Input/problem | Expected status |
|---|---|
| Missing required JSON field | `422` |
| `amount <= 0` | `400` |
| `kind = "food"` | `400` |
| `transaction_id = abc` | `422` |
| valid but missing transaction ID | `404` |
| `limit = 0` | `400` |
| `limit = abc` | `422` |

---

## Request Flow

```text
Client/TestClient/browser
→ FastAPI route matching
→ Pydantic extracts and validates path/query/body values
→ route function calls db_functions.py
→ db_functions.py validates business rules and talks to SQLite
→ SQLite returns rows, counts, or affected-row results
→ route converts raw DB results into JSON-ready responses
→ client receives JSON response
```

---

## How to Run the API

Install dependencies:

```powershell
pip install fastapi uvicorn pytest
```

Run the server:

```powershell
uvicorn main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

---

## How to Run Tests

Run all tests:

```powershell
python -m pytest -q
```

Expected result:

```text
36 passed
```

---

## Manual Smoke Test

Manual smoke testing was completed through `/docs`.

Checked:

- created an income transaction
- created an expense transaction
- listed all transactions
- filtered transactions by `income`
- filtered transactions by `expense`
- got a transaction by ID
- updated a transaction amount
- checked the updated transaction
- deleted a transaction
- confirmed the deleted transaction returned `404`
- checked `/transactions/count`
- checked `/transactions/summary`
- checked `/transactions/recent?limit=2`

---

## Known Limitations

- This is a local learning project, not a production accounting system.
- There is no authentication.
- There is no pagination.
- The database is local SQLite.
- There is no frontend UI.
- The project focuses on backend fundamentals, not production deployment.

---

## Checkpoint Result

Final test result:

```text
36 passed
```

Final Git status:

```text
nothing to commit, working tree clean
```
```

After pasting it, run:

```powershell
python -m pytest -q
git status --short
```

Then commit:

```powershell
git add README.md
git commit -m "polish README documentation"
```