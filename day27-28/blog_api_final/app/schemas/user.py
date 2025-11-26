from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from app.schemas.post import PostOut

class UserBase(BaseModel):
    """
    Shared properties for User.
    """
    email: EmailStr = Field(..., example="muhammad@example.com", description="Unique user email")
    name: str = Field(..., example="Muhammad", description="Full name of the user")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "muhammad@example.com",
                "name": "Muhammad"
            }
        }
    }


class UserCreate(UserBase):
    """Request body used to create a user."""
    pass


class UserOut(UserBase):
    """Response model returned by user endpoints."""
    id: int
    created_at: datetime
    posts: Optional[List[PostOut]] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "muhammad@example.com",
                "name": "Muhammad",
                "created_at": "2025-11-23T12:00:00Z",
                "posts": []
            }
        }
    }
