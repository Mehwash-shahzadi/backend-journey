from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    async def create_user_with_validation(self, data):
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise Exception("Email already exists")

        if data.age < 0:
            raise Exception("Age cannot be negative")

        username = data.name.lower().replace(" ", "") + "123"

        return await self.repo.create(data.name, data.email, data.age)

    async def get_users(self):
        return await self.repo.get_all()
