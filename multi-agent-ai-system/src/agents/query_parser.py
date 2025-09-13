import os
import json
from typing import List, Optional
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------
# Load API key from .env
# --------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)


# --------------------
# Pydantic schema for structured output
# --------------------
class TripQuery(BaseModel):
    destination: str
    start_date: Optional[str] = None   # ISO format: YYYY-MM-DD
    end_date: Optional[str] = None
    budget: Optional[float] = None
    currency: Optional[str] = "INR"
    preferences: List[str] = []


# --------------------
# Gemini-powered parser
# --------------------
def parse_trip_request(user_input: str) -> TripQuery:
    """
    Convert free-text user input into structured TripQuery using Gemini.
    """

    system_prompt = f"""
    You are a travel assistant that extracts structured JSON from natural language trip requests.
    Always return ONLY valid JSON (no text before or after).
    Keys required: destination (string), start_date (YYYY-MM-DD if possible), end_date (YYYY-MM-DD if possible),
    budget (number), currency (3-letter code or INR if not specified), preferences (list of strings).
    """

    # Ask Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([system_prompt, user_input])

    # Try to parse JSON
    raw_text = response.text.strip()
    try:
        parsed = json.loads(raw_text)
        return TripQuery(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"❌ Failed to parse Gemini output: {e}\nOutput was: {raw_text}")


# --------------------
# Test locally
# --------------------
if __name__ == "__main__":
    test_input = "Plan me a 5-day Japan trip under ₹80,000 focused on food & culture."
    result = parse_trip_request(test_input)
    print("✅ Parsed Trip Query:")
    print(result.json(indent=2))
