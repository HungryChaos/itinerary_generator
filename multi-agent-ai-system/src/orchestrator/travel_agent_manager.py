# orchestrator/travel_agent_manager.py

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # allow imports

from agents.query_parser import parse_trip_request
from agents.flight_agent import search_flights
from agents.hotel_agent import HotelAgent
from agents.attractions_agent import search_attractions

import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_itinerary_with_gemini(destination, start_date, end_date, flight, hotel, attractions):
    """
    Use Gemini to create a day-by-day itinerary.
    """
    system_prompt = f"""
    You are a smart travel planner.
    Create a detailed day-by-day travel itinerary in JSON.
    The user is visiting {destination} from {start_date} to {end_date}.
    They chose this flight: {flight}
    They chose this hotel: {hotel['name']} ({hotel['rating']}⭐)
    Recommended attractions: {json.dumps(attractions, indent=2)}

    Output a JSON structure like:
    {{
      "day1": ["arrival", "activity1", "activity2"],
      "day2": ["activity1", "activity2"],
      ...
    }}
    """

    response = model.generate_content(system_prompt)
    text = response.text.strip()
    # Clean Gemini response (remove markdown if present)
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse itinerary", "raw": response.text}


def run_travel_planner(user_input: str):
    print("📝 Parsing user request...")
    trip = parse_trip_request(user_input)
    print("✅ Parsed Trip:", trip.model_dump_json(indent=2))

    # Flights
    print("\n✈️ Searching flights...")
    if not trip.origin:
        print("❌ Origin not specified in trip request.")
        return None
    flights = search_flights(trip.origin, trip.destination, trip.start_date, trip.end_date)
    if not flights:
        print("❌ No flights found.")
        return None
    chosen_flight = flights[0]

    # Hotels
    print("\n🏨 Searching hotels...")
    hotel_agent = HotelAgent()
    hotels = hotel_agent.get_hotels(trip, max_results=5)
    if not hotels:
        print("❌ No hotels found.")
        return None
    chosen_hotel = hotels[0]

    # Attractions
    print("\n🎡 Searching attractions...")
    attractions = search_attractions(trip.destination, preferences=trip.preferences)

    # Itinerary with Gemini
    print("\n🗓️ Generating itinerary...")
    itinerary = generate_itinerary_with_gemini(
        trip.destination,
        trip.start_date,
        trip.end_date,
        chosen_flight,
        chosen_hotel,
        attractions[:5]
    )

    return {
        "trip": trip.model_dump(),
        "flight": chosen_flight,
        "hotel": chosen_hotel,
        "attractions": attractions[:5],
        "itinerary": itinerary
    }


if __name__ == "__main__":
    user_prompt = "Plan me a 5-day trip from New York to paris starting on 2025-10-01 under $5000 focused on food & culture for 2 travelers."
    result = run_travel_planner(user_prompt)

    if result:
        print("\n✅ Final Itinerary Preview:")
        print(json.dumps(result, indent=2))
    else:
        print("\n❌ Failed to generate itinerary.")
