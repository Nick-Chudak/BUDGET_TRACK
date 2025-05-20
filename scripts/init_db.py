from sqlalchemy import create_engine
from app.core.config import settings
from app.db.base_class import Base
from app.db.models import User, Category, Transaction, ClassificationRule


def init_db():
    engine = create_engine(settings.get_database_url)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db() 