from fastapi import FastAPI
from app.modules.users.router import router as users_router

def create_app() -> FastAPI:
    app = FastAPI(title="Day 49 RBAC")

    app.include_router(users_router)

    @app.get("/")
    async def root():
        return {"message": "Day 49 RBAC Running!"}

    return app

app = create_app()