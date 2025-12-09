from app.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

def get_db_session(db: AsyncSession = Depends(get_db)):
    return db