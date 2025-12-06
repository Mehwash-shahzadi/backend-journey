"""
Database engine and session management.

Provides async engine, session factory, and get_async_session() dependency for FastAPI.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.models import Base  # Import Base to register all models


# Create async engine
settings = get_settings()
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Async session factory
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a fresh AsyncSession for each request.

    Usage:
        session: AsyncSession = Depends(get_async_session)

    Session is auto-committed / rolled back and closed at the end of the request.
    """

    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    """
    Initialize the database by creating all tables.

    Call this during application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close the database engine.

    Call this during application shutdown.
    """
    await engine.dispose()