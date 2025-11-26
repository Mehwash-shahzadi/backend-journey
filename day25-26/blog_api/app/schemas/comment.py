from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    post_id: int

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
