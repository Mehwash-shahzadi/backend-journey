from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from dependencies import get_db
from services.tag_service import TagService
from schemas import TagCreate, TagSchema, PostSchema

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=TagSchema)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    try:
        return await service.create_tag(tag.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TagSchema])
async def list_tags(db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    return await service.get_all_tags()

@router.get("/{tag_id}/posts", response_model=List[PostSchema])
async def get_posts_by_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    try:
        return await service.get_posts_by_tag(tag_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))