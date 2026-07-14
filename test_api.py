import pytest
from fastapi.testclient import TestClient

from main import app
import db_functions as db

client = TestClient(app)

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_NAME", str(test_db))
    db.create_transaction_table()

def test_create_transaction():
    response = client.post("/transactions",json={
        "description": "Salary",
        "amount" : 10000,
        "kind" : "income"
    }
    )
    assert response.status_code == 201
    assert response.json() == {
        "status": "ok",
        "id": 1
        }

    assert db.get_transaction_by_id(1) == (1, "Salary", 10000.0, "income")

def test_create_transaction_missing_field_returns_422():
    response1 = client.post("/transactions",json={
        "amount" : 10000,
        "kind" : "income"
    }
    )
    response2 = client.post("/transactions",json={
        "description": "Salary",
        "kind" : "income"
    }
    )
    response3 = client.post("/transactions",json={
        "description": "Salary",
        "amount" : 10000,
    }
    )

    assert response1.status_code == 422
    assert response2.status_code == 422
    assert response3.status_code == 422

def test_create_transaction_invalid_business_input_returns_400():
    response1 = client.post("/transactions",json={
        "description": "",
        "amount" : 10000,
        "kind" : "income"
    }
    )
    assert response1.status_code == 400
    assert response1.json()=={"detail":"description must be a non-empty string"}

    response2 = client.post("/transactions",json={
        "description": "Salary",
        "amount" : -1,
        "kind" : "income"
    }
    )
    assert response2.status_code == 400
    assert response2.json()=={"detail":"amount must be a positive number"}

    response3 = client.post("/transactions",json={
        "description": "Salary",
        "amount" : 10000,
        "kind" : "food"
    }
    )
    assert response3.status_code == 400
    assert response3.json()=={"detail":"kind must be either income or expense"}

def test_get_all_transactions():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    response = client.get("/transactions")

    assert response.status_code == 200
    assert response.json() == {
        "status" : "ok",
        "transactions":[
            {"id":1 , "description":"Salary", "amount":5000.0, "kind":"income"},
            {"id":2 , "description":"Rent", "amount":50.0, "kind":"expense"},
            {"id":3 , "description":"Trading", "amount":10000.0, "kind":"income"},
            {"id":4 , "description":"Travels", "amount":150.0, "kind":"expense"}
        ]
    }

def test_get_transactions_by_kind():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    response1 = client.get("/transactions?kind=income")
    response2 = client.get("/transactions?kind=expense")

    assert response1.status_code == 200
    assert response1.json() == {
        "status" : "ok",
        "transactions":[
            {"id":1 , "description":"Salary", "amount":5000.0, "kind":"income"},
            {"id":3 , "description":"Trading", "amount":10000.0, "kind":"income"},
        ]
    }

    assert response2.status_code == 200
    assert response2.json() == {
        "status" : "ok",
        "transactions":[
            {"id":2 , "description":"Rent", "amount":50.0, "kind":"expense"},
            {"id":4 , "description":"Travels", "amount":150.0, "kind":"expense"}
        ]
    }

def test_get_transactions_by_id():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    response = client.get("/transactions/2")

    assert response.status_code == 200
    assert response.json() == {
        "status" : "ok",
        "transaction":{"id":2, "description": "Rent", "amount":50, "kind":"expense"}
    }

def test_get_transaction_missing_id():
    response = client.get("/transactions/1")
    assert response.status_code == 404
    assert response.json() == {"detail":"Transaction not found"}

def test_update_transaction_missing_id():

    response = client.patch("/transactions/1",json={"amount":100})

    assert response.status_code == 404
    assert response.json() == {"detail":"Transaction not found"}

def test_update_transaction_by_id():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    response = client.patch("/transactions/1",json={"amount":100})

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_delete_transaction_missing_id():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    before = db.get_all_transactions()

    response = client.delete("/transactions/99")

    after = db.get_all_transactions()

    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found"}
    assert before == after

def test_delete_transaction_by_id():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    response = client.delete("/transactions/1")

    assert response.status_code == 200
    assert response.json() == {"status":"ok"}
    assert db.get_transaction_by_id(1) == None

def test_get_recent_transactions():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    response = client.get("/transactions/recent",params={"limit":2})

    assert response.status_code == 200
    assert response.json() == {
        "status" : "ok",
        "recent_transactions": [
            {"id":4, "description":"Travels", "amount":150.0, "kind":"expense"},
            {"id":3, "description":"Trading", "amount":10000.0, "kind":"income"}
        ]
    }


def test_get_recent_transactions_limit_is_0_returns_400():
    response = client.get("/transactions/recent",params={"limit":0})
    assert response.status_code == 400

def test_get_recent_transactions_limit_is_abc_returns_422():
    response = client.get("/transactions/recent",params={"limit":"abc"})
    assert response.status_code == 422

def test_static_routes_do_not_get_captured_by_dynamic_routes():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    response1 = client.get("/transactions/count")

    response2 = client.get("/transactions/summary")

    assert response1.status_code == 200
    assert response2.status_code == 200

    assert response2.json() == {
        "status" : "ok",
        "summary":{
        "total_income":15000.0,
        "total_expense":200.0,
        "balance":14800.0
        }
    }

def test_get_transactions_by_kind_other_than_income_or_expense_returns_400():
    response = client.get("/transactions?kind=food")
    assert response.status_code == 400
    assert response.json() == {"detail":"kind must be either income or expense"}

def test_get_transactions_by_id_abc_returns_422():
    response = client.get("/transactions/abc")
    assert response.status_code == 422

def test_update_transactions_by_id_with_negative_amount_returns_400():
    response = client.patch("/transactions/1",json={"amount":-5})
    assert response.status_code == 400

























