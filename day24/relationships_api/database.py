from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://postgres:route@localhost/fastapi_db"

# Create engine to connect with PostgreSQL
engine = create_engine(DATABASE_URL)

# Create session maker (opens/closes DB connection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()
