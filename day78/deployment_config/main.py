"""
FastAPI app with logging and monitoring for Day 78.
Includes structured logging, request middleware, and health check endpoint.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from logging_config import setup_logging, get_logger
from middleware.logging_middleware import LoggingMiddleware

# Setup logging at startup
setup_logging(log_level="INFO")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Application startup", extra={"version": "1.0.0"})
    yield
    # Shutdown
    logger.info("Application shutdown")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Chatbot API with Logging",
    description="Day 78: Logging & Monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns status and environment information.
    """
    logger.info("Health check called")
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "message": "Chatbot API is running",
            "version": "1.0.0"
        }
    )


@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root endpoint called")
    return {
        "message": "Welcome to Chatbot API",
        "health_check": "/health",
        "docs": "/docs"
    }


@app.get("/logs/status")
async def logs_status():
    """
    Return current logging status.
    Useful for verifying logging setup.
    """
    logger.info("Logs status check")
    return {
        "logging_enabled": True,
        "structured_logs": "logs/app.json",
        "error_logs": "logs/error.json",
        "message": "Check logs/ directory for output files"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server with uvicorn")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None  # Use our custom logging config
    )