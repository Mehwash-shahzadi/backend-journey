from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.database.db import engine
from app.models import Base  # imports all models for Base.metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Startup:
        - Creates all database tables from SQLAlchemy models (development only).
        - For production, use Alembic migrations instead.

    Shutdown:
        - Disposes of the async engine.

    Args:
        app: FastAPI application instance.

    Yields:
        None
    """
    # Startup: Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown: Cleanup engine
    await engine.dispose()


# Create FastAPI app with lifespan
app = FastAPI(
    title="E-Commerce API",
    description="Days 36-38 Portfolio Project – 90-Day Backend Engineering Journey",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(v1_router)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        Status and version information.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
    }
@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "E-Commerce API is running!"}