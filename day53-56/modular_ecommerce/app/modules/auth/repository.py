from sqlalchemy.orm import Session
from datetime import datetime

from app.modules.auth.models import User, RefreshToken


def create_user(db: Session, email: str, hashed_password: str, role: str = "user", full_name: str | None = None, bio: str | None = None) -> User:
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        role=role,
        full_name=full_name,
        bio=bio
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_refresh_token(db: Session, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
    refresh_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token


def get_refresh_token(db: Session, token: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def revoke_refresh_token(db: Session, token: str) -> bool:
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if db_token:
        db_token.revoked = True
        db.commit()
        return True
    return False