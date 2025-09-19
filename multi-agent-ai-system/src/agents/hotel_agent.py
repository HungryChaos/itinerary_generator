# hotel_agents.py

from services.google_places import search_places

def search_hotels(city, check_in, check_out, adults=1):
    """
    Search hotels using Google Places API (with ratings & photos).
    """
    query = f"hotels in {city}"
    hotels = search_places(query, place_type="lodging")

    # sort by rating + number of reviews
    hotels = sorted(hotels, key=lambda x: (x["rating"] or 0, x["user_ratings_total"] or 0), reverse=True)
    return hotels[:10]  # return top 10
