# """
# SQLAlchemy models package.

# Re-exports all models and association tables for convenient importing.
# """

# from .user import User
# from .category import Category
# from .product import Product
# from .order import Order
# from .order_item import OrderItem
# from .association import product_categories

# __all__ = [
#     "User",
#     "Category",
#     "Product",
#     "Order",
#     "OrderItem",
#     "product_categories",
# ]
"""
Export all models and the SQLAlchemy Base so that:
    from app.models import Base, User, Category, Product, Order, OrderItem
works everywhere (main.py, alembic, create_admin.py, etc.)
"""

from app.models.user import Base  # ← this is the important line
from app.models.user import User
from app.models.category import Category
from app.models.product import Product, product_categories  # association table
from app.models.order import Order
from app.models.order_item import OrderItem

__all__ = [
    "Base",
    "User",
    "Category",
    "Product",
    "Order",
    "OrderItem",
    "product_categories",
]