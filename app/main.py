from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from app.core.config import settings
from app.db.session import get_db
from app.db.models import User, Transaction, Category
from app.services.transaction_service import TransactionService
from app.schemas import (
    UserCreate,
    UserResponse,
    TransactionCreate,
    TransactionResponse,
    CategoryCreate,
    CategoryResponse
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
def get_current_user(db: Session = Depends(get_db)):
    # TODO: Implement JWT authentication
    pass

# Routes
@app.post(f"{settings.API_V1_STR}/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: Implement user creation with password hashing
    pass

@app.get(f"{settings.API_V1_STR}/users/me/", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post(f"{settings.API_V1_STR}/transactions/import/")
def import_transactions(
    file_path: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    try:
        transactions = service.import_from_excel(file_path, current_user.id)
        return {"message": f"Successfully imported {len(transactions)} transactions"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get(f"{settings.API_V1_STR}/transactions/", response_model=List[TransactionResponse])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_user_transactions(current_user.id)[skip:skip + limit]

@app.post(f"{settings.API_V1_STR}/categories/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_category = Category(**category.dict(), user_id=current_user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get(f"{settings.API_V1_STR}/categories/", response_model=List[CategoryResponse])
def read_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Category).filter(Category.user_id == current_user.id).all()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 