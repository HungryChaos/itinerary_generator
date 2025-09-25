import os
import json
from typing import List, Optional
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)


# --------------------
# Pydantic schema for structured output
# --------------------
class TripQuery(BaseModel):
    origin: Optional[str] = None  # Starting location (e.g., city or airport code)
    destination: str
    start_date: Optional[str] = None   # ISO format: YYYY-MM-DD
    end_date: Optional[str] = None
    budget: Optional[float] = None
    currency: Optional[str] = "INR"
    trip_type: Optional[str] = "round-trip"  # one-way or round-trip
    travelers: Optional[int] = 1
    preferences: Optional[List[str]] = []  # e.g., ["food", "culture"]


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
    
    Required keys:
    - origin (string, e.g., starting city or airport)
    - destination (string)
    - start_date (YYYY-MM-DD if possible)
    - end_date (YYYY-MM-DD if possible)
    - budget (number, in currency units)
    - currency (3-letter code, default "INR" if not given)
    - preferences (list of strings, like ["food", "culture"])
    - trip_type ("one-way" or "round-trip")
    
    Rules:
    - If the user specifies both a start and end date, assume "round-trip".
    - If the user only specifies a start date or explicitly says "one-way", set trip_type="one-way".
    - If unsure, default to "round-trip".
    """
 
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([system_prompt, user_input])

    raw_text = response.text.strip()
    
    # Strip Markdown code blocks if present
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]  # Remove ```json
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]  # Remove ```
    raw_text = raw_text.strip()  # Clean whitespace
    
    try:
        parsed = json.loads(raw_text)
        return TripQuery(**parsed)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"❌ Failed to parse Gemini output: {e}\nOutput was: {raw_text}")


# --------------------
# Test locally
# --------------------
if __name__ == "__main__":
    test_input = "Plan me a one-way flight from new york to paris on 10th October under $60,000."
    result = parse_trip_request(test_input)
    print("✅ Parsed Trip Query:")
    print(result.model_dump_json(indent=2))
