"""
Product model.

Represents products in the e-commerce system.
Products have a many-to-many relationship with Categories.
Products can have multiple OrderItems.
"""

from typing import TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, Integer, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import Base
from .association import product_categories

if TYPE_CHECKING:
    from .category import Category
    from .order_item import OrderItem


class Product(Base):
    """
    Product model.

    Attributes:
        id: Unique identifier (auto-increment).
        name: Product name (indexed).
        price: Product price (decimal, 10 digits, 2 decimals).
        stock: Current stock quantity (must be >= 0).
        created_at: Timestamp when product was created (server-generated).
        categories: Relationship to Category objects via many-to-many.
        order_items: Relationship to OrderItem objects.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )

    __table_args__ = (
        CheckConstraint("stock >= 0", name="ck_product_stock_non_negative"),
    )

    # Many-to-many with categories
    categories: Mapped[list["Category"]] = relationship(
        secondary=product_categories,
        back_populates="products",
    )

    # One-to-many: Product -> OrderItem
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )

    def __repr__(self) -> str:
        """Return a string representation of the Product."""
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, stock={self.stock})>"