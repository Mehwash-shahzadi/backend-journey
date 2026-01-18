from slowapi import Limiter
from fastapi import Request


def get_rate_limit_key(request: Request) -> str:
    """
    Get rate limit key based on IP address.
    Day 73: All users limited to 10 req/min by IP
    Future: Can add user_id from headers for authenticated users (60 req/min)
    """
    return request.client.host if request.client else "unknown"


# Initialize rate limiter 
# Rate limits:
# - Free tier: 10 requests per minute (current)
# - Auth tier: 60 requests per minute (future: add auth detection)
limiter = Limiter(key_func=get_rate_limit_key)
