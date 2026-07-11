import sqlite3

DB_NAME = "budget.db"


def create_transaction_table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY,
    description TEXT,
    amount REAL,
    kind TEXT
    )
    """)
    connection.commit()
    connection.close()


def validate_transaction_id(transaction_id):
    if not isinstance(transaction_id, int) or isinstance(transaction_id, bool) or transaction_id <=0:
        raise ValueError("transaction_id must be positive number")

def validate_description(description):
    if not isinstance(description, str) or description.strip()=="":
        raise ValueError("description must be a non-empty string")
    
    description = description.strip()
    return description

def validate_amount(amount):
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("amount must be a positive number")

def validate_kind(kind):
    if not isinstance(kind, str):
        raise ValueError("kind must be either income or expense")
    
    kind = kind.strip().lower()
    if kind not in ("income", "expense"):
        raise ValueError("kind must be either income or expense")
    
    return kind

def validate_limit(limit):
    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("limit must be a positive number")


def add_transaction(description, amount, kind):
    description = validate_description(description)
    validate_amount(amount)
    kind  = validate_kind(kind)

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO transactions (description, amount, kind) 
    VALUES (?, ? , ?)""",
    (description, amount, kind))
    new_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return new_id

def get_all_transactions():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM transactions ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_transaction_by_kind(kind):
    kind = validate_kind(kind)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM transactions WHERE kind = ? ORDER BY id
    """,
    (kind,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_transaction_by_id(transaction_id):
    validate_transaction_id(transaction_id)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM transactions WHERE id = ?
    """,
    (transaction_id,)
    )

    row = cursor.fetchone()

    connection.close()

    return row

def update_transaction_by_id(transaction_id, new_amount):
    validate_transaction_id(transaction_id)
    validate_amount(new_amount)

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE transactions SET amount = ? WHERE id = ?
    """,
    (new_amount, transaction_id))

    affected_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return affected_rows

def delete_transaction_by_id(transaction_id):
    validate_transaction_id(transaction_id)

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM transactions WHERE id = ?
    """,
    (transaction_id,)
    )

    affected_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return affected_rows

def get_recent_transactions(limit):
    validate_limit(limit)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT ?",(limit,))

    recent_rows = cursor.fetchall()

    connection.close()

    return recent_rows

def get_transaction_count():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_summary():
    income_total = 0
    expense_total = 0

    income_transactions = get_transaction_by_kind("income")
    for transaction in income_transactions:
        income_total += transaction[2]
    expense_transactions = get_transaction_by_kind("expense")    
    for transaction in expense_transactions:
        expense_total += transaction[2]

    balance = income_total - expense_total

    return {
        "income_total" : income_total,
        "expense_total" : expense_total,
        "balance" : balance
    }

        










