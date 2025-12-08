# app/modules/products/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.products.repository import get_product_by_id, get_products

async def get_product_service(db: AsyncSession, product_id: int):
    return await get_product_by_id(db, product_id)


async def list_products_service(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await get_products(db, skip, limit)