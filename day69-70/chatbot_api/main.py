from fastapi import FastAPI
from routers.chat import router as chat_router

app = FastAPI(title="AI Chatbot Backend - Day 69")

app.include_router(chat_router)