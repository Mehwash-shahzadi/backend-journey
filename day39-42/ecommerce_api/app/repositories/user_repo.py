from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from .base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model.

    Provides async database operations for users.
    Inherits: get_all, get_by_id, create, update, delete.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize UserRepository.

        Args:
            session: AsyncSession instance.
        """
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email address.

        Args:
            email: User email to search.

        Returns:
            User instance if found, None otherwise.
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()