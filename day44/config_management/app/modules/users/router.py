from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db_session
from app.modules.users.service import get_user_service
from app.modules.users.schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await get_user_service(db, user_id)
    return user
