from fastapi import HTTPException

def get_pagination(skip: int = 0, limit: int = 10):
    """Utility function to handle pagination parameters."""
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="skip must be >= 0 and limit must be > 0")
    return {"skip": skip, "limit": limit}

def get_user_by_id(user_id: int):
    """
    Reusable dependency to validate that a user exists.
    Returns the user object if found, otherwise raises 404.
    """
    from main import users   

    for user in users:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")
