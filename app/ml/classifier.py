from typing import Tuple, Optional
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from app.db.models import Transaction, Category, ClassificationRule


class TransactionClassifier:
    def __init__(self):
        self.rule_based_classifier = RuleBasedClassifier()
        self.ml_classifier = MLClassifier()

    def classify_transaction(
        self, description: str, rules: list[ClassificationRule], categories: list[Category]
    ) -> Tuple[Optional[Category], float]:
        # Try rule-based classification first
        category, confidence = self.rule_based_classifier.classify(description, rules)
        
        # If rule-based classification fails or has low confidence, use ML
        if category is None or confidence < 0.7:
            ml_category, ml_confidence = self.ml_classifier.classify(description, categories)
            if ml_confidence > confidence:
                return ml_category, ml_confidence
        
        return category, confidence


class RuleBasedClassifier:
    def classify(
        self, description: str, rules: list[ClassificationRule]
    ) -> Tuple[Optional[Category], float]:
        # Sort rules by priority
        sorted_rules = sorted(rules, key=lambda x: x.priority, reverse=True)
        
        for rule in sorted_rules:
            if not rule.is_active:
                continue
                
            # Convert pattern to regex
            pattern = re.compile(rule.pattern, re.IGNORECASE)
            if pattern.search(description):
                return rule.category, 1.0
        
        return None, 0.0


class MLClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                stop_words='english'
            )),
            ('classifier', MultinomialNB())
        ])
        self.is_trained = False

    def train(self, transactions: list[Transaction]):
        if not transactions:
            return

        descriptions = [t.description for t in transactions]
        categories = [t.category_id for t in transactions]
        
        self.pipeline.fit(descriptions, categories)
        self.is_trained = True

    def classify(
        self, description: str, categories: list[Category]
    ) -> Tuple[Optional[Category], float]:
        if not self.is_trained:
            return None, 0.0

        # Get prediction probabilities
        probs = self.pipeline.predict_proba([description])[0]
        max_prob_idx = np.argmax(probs)
        max_prob = probs[max_prob_idx]

        # Get category ID from pipeline classes
        category_id = self.pipeline.classes_[max_prob_idx]
        
        # Find corresponding category object
        category = next((c for c in categories if c.id == category_id), None)
        
        return category, float(max_prob) 