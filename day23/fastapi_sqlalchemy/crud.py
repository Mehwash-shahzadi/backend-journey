from sqlalchemy.orm import Session
from models import User

def create_user(db: Session, email: str, name: str):
    new_user = User(email=email, name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, name: str):
    user = get_user_by_id(db, user_id)
    if user:
        user.name = name
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
