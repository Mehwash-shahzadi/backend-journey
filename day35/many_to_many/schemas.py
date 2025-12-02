from pydantic import BaseModel
from typing import List
from datetime import datetime

class TagCreate(BaseModel):
    name: str

class TagSchema(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str
    author: str

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    tags: List[TagSchema] = []
    
    class Config:
        from_attributes = True

class TagAdd(BaseModel):
    tag_name: str