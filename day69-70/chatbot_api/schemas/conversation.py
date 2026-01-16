from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ConversationCreate(BaseModel):
    user_id: str
    title: Optional[str] = None

class ConversationOut(BaseModel):
    id: UUID
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True