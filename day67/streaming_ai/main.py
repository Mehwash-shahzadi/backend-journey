from fastapi import FastAPI, Depends, Request, Query , HTTPException 
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import logging
from services.gemini_service import GeminiService

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gemini Streaming Chat")

app.state.chat_history: list[dict] = [] 
def get_gemini() -> GeminiService:
    return GeminiService(API_KEY)

class Message(BaseModel):
    text: str
@app.get("/ai/stream")
async def stream_chat_get(
    text: str = Query(...),  
    gemini: GeminiService = Depends(get_gemini)
):
    if not text.strip():
        raise HTTPException(400, "Empty message")

    logger.info(f"Streaming GET request: {text[:50]}...")

    async def event_generator():
        async for chunk in gemini.generate_stream(
            app.state.chat_history,
            text
        ):
            yield chunk

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )
@app.post("/ai/stream")
async def stream_chat(
    msg: Message,
    gemini: GeminiService = Depends(get_gemini)
):
    if not msg.text.strip():
        return {"error": "Empty message"}

    logger.info(f"Streaming request: {msg.text[:50]}...")

    async def event_generator():
        async for chunk in gemini.generate_stream(
            app.state.chat_history,
            msg.text
        ):
            yield chunk

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )