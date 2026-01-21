"""
Example FastAPI application using the configuration system.
This shows how to load and use environment variables safely.
"""

from fastapi import FastAPI, Depends
from config import Settings, get_settings

app = FastAPI(
    title="Configured FastAPI App",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    """Log startup info (no secrets!)."""
    settings = get_settings()
    print(f" Starting app in {settings.ENVIRONMENT} mode")
    print(f" Debug mode: {settings.DEBUG}")
    print(f" API Version: {settings.API_VERSION}")


@app.get("/")
async def root():
    """Home endpoint."""
    return {"message": "Configuration system working!"}


@app.get("/config/info")
async def config_info(settings: Settings = Depends(get_settings)):
    """
    Show non-sensitive configuration info.
    Never return actual secrets!
    """
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "api_version": settings.API_VERSION,
        "token_expiry_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "algorithm": settings.ALGORITHM,
    }


@app.get("/health")
async def health_check(settings: Settings = Depends(get_settings)):
    """Check if app is running with valid config."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )
