from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud, database

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@app.get("/posts/", response_model=List[schemas.PostSchema])
def read_posts(
    search: Optional[str] = None,
    author: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sort: str = "created_at",
    order: str = "desc",
    tags: Optional[List[str]] = Query(None),
    db: Session = Depends(database.get_db)
):
    posts = crud.get_posts(
        db, search=search, author=author, from_date=from_date,
        to_date=to_date, sort=sort, order=order, tags=tags
    )
    return posts
