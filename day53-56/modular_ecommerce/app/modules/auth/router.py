from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.modules.auth.models import User, RefreshToken
from app.modules.auth.schemas import Register, Token, UserOut
from app.modules.auth.service import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
from app.modules.auth.repository import create_user, get_user_by_email, create_refresh_token as repo_create_refresh_token, get_refresh_token, revoke_refresh_token
from app.config import settings
from app.shared.exceptions import ConflictException, UnauthorizedException


router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
def register(user: Register, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise ConflictException("Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = create_user(db, user.email, hashed_pw)
    return new_user


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException("Incorrect email or password")
    if not user.is_active:
        raise UnauthorizedException("User inactive")
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token_str = create_refresh_token(data={"sub": str(user.id)})
    # Store refresh token
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    repo_create_refresh_token(db, refresh_token_str, user.id, expires_at)
    return {"access_token": access_token, "refresh_token": refresh_token_str}


@router.post("/token/refresh", response_model=Token)
def refresh_token_endpoint(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_token(refresh_token)
    user_id: int = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Invalid refresh token")
    db_token = get_refresh_token(db, refresh_token)
    if not db_token or db_token.revoked or db_token.expires_at < datetime.utcnow():
        raise UnauthorizedException("Invalid or expired refresh token")
    user = get_user_by_email(db, "")  
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or inactive")
    new_access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": new_access_token, "refresh_token": refresh_token}


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    revoke_refresh_token(db, refresh_token)
    return {"message": "Logged out"}