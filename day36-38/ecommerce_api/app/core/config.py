"""
Application configuration and settings.

Loads configuration from environment variables using python-dotenv.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: Async PostgreSQL connection string.
        DEBUG: Debug mode flag.
    """

    DATABASE_URL: str = "postgresql+asyncpg://postgres:route@localhost:5432/ecommerce_db"
    DEBUG: bool = False

    class Config:
        """Pydantic config for loading from .env file."""
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Singleton Settings instance.
    """
    return Settings()