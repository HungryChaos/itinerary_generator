from services.opentripmap import get_pois

# Simple city coordinates for OpenTripMap
CITY_COORDS = {
    "paris": (48.8566, 2.3522),
    "london": (51.5074, -0.1278),
    "new york": (40.7128, -74.0060),
    # Add more as needed
}

def search_attractions(city, preferences=None):
    city_lower = city.lower()
    if city_lower not in CITY_COORDS:
        print(f"❌ No coordinates for {city}, skipping attractions")
        return []
    
    lat, lon = CITY_COORDS[city_lower]
    kinds = "cultural,museums,food"  # Default kinds
    if preferences:
        if "food" in preferences:
            kinds += ",foods"
        if "culture" in preferences:
            kinds += ",cultural"
    
    print(f"🔍 Searching attractions in {city} with OpenTripMap")
    data = get_pois(lat, lon, kinds=kinds, radius=5000, limit=20)
    features = data.get("features", [])
    print(f"✅ Found {len(features)} attractions")
    
    attractions = []
    for f in features:
        props = f.get("properties", {})
        attractions.append({
            "name": props.get("name"),
            "address": f"{city}, {props.get('address', '')}",
            "rating": None,  # OpenTripMap doesn't provide ratings
            "user_ratings_total": None,
            "price_level": None,
            "photo": None,
            "place_id": props.get("xid")
        })
    

    return attractions[:10]
