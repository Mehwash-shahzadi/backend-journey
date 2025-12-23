from pydantic import BaseModel
from datetime import datetime
from typing import List
from decimal import Decimal


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: Decimal
    created_at: datetime
    items: List[OrderItemOut]