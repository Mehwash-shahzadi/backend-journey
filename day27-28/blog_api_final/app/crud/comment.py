from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.comment import Comment

def create_comment(db: Session, content: str, post_id: int) -> Comment:
    """
    Create a new comment for a post.

    Args:
        db (Session): Database session.
        content (str): Comment text.
        post_id (int): ID of the post being commented on.

    Returns:
        Comment: The newly created comment object.
    """
    comment = Comment(content=content, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment(db: Session, comment_id: int) -> Optional[Comment]:
    """
    Retrieve a single comment by its ID.

    Args:
        db (Session): Database session.
        comment_id (int): Comment ID.

    Returns:
        Optional[Comment]: Found comment or None.
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_comments_for_post(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
    """
    List comments belonging to a specific post.

    Args:
        db (Session): Database session.
        post_id (int): Related post ID.
        skip (int): Offset for pagination.
        limit (int): Max number of results.

    Returns:
        List[Comment]: List of comments for the post.
    """
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_comment(db: Session, comment_id: int) -> Optional[Comment]:
    """
    Delete a comment by ID.

    Args:
        db (Session): Database session.
        comment_id (int): Comment ID.

    Returns:
        Optional[Comment]: Deleted comment or None.
    """
    comment = get_comment(db, comment_id)
    if not comment:
        return None

    db.delete(comment)
    db.commit()
    return comment
