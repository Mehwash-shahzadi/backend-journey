"""
OrderItem schemas for order line items.

Schemas:
    - OrderItemCreate: Input schema for creating an order item (used in OrderCreate).
    - OrderItemResponse: Output schema for returning order item data (GET).
"""

from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class OrderItemCreate(BaseModel):
    """
    Schema for creating an order item (used within OrderCreate).

    Attributes:
        product_id: ID of the product to order.
        quantity: Quantity of the product (must be > 0).

    Example:
        >>> item = OrderItemCreate(product_id=1, quantity=2)
    """

    product_id: int = Field(..., gt=0, examples=[1])
    quantity: int = Field(..., gt=0, examples=[2])


class OrderItemResponse(BaseModel):
    """
    Schema for returning order item data in responses.

    Includes a nested product reference with basic product information
    (id, name, price only to avoid over-fetching).

    Attributes:
        id: Unique order item identifier.
        product_id: ID of the ordered product.
        quantity: Quantity ordered.
        price_at_purchase: Price snapshot at purchase time.

    Example:
        >>> item = OrderItemResponse(
        ...     id=1,
        ...     product_id=1,
        ...     quantity=2,
        ...     price_at_purchase=Decimal("999.99")
        ... )
    """

    id: int
    product_id: int
    quantity: int
    price_at_purchase: Decimal

    model_config = ConfigDict(from_attributes=True)