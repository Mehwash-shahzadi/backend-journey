from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.comment import CommentOut

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class PostOut(PostBase):
    id: int
    user_id: int
    created_at: datetime
    comments: Optional[List[CommentOut]] = []

    class Config:
        from_attributes = True
