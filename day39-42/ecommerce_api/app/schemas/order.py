from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field, ConfigDict

from .order_item import OrderItemCreate, OrderItemResponse


class OrderCreate(BaseModel):
    """
    What the user sends when placing an order.

    Example:
        {"items": [{"product_id": 5, "quantity": 2}]}
    """
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderResponse(BaseModel):
    """
    What we return after creating or fetching an order.
    Includes total, status, and full item list.
    """
    id: int
    user_id: int
    total: Decimal
    status: str          # e.g. "pending", "paid"
    created_at: datetime
    items: List[OrderItemResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)