from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import User
from repositories.user_repository import UserRepository
from schemas import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return repo.get_all()

@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    
    new_user = User(name=data.name, email=data.email)
    return repo.create(new_user.name, new_user.email, 0)