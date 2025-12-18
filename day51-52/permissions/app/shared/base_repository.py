from typing import TypeVar, Generic, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base


T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Generic repository providing CRUD operations.
    
    All module-specific repositories inherit from this.
    """
    
    def __init__(self, session: AsyncSession, model: Type[T]):
        """
        Initialize repository.
        
        Args:
            session: Database session.
            model: SQLAlchemy model class.
        """
        self.session = session
        self.model = model
    
    async def get_all(self) -> list[T]:
        """
        Retrieve all records.
        
        Returns:
            List of model instances.
        """
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, id: int) -> T | None:
        """
        Retrieve record by ID.
        
        Args:
            id: Record identifier.
        
        Returns:
            Model instance if found, None otherwise.
        """
        return await self.session.get(self.model, id)
    
    async def create(self, obj: T) -> T:
        """
        Create new record.
        
        Args:
            obj: Model instance to create.
        
        Returns:
            Created model instance.
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def update(self, id: int, data: dict) -> T | None:
        """
        Update record by ID.
        
        Args:
            id: Record identifier.
            data: Fields to update.
        
        Returns:
            Updated model instance if found, None otherwise.
        """
        obj = await self.get_by_id(id)
        if not obj:
            return None
        
        for key, value in data.items():
            setattr(obj, key, value)
        
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, id: int) -> bool:
        """
        Delete record by ID.
        
        Args:
            id: Record identifier.
        
        Returns:
            True if deleted, False if not found.
        """
        obj = await self.get_by_id(id)
        if not obj:
            return False
        
        await self.session.delete(obj)
        await self.session.commit()
        return True