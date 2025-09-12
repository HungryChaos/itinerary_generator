# query_parser.py
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
from pydantic import BaseModel, validator
import re
import dateparser
from typing import List, Optional
import requests
import json

class Query(BaseModel):
    destination: str
    start_date: Optional[str]
    end_date: Optional[str]
    budget: Optional[float]
    currency: Optional[str] = "INR"
    preferences: List[str] = []

# Gemini API call function
def call_gemini(prompt: str) -> dict:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    resp = requests.post(url, headers=headers, params=params, json=data)
    resp.raise_for_status()
    reply = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(reply)

def parse_free_text(text: str) -> Query:
    prompt = f"""Extract JSON with keys destination, start_date, end_date, budget, currency, preferences from:\n{text}\nReturn only JSON."""
    result = call_gemini(prompt)
    return Query(**result)
