from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.shared.security import decode_token
from app.modules.users.repository import get_user_by_email
from app.shared.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

def get_db_session(db: AsyncSession = Depends(get_db)):
    return db

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session)
):
    payload = decode_token(token)
    
    if payload is None:
        raise UnauthorizedException(detail="Invalid token")
    
    email: str = payload.get("sub")
    if email is None:
        raise UnauthorizedException(detail="Invalid token payload")
    
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise UnauthorizedException(detail="User not found")
    
    return user