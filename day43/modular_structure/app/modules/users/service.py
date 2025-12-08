# app/modules/users/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repository import get_user_by_id

async def get_user_service(db: AsyncSession, user_id: int):
    return await get_user_by_id(db, user_id)