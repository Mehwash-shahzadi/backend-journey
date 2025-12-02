from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str):
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, name: str, email: str, age: int):
        user = User(name=name, email=email, balance=0)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def get_all(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()