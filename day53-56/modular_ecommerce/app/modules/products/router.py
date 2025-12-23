from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from app.database import get_db
from app.modules.auth.dependencies import get_current_user, require_permission
from app.modules.auth.models import User
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductOut, ReviewCreate, ReviewOut
from app.modules.products.service import get_products, get_product_by_id, create_product, update_product, delete_product, create_review, get_reviews_for_product


router = APIRouter()


@router.get("/", response_model=List[ProductOut])
def read_products(
    skip: int = 0,
    limit: int = Query(10, le=100),
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    db: Session = Depends(get_db)
):
    return get_products(db, skip, limit, name, category_id, min_price, max_price)


@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductOut)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db), _: User = Depends(require_permission("create:product"))):
    new_product = create_product(db, product)
    return get_product_by_id(db, new_product.id)


@router.put("/{product_id}", response_model=ProductOut)
def update_existing_product(product_id: int, update_data: ProductUpdate, db: Session = Depends(get_db), _: User = Depends(require_permission("edit:product"))):
    updated = update_product(db, product_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return get_product_by_id(db, product_id)


@router.delete("/{product_id}")
def delete_existing_product(product_id: int, db: Session = Depends(get_db), _: User = Depends(require_permission("delete:product"))):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}


@router.post("/{product_id}/reviews", response_model=ReviewOut)
def add_review(product_id: int, review: ReviewCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not get_product_by_id(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    new_review = create_review(db, product_id, current_user.id, review)
    return ReviewOut(id=new_review.id, user_id=new_review.user_id, rating=new_review.rating, comment=new_review.comment, created_at=new_review.created_at)