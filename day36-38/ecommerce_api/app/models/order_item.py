"""
OrderItem model.

Represents a line item in an order.
Captures product snapshot (price_at_purchase) at order time.
"""

from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import Base

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderItem(Base):
    """
    OrderItem model.

    Attributes:
        id: Unique identifier (auto-increment).
        order_id: Foreign key to Order (CASCADE on delete).
        product_id: Foreign key to Product (RESTRICT on delete).
        quantity: Item quantity (must be > 0).
        price_at_purchase: Price snapshot at purchase time (decimal, 10 digits, 2 decimals).
        order: Relationship to Order object.
        product: Relationship to Product object.
    """

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_purchase: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_item_quantity_positive"),
    )

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()

    def __repr__(self) -> str:
        """Return a string representation of the OrderItem."""
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"