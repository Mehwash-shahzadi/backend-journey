"""
Order repository for order-specific database operations.

Includes special methods for preloading order items and product details.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models import Order
from .base_repo import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order model.

    Provides async database operations for orders.
    Inherits: get_all, get_by_id, create, update, delete.
    Special methods for eager-loading items and products.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize OrderRepository.

        Args:
            session: AsyncSession instance.
        """
        super().__init__(session, Order)

    async def get_by_id_with_items(
        self, user_id: int, order_id: int
    ) -> Order | None:
        """
        Retrieve a single order with all items and product details preloaded.

        Ensures user ownership and eagerly loads:
        - OrderItems
        - Product details for each OrderItem

        Args:
            user_id: User id (for ownership verification).
            order_id: Order id.

        Returns:
            Order instance with items and products preloaded, None if not found.
        """
        stmt = (
            select(Order)
            .where(Order.id == order_id, Order.user_id == user_id)
            .options(
                selectinload(Order.items).joinedload(
                    Order.items.property.mapper.relationships["product"]
                )
            )
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_all_by_user(self, user_id: int) -> list[Order]:
        """
        Retrieve all orders for a specific user with items preloaded.

        Args:
            user_id: User id to filter by.

        Returns:
            List of Order instances for the user.
        """
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()