from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import db_functions as db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_transaction_table()
    yield


app = FastAPI(lifespan=lifespan)

class TransactionInput(BaseModel):
    description: str
    amount: int | float
    kind: str

class AmountUpdate(BaseModel):
    amount: int | float

def raise_bad_request(error):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error)
    )


def raise_transaction_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Transaction not found"
    )

def transaction_row_to_dict(row):
    return {
        "id": row[0],
        "description": row[1],
        "amount": row[2],
        "kind": row[3]
    }

@app.get("/")
def home():
    return{"message":"Budget ledger checkpoint"}

@app.post("/transactions",status_code=201)
def create_transaction(input: TransactionInput):
    try:
        new_id = db.add_transaction(
            input.description,
            input.amount,
            input.kind
        )

    except ValueError as error:
        raise_bad_request(error)

    return {
        "status": "ok",
        "id": new_id
        }

@app.get("/transactions")
def get_transaction(kind : str | None = None):
    try:

        if kind is None:
            rows = db.get_all_transactions()
        else:
            rows = db.get_transaction_by_kind(kind)
    
    except ValueError as error:
        raise_bad_request(error)

    transactions = []

    for row in rows:
        transactions.append(transaction_row_to_dict(row))

    return {
        "status" : "ok",
        "transactions": transactions
    }
    
@app.get("/transactions/count")
def get_transaction_count():
    return{
        "status" : "ok",
        "count" : db.get_transaction_count()
    }

@app.get("/transactions/summary")
def get_transactions_summary():
    summary = db.get_summary()
    return{
        "status" : "ok",
        "summary":{
        "total_income":summary["income_total"],
        "total_expense":summary["expense_total"],
        "balance":summary["balance"]
        }
    }

@app.get("/transactions/recent")
def get_recent_transactions(limit:int = 5):
    try:
        rows = db.get_recent_transactions(limit)
    except ValueError as error:
        raise_bad_request(error)

    transactions = []

    for row in rows:
        transactions.append(transaction_row_to_dict(row))
    
    return {
        "status" : "ok",
        "recent_transactions": transactions
    }

@app.get("/transactions/{transaction_id}")
def get_transaction_by_transaction_id(transaction_id:int):
    try:
        row = db.get_transaction_by_id(transaction_id)

    except ValueError as error:
        raise_bad_request(error)

    if row is None:
        raise_transaction_not_found()

    return{
        "status":"ok",
        "transaction": transaction_row_to_dict(row)
    }

@app.patch("/transactions/{transaction_id}")
def update_transaction_by_id(transaction_id:int, new_amount:AmountUpdate):
    try:
        affected_row = db.update_transaction_by_id(transaction_id, new_amount.amount)
    except ValueError as error:
        raise_bad_request(error)

    if affected_row == 0:
        raise_transaction_not_found()

    return{
        "status": "ok"
    }

@app.delete("/transactions/{transaction_id}")
def delete_transaction_by_id(transaction_id:int):
    try:
        affected_row = db.delete_transaction_by_id(transaction_id)
    except ValueError as error:
        raise_bad_request(error)

    if affected_row == 0:
        raise_transaction_not_found()

    return{
        "status": "ok"
    }






