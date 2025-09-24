# services/amadeus_services.py

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

def get_city_code(city_name: str) -> str:
    """
    Get IATA location code (city or airport) from city name using Amadeus API.
    Uses subType=CITY,AIRPORT to get both city and airport codes, returns the first match.
    """
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL.replace('/v2', '/v1')}/reference-data/locations"
    params = {
        "keyword": city_name,
        "subType": "CITY,AIRPORT",  # Get both city and airport codes
        "page[limit]": 1  # Get top result
    }
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data.get("data"):
        return data["data"][0]["iataCode"]
    raise ValueError(f"❌ No IATA code found for {city_name}")


def search_hotel_offers(city_code, check_in_date, check_out_date, adults=1, currency="USD", max_results=5):
    """
    Search hotels with prices and booking links via Amadeus API.
    First searches for hotel IDs by city, then gets offers.
    City code must be IATA/Amadeus recognized (e.g., 'PAR' for Paris).
    """
    # Step 1: Search for hotels by city to get hotelIds
    search_url = f"{BASE_URL.replace('/v2', '/v1')}/reference-data/locations/hotels/by-city"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    search_params = {
        "cityCode": city_code,
        "radius": 5,
        "radiusUnit": "KM"
    }
    
    try:
        search_resp = requests.get(search_url, headers=headers, params=search_params)
        search_resp.raise_for_status()
        search_data = search_resp.json()
        
        hotel_ids = [hotel["hotelId"] for hotel in search_data.get("data", [])[:max_results]]
        if not hotel_ids:
            print("❌ No hotels found in city search.")
            return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ Amadeus Hotel Search API Error: {e}")
        print(f"Response: {search_resp.text}")
        return []
    
    # Step 2: Get offers for the hotelIds
    offers_url = f"https://test.api.amadeus.com/v3/shopping/hotel-offers"
    offers_params = {
        "hotelIds": ",".join(hotel_ids),
        "adults": adults,
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "currency": currency
    }
    
    try:
        offers_resp = requests.get(offers_url, headers=headers, params=offers_params)
        offers_resp.raise_for_status()
        offers_data = offers_resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ Amadeus Hotel Offers API Error: {e}")
        print(f"Response: {offers_resp.text}")
        return []
    
    hotels = []
    for offer in offers_data.get("data", []):
        hotel_info = offer.get("hotel", {})
        offers = offer.get("offers", [])
        price = offers[0]["price"]["total"] if offers else None
        booking_url = offers[0].get("self") if offers else None

        hotels.append({
            "name": hotel_info.get("name"),
            "hotel_id": hotel_info.get("hotelId"),
            "latitude": hotel_info.get("latitude"),
            "longitude": hotel_info.get("longitude"),
            "address": hotel_info.get("address", {}).get("lines", []),
            "price": price,
            "currency": currency,
            "booking_url": booking_url
        })
    return hotels[:max_results]
