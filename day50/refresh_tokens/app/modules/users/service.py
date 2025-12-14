from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repository import (
    create_user, 
    get_user_by_email,
    create_refresh_token,
    get_refresh_token,
    revoke_refresh_token
)
from app.shared.security import verify_password, create_refresh_token as generate_refresh_token
from datetime import datetime, timezone

async def register_user_service(db: AsyncSession, email: str, password: str, full_name: str | None, role: str = "user"):
    return await create_user(db, email, password, full_name, role)

async def authenticate_user_service(db: AsyncSession, username: str, password: str):
    user = await get_user_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# REFRESH TOKEN SERVICES 

async def create_user_refresh_token(db: AsyncSession, user_id: int) -> str:
    """Create and store refresh token for user"""
    token = generate_refresh_token()
    await create_refresh_token(db, token, user_id)
    return token

async def validate_refresh_token(db: AsyncSession, token: str) -> int | None:
    """Validate refresh token and return user_id if valid"""
    refresh_token = await get_refresh_token(db, token)
    
    if not refresh_token:
        return None
    
    if refresh_token.is_revoked:
        return None
    
    # Fix: Use timezone-aware datetime
    if refresh_token.expires_at < datetime.now(timezone.utc):
        return None
    
    return refresh_token.user_id

async def revoke_token_service(db: AsyncSession, token: str) -> bool:
    """Revoke a refresh token"""
    return await revoke_refresh_token(db, token)