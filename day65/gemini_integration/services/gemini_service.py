from google import genai
from google.genai import errors  
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str):
        # Create client with API key 
        self.client = genai.Client(api_key=api_key)

    async def generate_text(self, prompt: str) -> str:
        try:
            
            response = await self.client.aio.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt
            )
            logger.info(f"Generated response for prompt: {prompt[:50]}...")
            return response.text
        except errors.APIError as e:
            logger.error(f"Gemini API error: {e.code} - {e.message}")
            raise ValueError(f"Gemini API error ({e.code}): {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ValueError("An unexpected error occurred during generation.")