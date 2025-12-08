# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ecommerce_modular"
    SECRET_KEY: str = "your-secret-key-here"
    PROJECT_NAME: str = "Modular E-Commerce API"

    class Config:
        env_file = ".env"

settings = Settings()