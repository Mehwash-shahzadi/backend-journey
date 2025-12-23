from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.shared.exceptions import UnauthorizedException, ForbiddenException
from app.modules.auth.service import verify_token
from app.database import get_db
from app.modules.auth.models import User, Permission, role_permissions


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = verify_token(token)
    user_id: int = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise UnauthorizedException("User not found or inactive")
    return user


def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise ForbiddenException("Insufficient permissions")
        return current_user
    return role_checker


def require_permission(required_permission: str):
    def permission_checker(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Check if user's role has the permission
        perm = db.query(Permission).filter(Permission.name == required_permission).first()
        if not perm:
            raise ForbiddenException("Permission not found")
        role_perm = db.execute(select(role_permissions).where(
            role_permissions.c.role == current_user.role,
            role_permissions.c.permission_id == perm.id
        )).first()
        if not role_perm:
            raise ForbiddenException("Insufficient permissions")
        return current_user
    return permission_checker