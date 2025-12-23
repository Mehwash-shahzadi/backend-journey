from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum

from app.database import Base


class OrderStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.pending)
    total_price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_purchase: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))

    order = relationship("Order", back_populates="items")
    product = relationship("Product")