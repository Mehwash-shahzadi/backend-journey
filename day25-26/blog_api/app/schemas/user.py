from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.schemas.post import PostOut

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime
    posts: Optional[List[PostOut]] = []

    class Config:
        from_attributes = True
