from fastapi import FastAPI
from app.modules.users.router import router as users_router
from app.modules.permissions.router import router as permissions_router
from app.database import engine, Base

def create_app() -> FastAPI:
    app = FastAPI(title="Day 51-52 Permission System")

    app.include_router(users_router)
    app.include_router(permissions_router)  

    @app.get("/")
    async def root():
        return {"message": "Day 51-52 Permission System Running!"}

    return app

app = create_app()