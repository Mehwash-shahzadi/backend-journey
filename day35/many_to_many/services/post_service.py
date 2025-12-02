from repositories.post_repository import PostRepository
from repositories.tag_repository import TagRepository

class PostService:
    def __init__(self, db):
        self.repo = PostRepository(db)
        self.tag_repo = TagRepository(db)

    async def create_post(self, title: str, content: str, author: str):
        return await self.repo.create(title, content, author)

    async def get_all_posts(self):
        return await self.repo.get_all()

    async def get_post_by_id(self, post_id: int):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise Exception("Post not found")
        return post

    async def add_tag_to_post(self, post_id: int, tag_name: str):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise Exception("Post not found")
        
        tag = await self.tag_repo.get_by_name(tag_name)
        if not tag:
            raise Exception("Tag not found")
        
        if tag in post.tags:
            raise Exception("Tag already added to post")
        
        return await self.repo.add_tag_to_post(post, tag)