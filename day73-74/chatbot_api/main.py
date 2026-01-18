from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from middleware.error_handler import ErrorHandlingMiddleware
from routers.chat import router as chat_router
from routers.ai_features import router as ai_router
from limiter import limiter

# Create FastAPI app with rate limiter
app = FastAPI(title="AI Chatbot Backend - Days 69-72 with Day 73 Security & Day 74 Optimization")
app.state.limiter = limiter

# Add error handling middleware 
app.add_middleware(ErrorHandlingMiddleware)

# Add exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    """Handle rate limit exceeded errors (Day 73)"""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please try again later.",
            "error_code": "RATE_LIMIT_EXCEEDED"
        }
    )

# Include routers with rate limiting 
# Rate limits:
# - Free tier: 10 requests per minute
# - Auth tier: 60 requests per minute (future: add auth detection)
app.include_router(chat_router)
app.include_router(ai_router)  # AI features router with rate limiting and error handling 