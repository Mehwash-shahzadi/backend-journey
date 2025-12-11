from fastapi import FastAPI
from app.modules.users.router import router as users_router
from app.database import engine, Base

def create_app() -> FastAPI:
    app = FastAPI(title="Day 46-47 JWT Auth")

    app.include_router(users_router)

    @app.on_event("startup")
    async def startup_event():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables checked/created automatically!")

    @app.get("/")
    async def root():
        return {"message": "Day 46-47 JWT Auth Running!"}

    return app

app = create_app()

