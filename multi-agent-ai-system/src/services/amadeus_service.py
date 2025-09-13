import os
from amadeus import Client, ResponseError
from dotenv import load_dotenv

# --------------------
# Load API key
# --------------------
load_dotenv()
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

if not (AMADEUS_API_KEY and AMADEUS_API_SECRET):
    raise ValueError("❌ Amadeus API credentials missing in .env")

# --------------------
# Amadeus Agent
# --------------------
class AmadeusAgent:
    def __init__(self):
        self.client = Client(
            client_id=AMADEUS_API_KEY,
            client_secret=AMADEUS_API_SECRET
        )

    def search_flights(self, origin, destination, departure_date, end_date=None, trip_type="round-trip", adults=1):
        """
        Search flights using Amadeus API.
        - origin: IATA code of origin (e.g., DEL)
        - destination: IATA code of destination (e.g., NRT)
        - departure_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD (used if trip_type == "round-trip")
        - trip_type: "one-way" or "round-trip"
        """
        try:
            params = {
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departure_date,
                "adults": adults,
                "max": 5
            }

            if trip_type == "round-trip" and end_date:
                params["returnDate"] = end_date

            response = self.client.shopping.flight_offers_search.get(**params)
            return response.data

        except ResponseError as error:
            print("❌ Amadeus API Error:", error)
            return []
