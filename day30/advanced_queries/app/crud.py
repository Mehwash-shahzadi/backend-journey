from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import models
from datetime import datetime

def get_posts(
    db: Session,
    search: str = None,
    author: str = None,
    from_date: str = None,
    to_date: str = None,
    sort: str = "created_at",
    order: str = "desc",
    tags: list = None
):
    query = db.query(models.Post)

    # Search
    if search:
        query = query.filter(
            or_(
                models.Post.title.ilike(f"%{search}%"),
                models.Post.content.ilike(f"%{search}%")
            )
        )

    # Filter by author
    if author:
        query = query.filter(models.Post.author == author)

    # Filter by date range
    if from_date and to_date:
        query = query.filter(
            models.Post.created_at.between(from_date, to_date)
        )

    # Filter by tags
    if tags:
        query = query.join(models.Post.tags).filter(models.Tag.name.in_(tags))

    # Sorting
    if order == "desc":
        query = query.order_by(getattr(models.Post, sort).desc())
    else:
        query = query.order_by(getattr(models.Post, sort).asc())

    return query.all()
