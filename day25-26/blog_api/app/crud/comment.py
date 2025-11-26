from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.comment import Comment

def create_comment(db: Session, content: str, post_id: int) -> Comment:
    comment = Comment(content=content, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comment(db: Session, comment_id: int) -> Optional[Comment]:
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comments_for_post(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

def delete_comment(db: Session, comment_id: int) -> Optional[Comment]:
    comment = get_comment(db, comment_id)
    if not comment:
        return None
    db.delete(comment)
    db.commit()
    return comment
