from google import genai
import logging
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_stream(
        self,
        history: list[dict],
        new_message: str,
        max_tokens: int = 800
    ) -> AsyncGenerator[str, None]:
        """
        Async generator that yields SSE formatted chunks from Gemini
        """
        try:
            client = genai.Client(api_key=self.api_key)

            contents = history + [{"role": "user", "parts": [{"text": new_message}]}]

            async for chunk in await client.aio.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents,
                config=genai.types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7
                )
            ):
                if chunk.text:
                    yield f"data: {chunk.text}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            yield f"data: Error: {str(e)}\n\n"
            yield "data: [DONE]\n\n"