from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.modules.auth.dependencies import get_current_user, require_role
from app.modules.auth.models import User
from app.modules.orders.models import Order, OrderItem
from app.modules.orders.schemas import OrderCreate, OrderOut, OrderItemOut
from app.modules.orders.service import checkout_order, get_user_orders, get_order_by_id


router = APIRouter()


@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_order = checkout_order(db, current_user.id, order)
    return get_order_by_id(db, new_order.id, current_user.id)


@router.get("/", response_model=List[OrderOut])
def read_user_orders(skip: int = 0, limit: int = Query(10, le=100), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_orders(db, current_user.id, skip, limit)


@router.get("/{order_id}", response_model=OrderOut)
def read_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id, current_user.id)
    if not order:
        # Allow admin to view any order
        if current_user.role == "admin":
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
                item_outs = [OrderItemOut(id=i.id, product_id=i.product_id, quantity=i.quantity, price_at_purchase=i.price_at_purchase) for i in items]
                return OrderOut(id=order.id, user_id=order.user_id, status=order.status.value, total_price=order.total_price, created_at=order.created_at, items=item_outs)
        raise HTTPException(status_code=404, detail="Order not found")
    return order