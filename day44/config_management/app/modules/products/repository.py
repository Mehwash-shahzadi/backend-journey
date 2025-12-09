from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.products.models import Product
from app.shared.exceptions import NotFoundException

async def get_product_by_id(db: AsyncSession, product_id: int) -> Product:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise NotFoundException("Product not found")
    return product


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()