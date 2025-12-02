from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import Post

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str, content: str, author: str):
        post = Post(title=title, content=content, author=author)
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post, ["tags"])
        return post

    async def get_by_id(self, post_id: int):
        result = await self.db.execute(
            select(Post)
            .where(Post.id == post_id)
            .options(selectinload(Post.tags))
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(Post).options(selectinload(Post.tags))
        )
        return result.scalars().all()

    async def add_tag_to_post(self, post, tag):
        post.tags.append(tag)
        await self.db.commit()
        await self.db.refresh(post, ["tags"])
        return post