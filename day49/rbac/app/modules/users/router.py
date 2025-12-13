from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import List
from app.dependencies import (
    get_db_session, 
    get_current_user, 
    get_current_admin,
    require_role
)
from app.modules.users.schemas import UserCreate, UserOut, Token
from app.modules.users.service import register_user_service, authenticate_user_service
from app.modules.users.models import User, UserRole
from app.shared.security import create_access_token
from app.config import settings
from sqlalchemy.future import select

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db_session)):
    """Register new user - default role is USER"""
    user = await register_user_service(db, user_in.email, user_in.password, user_in.full_name, user_in.role)
    return user

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  
    db: AsyncSession = Depends(get_db_session)
):
    """Login to get access token"""
    user = await authenticate_user_service(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information - any authenticated user"""
    return current_user

# ============= ADMIN ONLY ROUTES =============

@router.get("/admin/all-users", response_model=List[UserOut])
async def get_all_users(
    db: AsyncSession = Depends(get_db_session),
    current_admin: User = Depends(get_current_admin)
):
    """Get all users - ADMIN ONLY"""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_admin: User = Depends(get_current_admin)
):
    """Delete a user - ADMIN ONLY"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    await db.delete(user)
    await db.commit()
    return {"message": f"User {user.email} deleted successfully"}

@router.patch("/admin/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: UserRole,
    db: AsyncSession = Depends(get_db_session),
    current_admin: User = Depends(get_current_admin)
):
    """Update user role - ADMIN ONLY"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = new_role.value  # Convert enum to string
    await db.commit()
    await db.refresh(user)
    return {"message": f"User {user.email} role updated to {new_role.value}"}

# ============= MODERATOR ROUTES =============

@router.get("/moderator/stats")
async def get_user_stats(
    db: AsyncSession = Depends(get_db_session),
    current_moderator: User = Depends(require_role(UserRole.MODERATOR, UserRole.ADMIN))
):
    """Get user statistics - MODERATOR or ADMIN"""
    result = await db.execute(select(User))
    all_users = result.scalars().all()
    
    stats = {
        "total_users": len(all_users),
        "admins": len([u for u in all_users if u.role == "admin"]),
        "moderators": len([u for u in all_users if u.role == "moderator"]),
        "regular_users": len([u for u in all_users if u.role == "user"])
    }
    return stats