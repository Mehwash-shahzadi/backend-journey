import asyncio
from app.database.db import async_session_factory
from app.models import User
from app.core.security import hash_password  
from sqlalchemy import text

async def create_first_user():
    async with async_session_factory() as session:
        async with session.begin():
            # Use `text()` for raw SQL query
            result = await session.execute(text("SELECT 1 FROM users WHERE id = 1"))
            if result.fetchone():
                print("User ID 1 already exists")
                return

            user = User(
                id=1,  # Force ID 1 so fake admin matches
                email="admin@shop.com",
                name="Admin User",
                role="admin",
                hashed_password=hash_password("admin123")
            )
            session.add(user)
            await session.commit()
            print("Created real user: ID=1, admin@shop.com / admin123")


if __name__ == "__main__":
    asyncio.run(create_first_user())
