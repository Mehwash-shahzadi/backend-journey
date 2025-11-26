from app.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    """
    FastAPI dependency that yields a database session.
    It ensures the session is closed after the request finishes.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
