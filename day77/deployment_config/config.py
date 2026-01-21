"""
Production-ready environment configuration with strict validation.
Loads from .env file and validates all settings before app starts.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field
from urllib.parse import urlparse
import os


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    Validates all values before allowing app to start.
    """

    #  Database 
    DATABASE_URL: str = Field(..., description="PostgreSQL connection string")
    
    #  Redis 
    REDIS_URL: str = Field(..., description="Redis connection string")
    
    #  API Keys
    GEMINI_API_KEY: str = Field(..., description="Google Gemini API key")
    OPENAI_API_KEY: str | None = Field(None, description="OpenAI API key (optional)")
    
    #  Security 
    SECRET_KEY: str = Field(..., description="Secret key for JWT tokens")
    ALGORITHM: str = Field("HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, ge=1, le=1440, description="Token expiry in minutes")
    
    #  Application 
    DEBUG: bool = Field(False, description="Debug mode (never True in production)")
    ENVIRONMENT: str = Field("production", description="Environment: development, staging, production")
    APP_NAME: str = Field("FastAPI Backend", description="Application name")
    API_VERSION: str = Field("1.0.0", description="API version")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="forbid",  # Reject unknown environment variables
        validate_default=True
    )

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Ensure ENVIRONMENT is one of the allowed values."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}, got {v}")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate PostgreSQL connection string format."""
        if not v:
            raise ValueError("DATABASE_URL is required")
        
        try:
            parsed = urlparse(v)
            if parsed.scheme not in ["postgresql", "postgres"]:
                raise ValueError("DATABASE_URL must use postgresql:// scheme")
            if not parsed.hostname:
                raise ValueError("DATABASE_URL must include hostname")
            if not parsed.path or parsed.path == "/":
                raise ValueError("DATABASE_URL must include database name")
        except Exception as e:
            raise ValueError(f"Invalid DATABASE_URL format: {str(e)}")
        
        return v

    @field_validator("REDIS_URL")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate Redis connection string format."""
        if not v:
            raise ValueError("REDIS_URL is required")
        
        try:
            parsed = urlparse(v)
            if parsed.scheme != "redis":
                raise ValueError("REDIS_URL must use redis:// scheme")
            if not parsed.hostname:
                raise ValueError("REDIS_URL must include hostname")
        except Exception as e:
            raise ValueError(f"Invalid REDIS_URL format: {str(e)}")
        
        return v

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Reject weak, default, or placeholder SECRET_KEY values."""
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        
        weak_keys = [
            "secret",
            "changeme",
            "change_me",
            "123456",
            "password",
            "your_secret_key",
            "your-secret-key",
            "secretkey",
            "development",
            "dev",
            "test",
        ]
        
        if v.lower() in weak_keys or v.startswith("your_"):
            raise ValueError(
                f"SECRET_KEY '{v}' is weak or placeholder. "
                "Use a strong, random key generated with secrets.token_urlsafe(32)"
            )
        
        return v

    @field_validator("DEBUG")
    @classmethod
    def validate_debug_for_production(cls, v: bool, info) -> bool:
        """Never allow DEBUG=True in production."""
        environment = info.data.get("ENVIRONMENT")
        
        if v and environment == "production":
            raise ValueError(
                "DEBUG cannot be True in production environment. "
                "This is a security risk. Set DEBUG=false."
            )
        
        return v

    @field_validator("GEMINI_API_KEY")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Reject placeholder API keys."""
        if not v or v.startswith("your_") or v == "placeholder":
            raise ValueError(
                "GEMINI_API_KEY is required and cannot be a placeholder. "
                "Get your key from Google Cloud Console."
            )
        return v

    class Config:
        """Pydantic config."""
        validate_assignment = True


# Create global settings instance (loaded on import)
settings = Settings()


def get_settings() -> Settings:
    """Dependency for FastAPI to inject settings."""
    return settings
