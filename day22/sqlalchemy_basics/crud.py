from sqlalchemy.orm import Session
from models import User


def create_user(db: Session, email: str, name: str):
    # Check if email already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print(f"User with email {email} already exists!")
        return existing

    user = User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    """Return all users."""
    return db.query(User).all()


def get_user_by_email(db: Session, email: str):
    """Return a user matching the email."""
    return db.query(User).filter(User.email == email).first()


def update_user_name(db: Session, user_id: int, new_name: str):
    """Update a user's name."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = new_name
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """Delete a user from database."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
