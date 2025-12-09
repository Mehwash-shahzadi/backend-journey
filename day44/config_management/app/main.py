from fastapi import FastAPI
from app.modules.users.router import router as users_router
from app.modules.products.router import router as products_router
from app.config import settings

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

    app.include_router(users_router)
    app.include_router(products_router)


    @app.get("/")
    async def root():
        return {"message": "Pydentic setting Day 44 Complete!"}
    
    @app.get("/config")
    async def show_config():
       from app.config import settings
       return {
            "project": settings.PROJECT_NAME,
            "debug": settings.DEBUG,
            "db_connected": True
              }

    return app

app = create_app()