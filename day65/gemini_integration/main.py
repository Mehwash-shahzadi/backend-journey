from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
from services.gemini_service import GeminiService

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gemini Integration API")

# Dependency to get Gemini service
async def get_gemini_service():
    return GeminiService(API_KEY)

# Request model for validation
class GenerateRequest(BaseModel):
    prompt: str  # Required, non-empty string

@app.post("/ai/generate")
async def generate_text(request: GenerateRequest, gemini: GeminiService = Depends(get_gemini_service)):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    logger.info(f"Received generation request: {request.prompt[:50]}...")
    try:
        response_text = await gemini.generate_text(request.prompt)
        return {"response": response_text}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)