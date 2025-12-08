from typing import Generic, TypeVar, Type, Any, Optional, Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

# Generic type variable – works with any SQLAlchemy model
ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic async repository providing common CRUD operations.

    All repositories inherit from this class to avoid code duplication.
    Handles session management, commit, refresh, and error safety.
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        """
        Initialize the repository with session and model.

        Args:
            session: AsyncSession instance from dependency injection.
            model: SQLAlchemy model class (e.g., User, Category, Product).
        """
        self.session = session
        self.model = model

    async def get_all(self) -> Sequence[ModelType]:
        """
        Retrieve all records from the table.

        Returns:
            List of all model instances.
        """
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, id: int) -> ModelType | None:
        """
        Retrieve a single record by primary key.

        Args:
            id: Primary key value.

        Returns:
            Model instance if found, None otherwise.
        """
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, obj: ModelType) -> ModelType:
        """
        Create a new record in the database.

        Args:
            obj: Model instance to create (with data already set).

        Returns:
            Created model instance with database-generated fields (e.g., id).

        Note:
            This now commits and refreshes — data is actually saved!
        """
        self.session.add(obj)
        await self.session.commit()          
        await self.session.refresh(obj)      
        return obj

    async def update(self, id: int, update_data: dict[str, Any]) -> ModelType | None:
        """
        Update an existing record by id.

        Args:
            id: Primary key of record to update.
            update_data: Dictionary of fields to update (e.g., {"name": "New Name"}).

        Returns:
            Updated model instance, or None if not found.
        """
        obj = await self.get_by_id(id)
        if not obj:
            return None

        for key, value in update_data.items():
            setattr(obj, key, value)

        await self.session.commit()          
        await self.session.refresh(obj)      
        return obj

    async def delete(self, id: int) -> bool:
        """
        Delete a record by id.

        Args:
            id: Primary key of record to delete.

        Returns:
            True if deleted, False if not found.
        """
        obj = await self.get_by_id(id)
        if not obj:
            return False

        await self.session.delete(obj)
        await self.session.commit()          
        return True