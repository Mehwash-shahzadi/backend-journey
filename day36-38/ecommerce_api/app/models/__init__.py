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