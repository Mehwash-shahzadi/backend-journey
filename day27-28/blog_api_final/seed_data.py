"""
Seed the database with demo users, posts and comments.

Run:
    python seed_data.py
"""
from app.database import SessionLocal, engine
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.database import Base

def seed():
    # create tables if missing
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # simple idempotent approach: only seed if no users exist
        if db.query(User).count() > 0:
            print("Seed data already present. Skipping.")
            return

        u1 = User(name="Zara", email="zara@example.com")
        u2 = User(name="Boby", email="boby@example.com")
        db.add_all([u1, u2])
        db.commit()
        db.refresh(u1); db.refresh(u2)

        p1 = Post(title="Hello World", content="My first post", user_id=u1.id)
        p2 = Post(title="FastAPI Tips", content="Use Pydantic and SQLAlchemy", user_id=u2.id)
        db.add_all([p1, p2])
        db.commit()
        db.refresh(p1); db.refresh(p2)

        c1 = Comment(content="Nice post!", post_id=p1.id)
        c2 = Comment(content="Good tips", post_id=p2.id)
        db.add_all([c1, c2])
        db.commit()

        print("Seed data inserted.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
