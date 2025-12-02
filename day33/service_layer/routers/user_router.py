from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import UserCreate, UserResponse
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
#create user
@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        user = service.create_user_with_validation(data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
# Deactivate a user
@router.post("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.deactivate_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get user with posts
@router.get("/users/{user_id}/posts")
def get_user_with_posts(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user_with_posts(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
