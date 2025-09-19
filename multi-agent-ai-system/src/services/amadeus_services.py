# services/amadeus_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

if not AMADEUS_API_KEY or not AMADEUS_API_SECRET:
    raise ValueError("❌ Missing AMADEUS_API_KEY or AMADEUS_API_SECRET in .env")

# Amadeus base URL (test environment)
BASE_URL = "https://test.api.amadeus.com/v2"

# Token cache
ACCESS_TOKEN = None

def get_access_token():
    global ACCESS_TOKEN
    if ACCESS_TOKEN:
        return ACCESS_TOKEN

    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET
    }
    resp = requests.post(auth_url, data=data)
    resp.raise_for_status()
    ACCESS_TOKEN = resp.json()["access_token"]
    return ACCESS_TOKEN

def search_flights_api(origin, destination, departure_date, return_date=None, adults=1, currency="INR"):
    """
    Call Amadeus API to search for flights.
    """
    url = f"{BASE_URL}/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "currencyCode": currency,
        "max": 5  # top 5 results
    }
    if return_date:
        params["returnDate"] = return_date

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()
