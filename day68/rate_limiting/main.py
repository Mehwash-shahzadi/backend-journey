from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
from services.gemini_service import GeminiService
from services.usage_tracker import UsageTracker, BUDGET_LIMIT_USD
from models.usage import UserUsageSummary

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gemini – Rate Limited & Cost Controlled")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.state.chat_history: list[dict] = []  # demo only

def get_gemini():
    return GeminiService(API_KEY)

class Message(BaseModel):
    text: str

@app.post("/ai/stream")
@limiter.limit("5/minute")
async def stream_chat(
    request: Request,
    msg: Message,
    gemini: GeminiService = Depends(get_gemini)
):
    client_ip = request.client.host
    logger.info(f"Request from {client_ip}: {msg.text[:50]}...")

    summary = UsageTracker.get_summary(client_ip)
    if summary.is_blocked:
        raise HTTPException(
            status_code=429,
            detail=f"Monthly budget (${BUDGET_LIMIT_USD}) exceeded."
        )

    async def event_generator():
        full_response = ""
        async for chunk in gemini.generate_stream(app.state.chat_history, msg.text):
            if chunk.startswith("data: "):
                text_chunk = chunk[6:].strip()
                if text_chunk != "[DONE]":
                    full_response += text_chunk
            yield chunk

        # Record approximate usage
        approx_usage = {
            "prompt_tokens": len(msg.text) // 4,
            "completion_tokens": len(full_response) // 4,
        }
        approx_usage["total_tokens"] = approx_usage["prompt_tokens"] + approx_usage["completion_tokens"]
        approx_usage["estimated_cost_usd"] = UsageTracker.calculate_cost(
            approx_usage["prompt_tokens"], approx_usage["completion_tokens"]
        )

        UsageTracker.record_usage(client_ip, approx_usage)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )

@app.get("/ai/usage")
async def get_usage(request: Request):
    client_ip = request.client.host
    return UsageTracker.get_summary(client_ip)