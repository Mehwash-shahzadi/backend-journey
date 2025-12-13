from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repository import create_user, get_user_by_email
from app.shared.security import verify_password

async def register_user_service(db: AsyncSession, email: str, password: str, full_name: str | None):
    return await create_user(db, email, password, full_name)

async def authenticate_user_service(db: AsyncSession, username: str, password: str):
    # username parameter actually receives email in OAuth2
    user = await get_user_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user