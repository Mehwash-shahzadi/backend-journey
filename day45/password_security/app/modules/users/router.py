from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db_session
from app.modules.users.schemas import UserCreate, UserOut
from app.modules.users.service import register_user_service, authenticate_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db_session)):
    user = await register_user_service(db, user_in.email, user_in.password, user_in.full_name)
    return user

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db_session)):
    user = await authenticate_user_service(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"message": "Login successful", "user_id": user.id}