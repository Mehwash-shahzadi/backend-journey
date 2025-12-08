"""
User model.

Represents a user in the e-commerce system.
Users can be customers or admins, and can place multiple orders.
"""

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .order import Order


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""
    pass


class User(Base):
    """
    User model.

    Attributes:
        id: Unique identifier (auto-increment).
        email: User email (unique, indexed).
        name: User full name.
        role: User role ('customer' or 'admin').
        hashed_password: Bcrypt-hashed password.
        created_at: Timestamp when user was created (server-generated).
        orders: Relationship to Order objects.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="customer")
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )

    # One-to-many: User -> Order
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Return a string representation of the User."""
        return f"<User(id={self.id}, email={self.email}, name={self.name}, role={self.role})>"