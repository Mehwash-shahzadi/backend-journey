from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
from services.gemini_service import GeminiService

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gemini Chat API")

app.state.chat_history: list[dict] = []

def get_gemini_service() -> GeminiService:
    return GeminiService(API_KEY)

class ChatRequest(BaseModel):
    message: str 

@app.post("/ai/chat")
def chat_completion(
    request: ChatRequest,
    gemini: GeminiService = Depends(get_gemini_service)
):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    logger.info(f"Chat message received: {request.message[:50]}...")

    try:
        result = gemini.generate_chat_response(app.state.chat_history, request.message)
        
        # Update server history
        app.state.chat_history = result["updated_history"]
        
        return {
            "response": result["response"],
            "usage": result["usage"]
        }


    except ValueError as e:
        raise HTTPException(status_code=503 if "overloaded" in str(e) else 500, detail=str(e))