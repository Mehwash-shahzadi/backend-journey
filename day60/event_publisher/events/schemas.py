from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserRegisteredEvent(BaseModel):
    event_type: str = "user.registered"
    user_id: int
    email: str
    timestamp: Optional[datetime] = None


class OrderCreatedEvent(BaseModel):
    event_type: str = "order.created"
    order_id: int
    user_id: int
    total: float
    timestamp: Optional[datetime] = None
