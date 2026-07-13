# Budget Ledger API Checkpoint

A small backend API for tracking income and expense transactions.

This project is an independent rebuild checkpoint using **FastAPI**, **SQLite**, and **pytest**. It stores transactions in a local SQLite database and exposes API routes for creating, reading, filtering, updating, deleting, counting, summarizing, and listing recent transactions.

## Purpose

The goal of this project is to practice backend fundamentals:

- separating API logic from database logic
- validating user input
- using SQLite safely with parameterized queries
- converting raw database rows into JSON responses
- writing DB tests and API tests
- understanding status codes such as 200, 201, 400, 404, and 422

## Tech Stack

- Python
- FastAPI
- SQLite
- pytest
- FastAPI TestClient
- Uvicorn

## Project Structure

```text
.
├── db_functions.py
├── main.py
├── test_db_functions.py
├── test_api.py
├── .gitignore
└── README.md


File Overview



db_functions.py

Contains the database layer.
Responsibilities:
defines the SQLite database name
creates the transactions table
validates business rules
inserts transactions
reads transactions
filters by kind
updates transaction amounts
deletes transactions
returns recent transactions
returns transaction count
calculates income, expense, and balance summary
The database functions return raw Python values such as tuples, lists, integers, dictionaries, or None.

main.py

Contains the FastAPI application.
Responsibilities:
defines the FastAPI app
defines Pydantic request models
defines API routes
converts database rows into JSON-ready dictionaries
converts business validation errors into HTTP 400 responses
converts missing resources into HTTP 404 responses
returns JSON responses to the client

test_db_functions.py

Tests the database layer directly.
These tests check:
temporary test database isolation
valid transaction insertion
invalid description, amount, and kind validation
listing transactions
filtering by kind
getting transactions by ID
updating transactions
deleting transactions
recent transaction ordering
invalid recent limits
transaction count
income/expense/balance summary

test_api.py

Tests the API layer through FastAPI TestClient.
These tests check:
successful transaction creation
missing required fields returning 422
invalid business input returning 400
listing transactions as JSON
filtering transactions by kind
getting a transaction by ID
missing IDs returning 404
updating a transaction
deleting a transaction
recent transactions with query parameters
invalid recent limits
static routes not being captured by dynamic ID routes

.gitignore

Prevents runtime and generated files from being committed, including:
SQLite database files
virtual environment folders
Python cache folders
pytest cache folders


Transaction Model

Each transaction has:
Field	      Type	          Rule
id	         integer	    primary key
description	 text	        required, non-empty
amount	     real number	required, positive, not bool
kind	     text	        must be income or expense

API Endpoints

Home

GET /
Returns a simple welcome message.

Create Transaction
POST /transactions
Example body:
{
  "description": "Salary",
  "amount": 5000,
  "kind": "income"
}
Success response:
{
  "status": "ok",
  "id": 1
}
List Transactions
GET /transactions
Returns all transactions.

Filter Transactions by Kind

GET /transactions?kind=income
GET /transactions?kind=expense
Returns only transactions matching the selected kind.

Get Transaction by ID

GET /transactions/{transaction_id}
Example:
GET /transactions/1
Update Transaction Amount
PATCH /transactions/{transaction_id}
Example body:
{
  "amount": 8000
}

Delete Transaction

DELETE /transactions/{transaction_id}
Deletes a transaction by ID.
Count Transactions
GET /transactions/count
Returns the number of stored transactions.

Summary
GET /transactions/summary
Returns total income, total expense, and balance.
Recent Transactions
GET /transactions/recent?limit=2
Returns the newest transactions first.

Status Codes

Status Code	Meaning
200	Request succeeded
201	Transaction created
400	Business validation failed
404	Transaction ID was valid but not found
422	FastAPI/Pydantic rejected the request shape or type

Examples:

Missing required JSON field → 422
amount <= 0 → 400
kind = "food" → 400
transaction_id = abc → 422
valid but missing transaction ID → 404
limit = 0 → 400
limit = abc → 422
How to Run the API

Install dependencies:
pip install fastapi uvicorn pytest

Run the server:
uvicorn main:app --reload

Open the interactive API docs:
http://127.0.0.1:8000/docs

How to Run Tests
Run all tests:
python -m pytest -q

Expected result:
33 passed

Manual Smoke Test Summary

Manual smoke testing can be done through /docs.
Recommended checks:
Create an income transaction.
Create an expense transaction.
List all transactions.
Filter transactions by income and expense.
Get one transaction by ID.
Update one transaction amount.
Check the updated transaction.
Delete one transaction.
Confirm the deleted transaction returns 404.
Check /transactions/count.
Check /transactions/summary.
Check /transactions/recent?limit=2.

Request Flow

A client sends an HTTP request to FastAPI. FastAPI matches the route and uses Pydantic to extract and validate path, query, or body data. The route function then calls db_functions.py, where business validation and SQLite operations happen. SQLite returns rows, counts, or affected-row results. The API layer converts those raw database results into JSON responses and sends them back to the client.

Known Limitations

This is a local learning project, not a production accounting system.
There is no authentication.
There is no pagination.
The database is local SQLite.
The project focuses on backend fundamentals, not frontend UI.