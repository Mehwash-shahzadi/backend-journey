from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, post, comment  # package routers

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API (Day25-26)")

# include routers
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)

# root
@app.get("/")
def root():
    return {"message": "Blog API is up. Visit /docs for interactive docs."}

