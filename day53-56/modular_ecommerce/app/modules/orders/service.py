from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal
from fastapi import HTTPException

from app.modules.orders.models import Order, OrderItem, OrderStatus
from app.modules.orders.schemas import OrderCreate, OrderOut, OrderItemOut
from app.modules.products.models import Product


def checkout_order(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    # Validate stock and calculate total
    total = Decimal(0)
    items_to_create = []
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
        total += product.price * item.quantity
        items_to_create.append((product, item.quantity, product.price))

    # Atomic transaction
    try:
        # Deduct stock
        for product, quantity, _ in items_to_create:
            product.stock -= quantity

        # Create order
        new_order = Order(user_id=user_id, total_price=total)
        db.add(new_order)
        db.flush()  # Get order.id

        # Create order items
        for product, quantity, price in items_to_create:
            order_item = OrderItem(order_id=new_order.id, product_id=product.id, quantity=quantity, price_at_purchase=price)
            db.add(order_item)

        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Order failed due to error")


def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[OrderOut]:
    orders = db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()
    result = []
    for o in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
        item_outs = [OrderItemOut(id=i.id, product_id=i.product_id, quantity=i.quantity, price_at_purchase=i.price_at_purchase) for i in items]
        result.append(OrderOut(id=o.id, user_id=o.user_id, status=o.status.value, total_price=o.total_price, created_at=o.created_at, items=item_outs))
    return result


def get_order_by_id(db: Session, order_id: int, user_id: int) -> Optional[OrderOut]:
    o = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not o:
        return None
    items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
    item_outs = [OrderItemOut(id=i.id, product_id=i.product_id, quantity=i.quantity, price_at_purchase=i.price_at_purchase) for i in items]
    return OrderOut(id=o.id, user_id=o.user_id, status=o.status.value, total_price=o.total_price, created_at=o.created_at, items=item_outs)