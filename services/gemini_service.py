import os
from pathlib import Path

from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
        self.client = genai.Client(api_key=api_key)
        # Use a model that is currently available in the Gemini API
        self.model_id = 'gemini-2.5-flash'

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_content(self, prompt: str) -> str:
        """
        Calls the Gemini API with retry logic for robustness against transient failures.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            raise e
