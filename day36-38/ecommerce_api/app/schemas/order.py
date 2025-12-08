from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from .order_item import OrderItemCreate, OrderItemResponse


class OrderCreate(BaseModel):
    """
    Schema for creating a new order.

    User ID is assumed from the authenticated request context (dependency injection).

    Attributes:
        items: List of order items to include in the order.

    """

    items: list[OrderItemCreate] = Field(
        ...,
        min_length=1,
        examples=[
            [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 1},
            ]
        ],
    )


class OrderResponse(BaseModel):
    """
    Schema for returning order data with nested order items.

    Attributes:
        id: Unique order identifier.
        user_id: ID of the user who placed the order.
        total: Total order amount.
        status: Order status (pending, paid, shipped, delivered, cancelled).
        created_at: Timestamp of order creation.
        items: List of order items in the order.
    """

    id: int
    user_id: int
    total: Decimal
    status: str
    created_at: datetime
    items: list[OrderItemResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)