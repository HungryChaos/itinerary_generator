# agents/hotel_agent.py
from services.amadeus_services import search_hotel_offers
from services.google_places import search_places
from agents.query_parser import TripQuery


class HotelAgent:
    def __init__(self):
        # Remove manual city_codes dict – no longer needed
        pass

    def get_hotels(self, trip_query: TripQuery, max_results: int = 5):
        from services.amadeus_services import get_city_code  # Import here to avoid circular imports
        
        destination = trip_query.destination
        try:
            city_code = get_city_code(destination)
        except ValueError as e:
            print(f"Warning: {e}. Using fallback.")
            city_code = destination.upper()[:3]  # Fallback if API fails
        
        # Get hotels with prices from Amadeus
        amadeus_hotels = search_hotel_offers(
            city_code=city_code,
            check_in_date=trip_query.start_date,
            check_out_date=trip_query.end_date,
            adults=trip_query.travelers or 1,
            currency=trip_query.currency or "INR",
            max_results=max_results
        )

        # Enrich with Google Places data (photos, ratings)
        enriched_hotels = []
        for hotel in amadeus_hotels:
            hotel_name = hotel.get("name")
            if hotel_name:
                # Search Google Places for this hotel to get photos/ratings
                google_results = search_places(f"{hotel_name} {destination}", place_type="lodging")
                if google_results:
                    google_hotel = google_results[0]  # Take the first match
                    hotel["rating"] = google_hotel.get("rating")
                    hotel["user_ratings_total"] = google_hotel.get("user_ratings_total")
                    hotel["photo"] = google_hotel.get("photo")
                    hotel["price_level"] = google_hotel.get("price_level")

            # Keep only relevant info for frontend
            enriched_hotels.append({
                "name": hotel.get("name"),
                "address": " ".join(hotel.get("address", [])),
                "price": hotel.get("price"),
                "currency": hotel.get("currency"),
                "rating": hotel.get("rating"),
                "user_ratings_total": hotel.get("user_ratings_total"),
                "photo": hotel.get("photo"),
                "booking_url": hotel.get("booking_url"),
                "hotel_id": hotel.get("hotel_id")
            })

        return enriched_hotels