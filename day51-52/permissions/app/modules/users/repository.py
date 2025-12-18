from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.users.models import User, RefreshToken
from app.shared.security import hash_password
from datetime import datetime, timedelta, timezone
from app.config import settings

async def create_user(db: AsyncSession, email: str, password: str, full_name: str | None, role: str = "user"):
    hashed = hash_password(password)
    new_user = User(
        email=email, 
        hashed_password=hashed,
        full_name=full_name, 
        role=role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

# REFRESH TOKEN FUNCTIONS 

async def create_refresh_token(db: AsyncSession, token: str, user_id: int) -> RefreshToken:
    """Create and store refresh token in database"""
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(refresh_token)
    await db.commit()
    await db.refresh(refresh_token)
    return refresh_token

async def get_refresh_token(db: AsyncSession, token: str) -> RefreshToken | None:
    """Get refresh token from database"""
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    return result.scalar_one_or_none()

async def revoke_refresh_token(db: AsyncSession, token: str) -> bool:
    """Revoke a refresh token"""
    refresh_token = await get_refresh_token(db, token)
    if refresh_token:
        refresh_token.is_revoked = True
        await db.commit()
        return True
    return False

async def delete_expired_tokens(db: AsyncSession):
    """Delete expired refresh tokens (cleanup)"""
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.expires_at < datetime.now(timezone.utc))
    )
    expired_tokens = result.scalars().all()
    for token in expired_tokens:
        await db.delete(token)
    await db.commit()