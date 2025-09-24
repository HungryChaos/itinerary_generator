# agents/flight_agent.py

from services.amadeus_services import search_flights_api

def search_flights(origin, destination, departure_date, return_date=None, travelers=1, currency="INR"):
    """
    Agent wrapper for Amadeus flight search.
    Returns cleaned list of flights.
    """
    from services.amadeus_services import get_city_code
    
    try:
        origin_code = get_city_code(origin)
        destination_code = get_city_code(destination)
    except ValueError as e:
        print(f"❌ Error getting city codes: {e}")
        return []
    
    raw = search_flights_api(origin_code, destination_code, departure_date, return_date, travelers, currency)
    offers = raw.get("data", [])

    flights = []
    for offer in offers:
        price = offer["price"]["total"]
        itineraries = offer.get("itineraries", [])

        if not itineraries:
            continue

        first_leg = itineraries[0]["segments"][0]
        last_leg = itineraries[0]["segments"][-1]

        flights.append({
            "airline": first_leg["carrierCode"],
            "departure": first_leg["departure"]["iataCode"],
            "arrival": last_leg["arrival"]["iataCode"],
            "departure_time": first_leg["departure"]["at"],
            "arrival_time": last_leg["arrival"]["at"],
            "price": price
        })

    return flights
