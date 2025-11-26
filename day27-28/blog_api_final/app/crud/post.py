from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from app.models.post import Post
from app.models.user import User

def create_post(db: Session, title: str, content: str, user_id: int) -> Post:
    """
    Create a new post for a user.
    """
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: int) -> Optional[Post]:
    """
    Get a post by ID.
    """
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    sort: str = "created_at",
    desc: bool = True,
    user_id: Optional[int] = None,
    search: Optional[str] = None
) -> List[Post]:
    """
    Retrieve list of posts with filtering, sorting, search, pagination.
    """
    q = db.query(Post)

    if user_id is not None:
        q = q.filter(Post.user_id == user_id)

    if search:
        q = q.filter(Post.title.ilike(f"%{search}%"))

    sort_col = getattr(Post, sort, None)
    if sort_col is not None:
        q = q.order_by(sort_col.desc() if desc else sort_col.asc())

    return q.offset(skip).limit(limit).all()


def get_posts_for_user(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user and eagerly load all associated posts.
    """
    return (
        db.query(User)
        .options(selectinload(User.posts))
        .filter(User.id == user_id)
        .first()
    )


def update_post(db: Session, post_id: int, title: str, content: str) -> Optional[Post]:
    """
    Update an existing post by ID.
    """
    post = get_post(db, post_id)
    if not post:
        return None

    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int) -> Optional[Post]:
    """
    Delete a post by ID.
    """
    post = get_post(db, post_id)
    if not post:
        return None

    db.delete(post)
    db.commit()
    return post
