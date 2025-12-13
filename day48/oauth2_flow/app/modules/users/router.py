from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.dependencies import get_db_session, get_current_user
from app.modules.users.schemas import UserCreate, UserOut, Token
from app.modules.users.service import register_user_service, authenticate_user_service
from app.shared.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db_session)):
    user = await register_user_service(db, user_in.email, user_in.password, user_in.full_name)
    return user

@router.post("/token", response_model=Token)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    grant_type: str = Form(default="password"),
    db: AsyncSession = Depends(get_db_session)
):
    if grant_type != "password":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid grant_type"
        )
    
    user = await authenticate_user_service(db, username, password)
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
async def get_current_user_info(current_user: UserOut = Depends(get_current_user)):
    return current_user