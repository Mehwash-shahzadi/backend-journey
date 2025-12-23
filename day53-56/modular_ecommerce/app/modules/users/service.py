from sqlalchemy.orm import Session
from typing import List

from app.modules.auth.models import User
from app.modules.users.models import UserUpdate, UserPublic, UserOut
from app.shared.exceptions import NotFoundException
from .repository import get_user_by_id, update_user, get_users


def get_my_profile(current_user: User) -> User:
    return current_user


def update_my_profile(db: Session, current_user: User, update_data: UserUpdate) -> User:
    return update_user(db, current_user, update_data.full_name, update_data.bio)


def get_user_public(db: Session, user_id: int) -> UserPublic:
    user = get_user_by_id(db, user_id)
    if not user:
        raise NotFoundException("User not found")
    return UserPublic(id=user.id, full_name=user.full_name, bio=user.bio, created_at=user.created_at)


def get_users_admin(db: Session, skip: int = 0, limit: int = 10) -> List[UserOut]:
    users = get_users(db, skip, limit)
    return [UserOut(id=u.id, email=u.email, role=u.role, full_name=u.full_name, bio=u.bio, created_at=u.created_at) for u in users]