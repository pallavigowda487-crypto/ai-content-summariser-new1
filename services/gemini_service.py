import os
from pathlib import Path

from google import genai
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import dotenv_values, load_dotenv

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

root_env = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(root_env)
for key, value in dotenv_values(root_env).items():
    os.environ.setdefault(key, value)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not api_key and HAS_STREAMLIT:
            try:
                if "GOOGLE_API_KEY" in st.secrets:
                    api_key = st.secrets["GOOGLE_API_KEY"]
                elif "GEMINI_API_KEY" in st.secrets:
                    api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                pass

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable is not set. \n\n"
                "**How to fix this:**\n"
                "1. **Local Development:** Add `GOOGLE_API_KEY=your_key_here` to your `.env` file.\n"
                "2. **Streamlit Community Cloud:** Go to App Dashboard > Settings > Secrets and add `GOOGLE_API_KEY = \"your_key_here\"`.\n"
                "3. **Other Cloud Platforms (Render, Heroku, etc.):** Add `GOOGLE_API_KEY` to your Environment Variables settings."
            )
        
        self.client = genai.Client(api_key=api_key)
        # Use gemini-2.0-flash which has a much higher free-tier daily quota (1500 RPD vs 20 RPD)
        self.model_id = 'gemini-2.0-flash'

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
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
