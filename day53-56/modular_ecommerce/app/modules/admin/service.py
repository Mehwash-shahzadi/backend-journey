from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.modules.auth.models import User
from app.modules.orders.models import Order, OrderItem
from app.modules.products.models import Product


def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user_role(db: Session, user_id: int, new_role: str, current_admin: User) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    if user.id == current_admin.id:
        raise ValueError("Cannot change your own role")
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user


def ban_user(db: Session, user_id: int, current_admin: User) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    if user.id == current_admin.id:
        raise ValueError("Cannot ban yourself")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def get_sales_analytics(db: Session) -> Dict[str, Any]:
    total_orders = db.query(func.count(Order.id)).scalar()
    total_revenue = db.query(func.sum(OrderItem.price_at_purchase * OrderItem.quantity)).join(Order).scalar() or 0
    top_products = (
        db.query(Product.name, func.sum(OrderItem.quantity).label("total_sold"))
        .join(OrderItem)
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )
    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "top_5_products": [{"name": p.name, "total_sold": p.total_sold} for p in top_products]
    }