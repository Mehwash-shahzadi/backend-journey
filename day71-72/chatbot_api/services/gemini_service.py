from google import genai
import logging
from typing import AsyncGenerator, List
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

MAX_HISTORY_MESSAGES = 10  # Context window: keep last 10 messages

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_stream(
      self,
      history: List[dict],
      new_message: str,
      max_tokens: int = 800
  ) -> AsyncGenerator[str, None]:
      try:
        client = genai.Client(api_key=self.api_key)

        # === New: Context window management ===
        # Keep only the last 10 messages (trim old ones)
        MAX_HISTORY = 10
        trimmed_history = history[-MAX_HISTORY:]

        contents = trimmed_history + [{"role": "user", "parts": [{"text": new_message}]}]

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
        logger.error(f"Gemini streaming error: {str(e)}")
        yield f"data: Error: {str(e)}\n\n"
        yield "data: [DONE]\n\n"
