from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.comment import CommentCreate, CommentOut
from app.crud.comment import create_comment, get_comments_for_post
from app.dependencies import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
    response_description="Comment created successfully"
)
def api_create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    """
    Create a new comment on a blog post.

    This endpoint creates a new comment associated with a specific post.
    The post_id must reference an existing post in the database.

    Parameters:
        payload (CommentCreate): Request body containing content and post_id
        db (Session): Database session dependency

    Returns:
        CommentOut: The created comment object with id, post_id, content, and created_at

    Example Request:
        POST /comments/
        {
            "content": "Great post! Very informative.",
            "post_id": 1
        }
    """
    return create_comment(db, payload.content, payload.post_id)


@router.get(
    "/post/{post_id}",
    response_model=List[CommentOut],
    response_description="Comments retrieved successfully"
)
def api_get_comments_for_post(
    post_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all comments for a specific post.

    This endpoint returns a paginated list of comments associated with a given post ID.
    Comments are returned in the order they were created.

    Parameters:
        post_id (int): The unique identifier of the post
        skip (int): Number of records to skip for pagination (default: 0)
        limit (int): Maximum number of records to return, between 1 and 500 (default: 100)
        db (Session): Database session dependency

    Returns:
        List[CommentOut]: List of comment objects for the specified post

    Example Requests:
        GET /comments/post/1
        GET /comments/post/1?skip=0&limit=50
    """
    return get_comments_for_post(db, post_id, skip, limit)