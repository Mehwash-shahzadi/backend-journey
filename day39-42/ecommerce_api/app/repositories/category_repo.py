from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from .base_repo import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Repository for Category model.

    Provides async database operations for categories.
    Inherits: get_all, get_by_id, create, update, delete.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize CategoryRepository.

        Args:
            session: AsyncSession instance.
        """
        super().__init__(session, Category)

    async def get_by_name(self, name: str) -> Category | None:
        """
        Retrieve a category by name.

        Args:
            name: Category name to search.

        Returns:
            Category instance if found, None otherwise.
        """
        stmt = select(Category).where(Category.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()