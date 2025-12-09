import asyncio
from sqlalchemy import text
from app.database import async_session_factory
from app.models import Category, Product

async def seed_data():
    async with async_session_factory() as session:
        async with session.begin():
            # only skip if ALL 5 seed categories already exist
            result = await session.execute(text("SELECT name FROM categories"))
            existing_names = {row[0] for row in result.fetchall()}

            seed_names = {"Electronics", "Books", "Clothing", "Home Appliances", "Sports"}

            if seed_names.issubset(existing_names):
                print("All 5 seed categories already exist – skipping")
                return

            print("Seeding fresh data...")
    

            # 5 Categories
            categories = [
                Category(name="Electronics", description="Phones, laptops, gadgets"),
                Category(name="Books", description="Fiction & non-fiction books"),
                Category(name="Clothing", description="T-shirts, jeans, jackets"),
                Category(name="Home Appliances", description="Kitchen and home devices"),
                Category(name="Sports", description="Gym & outdoor equipment"),
            ]
            session.add_all(categories)
            await session.flush()  # Get IDs

            # 5 Products
            products = [
                Product(name="iPhone 15 Pro", price=1299.99, stock=30, categories=[categories[0]]),
                Product(name="Python Crash Course", price=29.99, stock=200, categories=[categories[1]]),
                Product(name="Nike Air Max", price=149.99, stock=80, categories=[categories[2]]),
                Product(name="Microwave Oven", price=89.99, stock=15, categories=[categories[3]]),
                Product(name="Yoga Mat Premium", price=24.99, stock=150, categories=[categories[4]]),
            ]
            session.add_all(products)

        await session.commit()
        print("Seed completed! 5 categories + 5 products inserted")
        


if __name__ == "__main__":
    asyncio.run(seed_data())