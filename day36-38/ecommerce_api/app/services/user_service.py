"""
User service for user-related business logic.

Handles user retrieval and validation.
"""

from fastapi import HTTPException, status

from app.models import User
from app.repositories import UserRepository


class UserService:
    """
    Service layer for user operations.

    Handles user business logic such as retrieval and validation.
    """

    def __init__(self, user_repo: UserRepository):
        """
        Initialize UserService.

        Args:
            user_repo: UserRepository instance for data access.
        """
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by id.

        Args:
            user_id: User id to retrieve.

        Returns:
            User instance.

        Raises:
            HTTPException: 404 if user not found.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email address.

        Args:
            email: User email to search.

        Returns:
            User instance if found, None otherwise.
        """
        return await self.user_repo.get_by_email(email)