from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.users.models import User
from app.shared.security import hash_password

async def create_user(db: AsyncSession, email: str, password: str, full_name: str | None):
    hashed = hash_password(password)
    new_user = User(email=email, hashed_password=hashed, full_name=full_name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()