"""
OrderItem repository for order item-specific database operations.

This repository is internal-only and used only by OrderService.
It is NOT exposed via public routers.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import OrderItem
from .base_repo import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):
    """
    Repository for OrderItem model.

    Internal repository used only by OrderService.
    Not exposed via public API routes.

    Provides async database operations for order items.
    Inherits: get_all, get_by_id, create, update, delete.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize OrderItemRepository.

        Args:
            session: AsyncSession instance.
        """
        super().__init__(session, OrderItem)

    async def get_by_order_id(self, order_id: int) -> list[OrderItem]:
        """
        Retrieve all order items for a specific order.

        Args:
            order_id: Order id to filter by.

        Returns:
            List of OrderItem instances for the order.
        """
        stmt = select(OrderItem).where(OrderItem.order_id == order_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()