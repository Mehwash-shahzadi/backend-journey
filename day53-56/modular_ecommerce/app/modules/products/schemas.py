from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class CategoryOut(BaseModel):
    id: int
    name: str


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    stock: int
    category_name: str | None = None 


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    category: Optional[CategoryOut] = None
    avg_rating: Optional[float] = None
    review_count: int = 0


class ReviewCreate(BaseModel):
    rating: int
    comment: str


class ReviewOut(BaseModel):
    id: int
    user_id: int
    rating: int
    comment: str
    created_at: datetime