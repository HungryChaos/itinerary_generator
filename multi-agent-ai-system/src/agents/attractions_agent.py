# attractions_agent.py

from ..services.google_places import search_places

def search_attractions(city, preferences=None):
    """
    Get top attractions in a city.
    Preferences (optional): culture, food, nightlife, adventure, etc.
    """
    query = f"top attractions in {city}"
    if preferences:
        query = f"{preferences} in {city}"

    attractions = search_places(query, place_type="tourist_attraction")

    # sort by rating + reviews
    attractions = sorted(attractions, key=lambda x: (x["rating"] or 0, x["user_ratings_total"] or 0), reverse=True)
    return attractions[:10]
