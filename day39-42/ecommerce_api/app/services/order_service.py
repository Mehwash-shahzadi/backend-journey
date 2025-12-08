import logging
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Order, OrderItem, Product
from app.repositories import OrderRepository, ProductRepository  
from app.schemas import OrderItemCreate

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def create_order(
        self,
        user: User,
        items_data: list[OrderItemCreate],
        product_repo: ProductRepository,
        session: AsyncSession,
    ) -> Order:
        total = Decimal("0.0")
        order_items_to_create = []

        for item in items_data:
            product = await product_repo.get_by_id(item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for '{product.name}'. Only {product.stock} left.",
                )

            total += product.price * item.quantity
            order_items_to_create.append((product, item.quantity))

        try:
            order = Order(user_id=user.id, total=total, status="pending")
            session.add(order)
            await session.flush()

            for product, quantity in order_items_to_create:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price_at_purchase=product.price,
                )
                session.add(order_item)
                product.stock -= quantity

            await session.commit()
            await session.refresh(order, attribute_names=["items"])

            logger.info(f"Order #{order.id} created | User {user.id} | Total ${total}")
            return order

        except Exception as e:
            await session.rollback()
            logger.error(f"Order failed: {e}")
            raise HTTPException(status_code=500, detail="Order creation failed") from e

    async def get_user_orders(self, user_id: int) -> list[Order]:
        return await self.order_repo.get_all_by_user_with_items(user_id)