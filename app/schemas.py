from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    date: datetime
    description: str
    amount: float
    category_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    is_classified: bool
    classification_confidence: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class ClassificationRuleBase(BaseModel):
    pattern: str
    category_id: int
    priority: int = 0
    is_active: bool = True


class ClassificationRuleCreate(ClassificationRuleBase):
    pass


class ClassificationRuleResponse(ClassificationRuleBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 