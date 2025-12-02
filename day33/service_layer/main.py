from fastapi import FastAPI
from database import Base, engine
from routers.user_router import router as user_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include user router
app.include_router(user_router)
