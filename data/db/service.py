import hashlib
import pandas as pd
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session as SessionType
from .engine import Session
from .models import Transaction, ImportLog

# Generate hash for deduplication
def generate_transaction_hash(date, amount, description, sub_description):
    raw = f"{date}_{amount}_{description}_{sub_description}".strip().lower()
    return hashlib.sha256(raw.encode()).hexdigest()

# Insert single transaction (if not exists)
def insert_transaction(date, amount, description, sub_description, transaction_type, balance, source_file=None):
    session: SessionType = Session()
    txn_hash = generate_transaction_hash(date, amount, description, sub_description)

    exists = session.query(Transaction).filter_by(transaction_hash=txn_hash).first()
    if not exists:
        txn = Transaction(
            date=date,
            amount=amount,
            description=description,
            sub_description=sub_description,
            transaction_type=transaction_type,
            balance=balance,
            transaction_hash=txn_hash,
            source_file=source_file
        )
        session.add(txn)
        session.commit()
        print(f"Inserted transaction: {description} - {amount}")
    else:
        print("Duplicate transaction skipped.")
    session.close()

# Bulk insert new transactions using conflict handling
def bulk_insert_transactions(df: pd.DataFrame, source_file: str = None):
    session: SessionType = Session()

    required_columns = {'date', 'amount', 'description', 'sub_description', 'transaction_type', 'balance'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing columns: {required_columns - set(df.columns)}")

    df['transaction_hash'] = df.apply(
        lambda row: generate_transaction_hash(
            row['date'], row['amount'], row['description'], row['sub_description']
        ), axis=1
    )
    df['source_file'] = source_file
    rows = df.to_dict(orient="records")

    stmt = sqlite_insert(Transaction).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=['transaction_hash'])

    result = session.execute(stmt)
    session.commit()
    session.close()

    inserted_count = result.rowcount if result.rowcount is not None else 0
    print(f"Inserted {inserted_count} new transactions.")

    if source_file:
        log_import(file_name=source_file, rows_loaded=inserted_count)

# Log each import
def log_import(file_name: str, rows_loaded: int):
    session: SessionType = Session()
    log = ImportLog(file_name=file_name, rows_loaded=rows_loaded)
    session.add(log)
    session.commit()
    session.close()
