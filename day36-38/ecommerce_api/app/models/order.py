"""
Order model.

Represents orders placed by users in the e-commerce system.
Orders contain multiple OrderItems and track order status and total.
"""

from typing import TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import Base

if TYPE_CHECKING:
    from .user import User
    from .order_item import OrderItem


class Order(Base):
    """
    Order model.

    Attributes:
        id: Unique identifier (auto-increment).
        user_id: Foreign key to User (CASCADE on delete).
        total: Total order amount (decimal, 12 digits, 2 decimals).
        status: Order status (pending, paid, shipped, delivered, cancelled).
        created_at: Timestamp when order was created (server-generated).
        user: Relationship to User object.
        items: Relationship to OrderItem objects.
    """

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Return a string representation of the Order."""
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total})>"