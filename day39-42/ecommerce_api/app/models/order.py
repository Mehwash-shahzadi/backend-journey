from typing import TYPE_CHECKING
from enum import StrEnum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import Base

if TYPE_CHECKING:
    from .user import User
    from .order_item import OrderItem
class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Fixed: NUMERIC(12, 2) = up to 10 billion with 2 decimals (perfect for money)
    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),           # ← THIS IS THE CORRECT ONE
        default=Decimal("0.00"),
        server_default="0.00",
        nullable=False,
    )

    status: Mapped[OrderStatus] = mapped_column(
        String(20),
        default=OrderStatus.PENDING,
        server_default=OrderStatus.PENDING.value,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Order #{self.id} | {self.status} | ${self.total}>"