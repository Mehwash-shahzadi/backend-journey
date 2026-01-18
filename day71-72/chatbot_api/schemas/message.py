from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageOut(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    tokens_used: int
    created_at: datetime

    class Config:
        from_attributes = True