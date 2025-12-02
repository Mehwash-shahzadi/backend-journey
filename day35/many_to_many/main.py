from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from routers.post_router import router as post_router
from routers.tag_router import router as tag_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Posts & Tags API", lifespan=lifespan)

app.include_router(post_router)
app.include_router(tag_router)

@app.get("/")
async def root():
    return {"message": "Posts & Tags API is running"}