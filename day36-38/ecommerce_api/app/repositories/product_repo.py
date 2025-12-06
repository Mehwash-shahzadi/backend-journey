"""
Product repository for product-specific database operations.

Includes special methods for preloading categories.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Product
from .base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository for Product model.

    Provides async database operations for products.
    Inherits: get_all, get_by_id, create, update, delete.
    Special methods for eager-loading relationships.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize ProductRepository.

        Args:
            session: AsyncSession instance.
        """
        super().__init__(session, Product)

    async def get_all_with_categories(self) -> list[Product]:
        """
        Retrieve all products with categories eagerly loaded.

        Avoids N+1 query problem by using joinedload.

        Returns:
            List of Product instances with categories preloaded.
        """
        stmt = select(Product).options(joinedload(Product.categories))
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_by_id_with_categories(self, id: int) -> Product | None:
        """
        Retrieve a single product by id with categories eagerly loaded.

        Args:
            id: Product id.

        Returns:
            Product instance with categories preloaded, None if not found.
        """
        stmt = select(Product).where(Product.id == id).options(joinedload(Product.categories))
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()