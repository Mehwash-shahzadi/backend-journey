from repositories.tag_repository import TagRepository

class TagService:
    def __init__(self, db):
        self.repo = TagRepository(db)

    async def create_tag(self, name: str):
        existing = await self.repo.get_by_name(name)
        if existing:
            raise Exception("Tag already exists")
        return await self.repo.create(name)

    async def get_all_tags(self):
        return await self.repo.get_all()

    async def get_tag_by_id(self, tag_id: int):
        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise Exception("Tag not found")
        return tag

    async def get_posts_by_tag(self, tag_id: int):
        tag = await self.repo.get_by_id(tag_id)
        if not tag:
            raise Exception("Tag not found")
        return await self.repo.get_posts_by_tag(tag_id)