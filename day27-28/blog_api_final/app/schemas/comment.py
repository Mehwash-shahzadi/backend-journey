from pydantic import BaseModel, Field
from datetime import datetime

class CommentBase(BaseModel):
    """
    Base fields for Comment.
    """
    content: str = Field(..., example="Nice post!", description="Comment text")

    model_config = {
        "json_schema_extra": {
            "example": {
                "content": "Nice post!"
            }
        }
    }

class CommentCreate(CommentBase):
    """Request body to create a comment"""
    post_id: int = Field(..., example=1, description="ID of the post being commented on")

class CommentOut(CommentBase):
    """Response model for comment endpoints"""
    id: int
    post_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "post_id": 1,
                "content": "Nice post!",
                "created_at": "2025-11-23T12:00:00Z"
            }
        }
    }
