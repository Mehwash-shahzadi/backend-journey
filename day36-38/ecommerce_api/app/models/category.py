"""
Category model.

Represents product categories in the e-commerce system.
Categories have a many-to-many relationship with Products.
"""

from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import Base
from .association import product_categories

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    """
    Category model.

    Attributes:
        id: Unique identifier (auto-increment).
        name: Category name (unique, indexed).
        description: Optional category description.
        products: Relationship to Product objects via many-to-many.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Many-to-many: Category <-> Product
    products: Mapped[list["Product"]] = relationship(
        secondary=product_categories,
        back_populates="categories",
    )

    def __repr__(self) -> str:
        """Return a string representation of the Category."""
        return f"<Category(id={self.id}, name={self.name})>"