import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use environment variable if available (recommended in production)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:route@localhost:5432/test_db"
)

# engine and session factory
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()
