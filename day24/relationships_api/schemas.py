from pydantic import BaseModel
from datetime import datetime
from typing import List

# ------- POST --------
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ------- USER --------
class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime
    posts: List[PostOut] = []

    class Config:
        orm_mode = True
