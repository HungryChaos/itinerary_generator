from services.google_places import search_places

def search_attractions(city, preferences=None):
    if preferences:
        if isinstance(preferences, list):
            pref_str = ", ".join(preferences)
        else:
            pref_str = str(preferences)
        query = f"attractions in {city}"  # Simplified query
    else:
        query = f"top attractions in {city}"

    print(f"🔍 Searching attractions with query: '{query}'")
    attractions = search_places(query, place_type=None)  # Remove type restriction
    print(f"✅ Found {len(attractions)} attractions")
    attractions = sorted(attractions, key=lambda x: ((x.get("rating") or 0), (x.get("user_ratings_total") or 0)), reverse=True)
    return attractions[:10]
