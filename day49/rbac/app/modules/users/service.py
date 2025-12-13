from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repository import create_user, get_user_by_email
from app.modules.users.models import UserRole
from app.shared.security import verify_password


async def register_user_service(db: AsyncSession, email: str, password: str, full_name: str | None, role: str = "user"):
    return await create_user(db, email, password, full_name, role)

async def authenticate_user_service(db: AsyncSession, username: str, password: str):
    user = await get_user_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user