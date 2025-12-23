from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal

from app.modules.products.models import Product, Category, Review
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductOut, CategoryOut, ReviewCreate, ReviewOut


def get_products(db: Session, skip: int = 0, limit: int = 10, name: Optional[str] = None, category_id: Optional[int] = None, min_price: Optional[Decimal] = None, max_price: Optional[Decimal] = None) -> List[ProductOut]:
    query = db.query(Product).outerjoin(Category)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    products = query.offset(skip).limit(limit).all()
    result = []
    for p in products:
        avg_rating = db.query(func.avg(Review.rating)).filter(Review.product_id == p.id).scalar()
        review_count = db.query(func.count(Review.id)).filter(Review.product_id == p.id).scalar()
        category_out = CategoryOut(id=p.category.id, name=p.category.name) if p.category else None
        result.append(ProductOut(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            stock=p.stock,
            category=category_out,
            avg_rating=avg_rating,
            review_count=review_count
        ))
    return result


def get_product_by_id(db: Session, product_id: int) -> Optional[ProductOut]:
    p = db.query(Product).outerjoin(Category).filter(Product.id == product_id).first()
    if not p:
        return None
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.product_id == p.id).scalar()
    review_count = db.query(func.count(Review.id)).filter(Review.product_id == p.id).scalar()
    reviews = db.query(Review).filter(Review.product_id == p.id).all()
    category_out = CategoryOut(id=p.category.id, name=p.category.name) if p.category else None
    return ProductOut(
        id=p.id,
        name=p.name,
        description=p.description,
        price=p.price,
        stock=p.stock,
        category=category_out,
        avg_rating=avg_rating,
        review_count=review_count
    )


def create_product(db: Session, product: ProductCreate) -> Product:
    category = None
    if product.category_name:
        category = db.query(Category).filter(Category.name == product.category_name).first()
        if not category:
            category = Category(name=product.category_name)
            db.add(category)
    
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=category.id if category else None
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product(db: Session, product_id: int, update_data: ProductUpdate) -> Optional[Product]:
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return p


def delete_product(db: Session, product_id: int) -> bool:
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True


def create_review(db: Session, product_id: int, user_id: int, review: ReviewCreate) -> Review:
    new_review = Review(product_id=product_id, user_id=user_id, **review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


def get_reviews_for_product(db: Session, product_id: int) -> List[ReviewOut]:
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    return [ReviewOut(id=r.id, user_id=r.user_id, rating=r.rating, comment=r.comment, created_at=r.created_at) for r in reviews]