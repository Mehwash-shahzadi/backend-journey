from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TagSchema(BaseModel):
    name: str
    class Config:
        from_attributes = True

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    tags: Optional[List[TagSchema]] = []
    class Config:
        from_attributes = True
