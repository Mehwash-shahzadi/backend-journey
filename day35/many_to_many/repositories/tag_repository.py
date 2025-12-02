from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import Tag, Post

class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str):
        tag = Tag(name=name)
        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)
        return tag

    async def get_by_name(self, name: str):
        result = await self.db.execute(
            select(Tag).where(Tag.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, tag_id: int):
        result = await self.db.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(select(Tag))
        return result.scalars().all()

    async def get_posts_by_tag(self, tag_id: int):
        result = await self.db.execute(
            select(Tag)
            .where(Tag.id == tag_id)
            .options(selectinload(Tag.posts).selectinload(Post.tags))
        )
        tag = result.scalar_one_or_none()
        if tag:
            return tag.posts
        return []