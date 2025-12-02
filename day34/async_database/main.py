from fastapi import FastAPI
from routers.user_router import router as user_router

app = FastAPI(title="Async User API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "API is running. Visit /docs for Swagger UI"}

app.include_router(user_router)