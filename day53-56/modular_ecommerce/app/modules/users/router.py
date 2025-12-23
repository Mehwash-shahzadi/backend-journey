from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.modules.auth.dependencies import get_current_user, require_role
from app.modules.auth.models import User
from app.modules.users.models import UserOut, UserUpdate, UserPublic
from app.modules.users.service import get_my_profile, update_my_profile, get_user_public, get_users_admin


router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return get_my_profile(current_user) 


@router.put("/me", response_model=UserOut)
def update_users_me(update_data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_my_profile(db, current_user, update_data)


@router.get("/{user_id}", response_model=UserPublic)
def read_user_public(user_id: int, db: Session = Depends(get_db)):
    return get_user_public(db, user_id)


@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = Query(10, le=100), db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return get_users_admin(db, skip, limit)