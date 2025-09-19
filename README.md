# 🧳 AI Travel Planner (Multi-Agent System)

An AI-powered multi-agent system that generates personalized travel itineraries with flights, hotels, attractions, and budget management.

## 🚀 Features
- Multi-agent architecture (Query Parser, Flight Agent, Attraction Recommender, etc.)
- Live API integration (Amadeus, OpenTripMap, BestTime)
- Budget-aware itinerary generation
- Interactive Streamlit frontend
- Export to PDF

## ⚡ Tech Stack
- Python, LangChain, Streamlit
- Amadeus API, OpenTripMap API, BestTime API

## ▶️ Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/ai-travel-planner.git
cd ai-travel-planner
pip install -r requirements.txt
streamlit run app/main.py






#we are making a trip planner using multi agent system, where the user gives a location, budget, start & end date, one-way/round trip in the query, the query is parsed, then the recommended hotels(photos using google places api) & flights are provided using amadeus api, high rated attractions in the location are found using opentripmap api and ratings through google places api, through this an iternary is generated along with how much budget is being used where
User enters a free-text prompt (like ChatGPT style, text bar in the middle).

Agents run in stages, not all at once:

Step 1 → Query Parser runs.

Step 2 → Flights + Hotels suggestions returned.

Step 3 → User picks one flight + one hotel (preferences).

Step 4 → Attractions agent finds top-rated options.

Step 5 → Itinerary builder agent creates day-by-day plan.

Step 6 → User can ask for changes → regenerate itinerary.