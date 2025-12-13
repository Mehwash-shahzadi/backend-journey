from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.users.models import User, UserRole
from app.shared.security import hash_password
from fastapi import HTTPException, status


async def create_user(db: AsyncSession, email: str, password: str, full_name: str | None, role: str = "user"):
    hashed = hash_password(password)  
    print(f"DEBUG: Plain password: {password[:5]}...")  
    print(f"DEBUG: Hashed password: {hashed[:20]}...")  
    
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
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()