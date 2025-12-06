"""
Category service for category-related business logic.

Handles CRUD operations for product categories (admin-only in routers).
"""

from fastapi import HTTPException, status

from app.models import Category
from app.repositories import CategoryRepository
from app.schemas import CategoryCreate, CategoryUpdate


class CategoryService:
    """
    Service layer for category operations.

    Handles category CRUD operations and validation.
    """

    def __init__(self, category_repo: CategoryRepository):
        """
        Initialize CategoryService.

        Args:
            category_repo: CategoryRepository instance for data access.
        """
        self.category_repo = category_repo

    async def get_all_categories(self) -> list[Category]:
        """
        Retrieve all categories.

        Returns:
            List of all Category instances.
        """
        return await self.category_repo.get_all()

    async def get_category_by_id(self, category_id: int) -> Category:
        """
        Retrieve a category by id.

        Args:
            category_id: Category id to retrieve.

        Returns:
            Category instance.

        Raises:
            HTTPException: 404 if category not found.
        """
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
        return category

    async def create_category(self, category_in: CategoryCreate) -> Category:
        """
        Create a new category.

        Args:
            category_in: CategoryCreate schema with category data.

        Returns:
            Created Category instance.

        Raises:
            HTTPException: 400 if category name already exists.
        """
        # Check if category with same name exists
        existing = await self.category_repo.get_by_name(category_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists",
            )

        category = Category(
            name=category_in.name,
            description=category_in.description,
        )
        return await self.category_repo.create(category)

    async def update_category(
        self, category_id: int, category_in: CategoryUpdate
    ) -> Category:
        """
        Update an existing category.

        Args:
            category_id: Category id to update.
            category_in: CategoryUpdate schema with fields to update.

        Returns:
            Updated Category instance.

        Raises:
            HTTPException: 404 if category not found.
            HTTPException: 400 if new name already exists.
        """
        category = await self.get_category_by_id(category_id)

        # Check for duplicate name if changing name
        if category_in.name and category_in.name != category.name:
            existing = await self.category_repo.get_by_name(category_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category with this name already exists",
                )

        update_data = category_in.model_dump(exclude_unset=True)
        return await self.category_repo.update(category_id, update_data)

    async def delete_category(self, category_id: int) -> bool:
        """
        Delete a category by id.

        Args:
            category_id: Category id to delete.

        Returns:
            True if deleted successfully.

        Raises:
            HTTPException: 404 if category not found.
        """
        category = await self.get_category_by_id(category_id)
        return await self.category_repo.delete(category_id)