from fastapi import FastAPI
from app.modules.users.router import router as users_router

def create_app() -> FastAPI:
    app = FastAPI(title="Day 48 OAuth2 Flow")

    app.include_router(users_router)

    @app.get("/")
    async def root():
        return {"message": "Day 48 OAuth2 Flow Running!"}

    return app

app = create_app()