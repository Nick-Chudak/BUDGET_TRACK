from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func, UniqueConstraint
from .engine import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)                     # From Excel "Date"
    description = Column(String, nullable=False)            # From Excel "Description"
    sub_description = Column(String)                        # From Excel "Sub-description"
    transaction_type = Column(String, nullable=False)       # "Debit" or "Credit"
    amount = Column(Float, nullable=False)                  # Transaction amount
    balance = Column(Float)                                 # Account balance after transaction
    transaction_hash = Column(String(64), unique=True, index=True, nullable=False)
    source_file = Column(String)                            # Optional: file name
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint('transaction_hash', name='uix_transaction_hash'),
    )

class ImportLog(Base):
    __tablename__ = "import_logs"

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    rows_loaded = Column(Integer)
    imported_at = Column(DateTime, server_default=func.now())