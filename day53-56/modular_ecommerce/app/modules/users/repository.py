from sqlalchemy.orm import Session
from typing import List

from app.modules.auth.models import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user: User, full_name: str | None = None, bio: str | None = None) -> User:
    if full_name is not None:
        user.full_name = full_name
    if bio is not None:
        user.bio = bio
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()