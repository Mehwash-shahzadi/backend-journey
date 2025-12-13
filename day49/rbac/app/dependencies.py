from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.shared.security import decode_token
from app.modules.users.repository import get_user_by_email
from app.modules.users.models import User, UserRole
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
) -> User:
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

def require_role(*allowed_roles: UserRole):
    """Dependency to check if user has required role"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_user
    return role_checker

async def get_current_admin(current_user: User = Depends(require_role(UserRole.ADMIN))) -> User:
    """Shortcut dependency for admin-only routes"""
    return current_user

async def get_current_moderator(current_user: User = Depends(require_role(UserRole.MODERATOR, UserRole.ADMIN))) -> User:
    """Shortcut dependency for moderator or admin routes"""
    return current_user