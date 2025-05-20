from typing import List, Optional
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models import Transaction, Category, User
from app.ml.classifier import TransactionClassifier


class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.classifier = TransactionClassifier()

    def import_from_excel(self, file_path: str, user_id: int) -> List[Transaction]:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Validate required columns
        required_columns = ['date', 'description', 'amount']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Excel file must contain columns: {required_columns}")

        # Get user's categories and rules
        categories = self.db.query(Category).filter(Category.user_id == user_id).all()
        rules = self._get_user_rules(user_id)

        # Process each transaction
        transactions = []
        for _, row in df.iterrows():
            transaction = Transaction(
                date=pd.to_datetime(row['date']),
                description=str(row['description']),
                amount=float(row['amount']),
                user_id=user_id
            )

            # Classify transaction
            category, confidence = self.classifier.classify_transaction(
                transaction.description,
                rules,
                categories
            )

            if category:
                transaction.category_id = category.id
                transaction.is_classified = True
                transaction.classification_confidence = confidence

            transactions.append(transaction)

        # Save to database
        self.db.add_all(transactions)
        self.db.commit()

        return transactions

    def _get_user_rules(self, user_id: int) -> List[dict]:
        # Get all active rules for the user
        rules = self.db.query(ClassificationRule).filter(
            ClassificationRule.user_id == user_id,
            ClassificationRule.is_active == True
        ).all()
        return rules

    def get_user_transactions(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category_id: Optional[int] = None
    ) -> List[Transaction]:
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)

        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)

        return query.order_by(Transaction.date.desc()).all()

    def update_transaction_category(
        self, transaction_id: int, category_id: int, user_id: int
    ) -> Optional[Transaction]:
        transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()

        if transaction:
            transaction.category_id = category_id
            transaction.is_classified = True
            transaction.classification_confidence = 1.0
            self.db.commit()

        return transaction 