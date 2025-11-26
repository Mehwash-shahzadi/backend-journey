from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User

def create_user(db: Session, email: str, name: str) -> User:
    """
    Create a new user.

    If email already exists, return the existing user.
    """
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing

    user = User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Return paginated list of users.
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, name: str) -> Optional[User]:
    """
    Update user name.
    """
    user = get_user(db, user_id)
    if not user:
        return None

    user.name = name
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    """
    Delete a user by ID.
    """
    user = get_user(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user
