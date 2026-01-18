from fastapi import FastAPI
from routers.chat import router as chat_router
from routers.ai_features import router as ai_router

app = FastAPI(title="AI Chatbot Backend - Day 69-72")

app.include_router(chat_router)
app.include_router(ai_router)  # NEW: Add AI features router