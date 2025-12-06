"""
Security utilities for authentication and authorization.

Provides dependencies for user authentication, role-based access control,
and password hashing.
"""

from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status

from app.models import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto",bcrypt__ident="2b",bcrypt__default_rounds=12,)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Args:
        password: Plain-text password.

    Returns:
        Hashed password string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.

    Args:
        plain_password: Plain-text password to verify.
        hashed_password: Hashed password from database.

    Returns:
        True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


# def get_current_user() -> User:
#     """
#     Get the current authenticated user.

#     Placeholder for actual JWT/session-based authentication.
#     Will be implemented with real auth in future iterations.

#     Returns:
#         Current User instance.

#     Raises:
#         HTTPException: 401 if user is not authenticated.

#     Note:
#         This is a placeholder. In production, this would validate JWT tokens
#         or session cookies and return the authenticated user from the database.
#     """
#     # TODO: Implement actual authentication (JWT, session, etc.)
#     # For now, this is a placeholder that will be replaced
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Authentication required",
#     )
def get_current_user() -> User:
    """
    TEMPORARY FAKE ADMIN USER  ONLY FOR TESTING (Days 36-38)
    
    """
    from app.models import User
    
    return User(
        id=1,
        email="admin@shop.com",
        name="Super Admin",
        role="admin",                    # This makes get_admin_user() pass automatically
        hashed_password="fake-hashed-password-just-for-testing"
    )

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Protect route  only let admins through.

    Use it exactly like this:

        @router.delete("/categories/{id}")
        async def delete_category(category_id: int, admin: User = Depends(get_admin_user)):
            # only admins reach here
            ...

    Raises 403 if the user is not admin.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user