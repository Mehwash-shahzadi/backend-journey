from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TokenUsage(BaseModel):
    user_key: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    timestamp: str  

class UserUsageSummary(BaseModel):
    user_key: str
    total_requests: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    last_request: Optional[str] = None
    is_blocked: bool = False