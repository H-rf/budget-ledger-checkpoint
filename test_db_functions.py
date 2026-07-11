import db_functions as db
import pytest

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_NAME", str(test_db))
    db.create_transaction_table()

def test_add_valid_transaciton():
    Salary_id = db.add_transaction("Salary", 5000, "Income")
    Rent_id = db.add_transaction("Rent", 50, " expense")

    assert Salary_id == 1
    assert Rent_id == 2

def test_add_transaction_invalid_description():
    with pytest.raises(ValueError, match="description must be a non-empty string"):
        db.add_transaction("", 5000, "income")
    with pytest.raises(ValueError, match="description must be a non-empty string"):    
        db.add_transaction(1, 5000, "income")

def test_add_transaction_invalid_amount():
    with pytest.raises(ValueError, match="amount must be a positive number"):
        db.add_transaction("Salary", "5000", "income")
def test_add_transaction_invalid_kind():
    with pytest.raises(ValueError,match="kind must be either income or expense"):
        db.add_transaction("Salary", 5000, "money")

def test_get_all_transaction(): 
    db.add_transaction("Salary", 5000, "Income")
    db.add_transaction("Rent", 50, " expense")

    rows = db.get_all_transactions()

    assert rows == [(1, "Salary", 5000.0, "income"),(2, "Rent", 50, "expense")]

def test_get_transaction_by_kind():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")
    
    rows = db.get_transaction_by_kind("income")

    assert rows == [(1, "Salary", 5000, "income"),(3, "Trading", 10000, "income")]

def test_get_transaction_by_invalid_kind():
    with pytest.raises(ValueError,match="kind must be either income or expense"):
        db.get_transaction_by_kind("food")

def test_get_transaction_by_id():
    Salary_id = db.add_transaction("Salary", 5000, "Income")
    Rent_id = db.add_transaction("Rent", 50, " expense")

    assert db.get_transaction_by_id(Salary_id) == (Salary_id, "Salary", 5000.0, "income")
    assert db.get_transaction_by_id(Rent_id) == (Rent_id, "Rent", 50.0, "expense")
    assert db.get_transaction_by_id(3) == None

def test_get_transaction_by_invalid_id():
    with pytest.raises(ValueError,match="transaction_id must be positive number"):
        db.get_transaction_by_id("1")

def test_update_transaction_by_id():
    Salary_id = db.add_transaction("Salary", 5000, "income")
    Rent_id = db.add_transaction("Rent", 50, "expense")

    affected_rows = db.update_transaction_by_id(Salary_id, 8000)

    assert affected_rows == 1

    assert db.get_transaction_by_id(Salary_id) == (Salary_id, "Salary", 8000, "income")
    assert db.get_transaction_by_id(Rent_id) == (Rent_id, "Rent", 50, "expense")

def test_update_transaction_by_missing_id():
    Salary_id = db.add_transaction("Salary", 5000, "income")
    Rent_id = db.add_transaction("Rent", 50, "expense")

    affected_rows = db.update_transaction_by_id(3, 8000)

    assert affected_rows == 0

    assert db.get_transaction_by_id(Salary_id) == (Salary_id, "Salary", 5000, "income")
    assert db.get_transaction_by_id(Rent_id) == (Rent_id, "Rent", 50, "expense")

def test_delete_transaction_by_id():
    Salary_id = db.add_transaction("Salary", 5000, "income")
    Rent_id = db.add_transaction("Rent", 50, "expense")

    affected_rows = db.delete_transaction_by_id(Salary_id)

    assert affected_rows == 1

    assert db.get_all_transactions() == [(Rent_id, "Rent", 50, "expense")]


def test_delete_transaction_by_missing_id():
    Salary_id = db.add_transaction("Salary", 5000, "income")
    Rent_id = db.add_transaction("Rent", 50, "expense")
    
    before = db.get_all_transactions()

    affected_rows = db.delete_transaction_by_id(3)

    after = db.get_all_transactions()

    assert affected_rows == 0

    assert before == after

def test_get_recent_transactions():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    rows = db.get_recent_transactions(3)

    assert rows == [(4, "Travels", 150, "expense"),(3, "Trading", 10000, "income"),(2, "Rent", 50, "expense")]

def test_get_recent_limit_surpasses_len_list_returns_all_rows():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    assert db.get_recent_transactions(99) == [(4, "Travels", 150, "expense"),(3, "Trading", 10000, "income"),(2, "Rent", 50, "expense"),(1, "Salary", 5000, "income")]

def test_get_recent_invalid_limit():
    with pytest.raises(ValueError,match="limit must be a positive number"):
        db.get_recent_transactions(-1)

def test_get_transaction_count():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")


    count = db.get_transaction_count()

    assert count == 4

def test_get_summary():
    db.add_transaction("Salary", 5000, "income")
    db.add_transaction("Rent", 50, "expense")
    db.add_transaction("Trading", 10000, "income")
    db.add_transaction("Travels", 150, "expense")

    assert db.get_summary() == {
        "income_total" : 15000,
        "expense_total" : 200,
        "balance" : 14800
    }













 









