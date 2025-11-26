from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from app.models.user import User

def create_user(db: Session, email: str, name: str) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing
    user = User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, name: str) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None
    user.name = name
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user
