from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.post import PostCreate, PostOut
from app.crud.post import create_post, get_post, get_posts, get_posts_for_user, update_post, delete_post
from app.dependencies import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostOut)
def api_create_post(payload: PostCreate, db: Session = Depends(get_db)):
    # ensure user exists could be added (left to db foreign key)
    return create_post(db, payload.title, payload.content, payload.user_id)

@router.get("/", response_model=List[PostOut])
def api_get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query("created_at"),
    desc: bool = Query(True),
    user_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_posts(db, skip=skip, limit=limit, sort=sort, desc=desc, user_id=user_id, search=search)

@router.get("/{post_id}", response_model=PostOut)
def api_get_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/user/{user_id}", response_model=List[PostOut])
def api_get_user_posts(user_id: int, db: Session = Depends(get_db)):
    user = get_posts_for_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.posts


@router.put("/{post_id}", response_model=PostOut)
def api_update_post(post_id: int, title: str, content: str, db: Session = Depends(get_db)):
    updated = update_post(db, post_id, title, content)
    if not updated:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated

@router.delete("/{post_id}")
def api_delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted = delete_post(db, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}
