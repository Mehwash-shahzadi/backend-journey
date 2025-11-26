from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_user, get_users, update_user, delete_user
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    response_description="User created successfully"
)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    This endpoint creates a new user with the provided email and name.
    If the email already exists, it returns the existing user instead of creating a duplicate.

    Parameters:
        user (UserCreate): Request body containing email and name
        db (Session): Database session dependency

    Returns:
        UserOut: The created or existing user object with id, email, name, created_at, and posts

    Example Request:
        POST /users/
        {
            "email": "john.doe@example.com",
            "name": "John Doe"
        }
    """
    return create_user(db, email=user.email, name=user.name)


@router.get(
    "/",
    response_model=List[UserOut],
    response_description="List of users retrieved successfully"
)
def api_get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of all users.

    This endpoint returns a list of users with pagination support.
    Use skip and limit parameters to control the number of results.

    Parameters:
        skip (int): Number of records to skip for pagination (default: 0)
        limit (int): Maximum number of records to return (default: 10)
        db (Session): Database session dependency

    Returns:
        List[UserOut]: List of user objects

    Example Request:
        GET /users/?skip=0&limit=10
    """
    return get_users(db, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    response_description="User retrieved successfully"
)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by their ID.

    This endpoint fetches detailed information about a specific user,
    including their associated posts.

    Parameters:
        user_id (int): The unique identifier of the user
        db (Session): Database session dependency

    Returns:
        UserOut: The user object with all details

    Raises:
        HTTPException 404: If user with the given ID does not exist

    Example Request:
        GET /users/1
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserOut,
    response_description="User updated successfully"
)
def api_update_user(
    user_id: int,
    name: str,
    db: Session = Depends(get_db)
):
    """
    Update an existing user's name.

    This endpoint allows you to modify the name of an existing user.
    Only the name field can be updated through this endpoint.

    Parameters:
        user_id (int): The unique identifier of the user to update
        name (str): The new name for the user
        db (Session): Database session dependency

    Returns:
        UserOut: The updated user object

    Raises:
        HTTPException 404: If user with the given ID does not exist

    Example Request:
        PUT /users/1?name=Jane%20Doe
    """
    updated = update_user(db, user_id, name)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_description="User deleted successfully"
)
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    This endpoint permanently removes a user from the database.
    All posts and comments associated with this user will also be deleted due to cascade delete.

    Parameters:
        user_id (int): The unique identifier of the user to delete
        db (Session): Database session dependency

    Returns:
        dict: Success message confirming deletion

    Raises:
        HTTPException 404: If user with the given ID does not exist

    Example Request:
        DELETE /users/1
    """
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"detail": "User deleted successfully"}