from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.comment import CommentCreate, CommentOut
from app.crud.comment import create_comment, get_comments_for_post
from app.dependencies import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut)
def api_create_comment(payload: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, payload.content, payload.post_id)

@router.get("/post/{post_id}", response_model=List[CommentOut])
def api_get_comments_for_post(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_comments_for_post(db, post_id, skip=skip, limit=limit)
