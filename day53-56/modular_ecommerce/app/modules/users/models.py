from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime


class UserPublic(BaseModel):
    id: int
    full_name: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None