# app/modules/products/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db_session
from app.modules.products.service import get_product_service, list_products_service
from app.modules.products.schemas import ProductOut

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductOut])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
):
    products = await list_products_service(db, skip, limit)
    return products


@router.get("/{product_id}", response_model=ProductOut)
async def read_product(
    product_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    product = await get_product_service(db, product_id)
    return product