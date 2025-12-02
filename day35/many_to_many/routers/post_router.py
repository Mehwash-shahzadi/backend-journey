from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from dependencies import get_db
from services.post_service import PostService
from schemas import PostCreate, PostSchema, TagAdd

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostSchema)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    service = PostService(db)
    return await service.create_post(post.title, post.content, post.author)

@router.get("/", response_model=List[PostSchema])
async def list_posts(db: AsyncSession = Depends(get_db)):
    service = PostService(db)
    return await service.get_all_posts()

@router.post("/{post_id}/tags", response_model=PostSchema)
async def add_tag_to_post(
    post_id: int,
    tag_data: TagAdd,
    db: AsyncSession = Depends(get_db)
):
    service = PostService(db)
    try:
        return await service.add_tag_to_post(post_id, tag_data.tag_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))