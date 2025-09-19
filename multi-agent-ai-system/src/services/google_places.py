# google_places.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_PLACES_API_KEY not found in .env")

BASE_URL = "https://maps.googleapis.com/maps/api/place"

def search_places(query, place_type=None, location=None, radius=5000):
    """
    Search for places (hotels, attractions, restaurants) using Google Places API.
    """
    url = f"{BASE_URL}/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY,
    }
    if place_type:
        params["type"] = place_type
    if location:
        params["location"] = location
        params["radius"] = radius

    resp = requests.get(url, params=params)
    body = resp.json()
    results = body.get("results", [])
    status = body.get("status")
    if status != "OK" and status != "ZERO_RESULTS":
        # Log or raise depending on how you want to handle it
        return []

    places = []
    for r in results:
        photo_ref = None
        if r.get("photos") and isinstance(r["photos"], list) and len(r["photos"]) > 0:
            photo_ref = r["photos"][0].get("photo_reference")
        place = {
            "name": r.get("name"),
            "address": r.get("formatted_address"),
            "rating": r.get("rating"),
            "user_ratings_total": r.get("user_ratings_total"),
            "price_level": r.get("price_level"),
            "photo": get_photo_url(photo_ref) if photo_ref else None,
            "place_id": r.get("place_id")
        }
        places.append(place)

    return places

def get_photo_url(photo_reference, max_width=600):
    """
    Get photo URL from Google Places API.
    """
    return f"{BASE_URL}/photo?maxwidth={max_width}&photoreference={photo_reference}&key={GOOGLE_API_KEY}"

