from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_user, get_users, update_user, delete_user
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    # create_user returns existing user if email exists (simple behavior)
    created = create_user(db, email=user.email, name=user.name)
    return created

@router.get("/", response_model=List[UserOut])
def api_get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def api_update_user(user_id: int, name: str, db: Session = Depends(get_db)):
    user = update_user(db, user_id, name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
