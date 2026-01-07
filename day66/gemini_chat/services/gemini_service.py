from google import genai
from google.genai import types  
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_chat_response(self, history: list[dict], new_message: str) -> dict:
        try:
            client = genai.Client(api_key=self.api_key)
            system_instruction = (
                "You are a helpful backend mentor. "
                "Respond in exactly 4-5 clear lines. "
                "Be informative, practical, and encouraging. "
                "Use bullet points or numbered steps if it helps clarity. "
                "Never be verbose or repetitive."
            )

            contents = history + [{"role": "user", "parts": [{"text": new_message}]}]

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=1500  
                )
            )

            response_text = response.text or "(No response)"

            updated_history = contents + [{"role": "model", "parts": [{"text": response_text}]}]

            usage = response.usage_metadata or type('obj', (object,), {
                'prompt_token_count': 0, 'candidates_token_count': 0, 'total_token_count': 0
            })()

            usage_dict = {
                "prompt_tokens": usage.prompt_token_count,
                "completion_tokens": usage.candidates_token_count,
                "total_tokens": usage.total_token_count
            }

            return {
                "response": response_text,
                "updated_history": updated_history,
                "usage": usage_dict
            }

        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            raise ValueError(f"Gemini API failed: {str(e)}")