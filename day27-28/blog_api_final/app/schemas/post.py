from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.comment import CommentOut

class PostBase(BaseModel):
    """
    Base fields for Post.
    """
    title: str = Field(..., example="My First Post", description="Post title")
    content: str = Field(..., example="Hello world content", description="Post body text")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My First Post",
                "content": "Hello world content"
            }
        }
    }

class PostCreate(PostBase):
    """Request body for creating a post."""
    user_id: int = Field(..., example=1, description="ID of the user who owns this post")


class PostOut(PostBase):
    """Response model for Post endpoints."""
    id: int
    user_id: int
    created_at: datetime
    comments: Optional[List[CommentOut]] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "My First Post",
                "content": "Hello world content",
                "created_at": "2025-11-23T12:00:00Z",
                "comments": []
            }
        }
    }
