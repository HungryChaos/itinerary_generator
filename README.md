# 🧳 AI Travel Planner (Multi-Agent System)

An AI-powered multi-agent system that generates personalized travel itineraries with flights, hotels, attractions, and budget management using real-time API integrations.

## � Overview

This project implements a multi-agent AI system for trip planning. Users provide a free-text query with destination, budget, dates, and preferences. The system parses the query, fetches live data from APIs, and generates a complete itinerary.

### Workflow
1. **Query Parser**: Parses user input using Gemini AI to extract destination, dates, budget, preferences, etc.
2. **Flight & Hotel Search**: Fetches options from Amadeus API.
3. **User Selection**: User picks preferred flight and hotel.
4. **Attractions Search**: Finds top-rated attractions using OpenTripMap and Google Places APIs.
5. **Itinerary Generation**: Creates a day-by-day plan with Gemini AI.
6. **Budget Tracking**: Tracks spending across flights, hotels, and activities.

## 🚀 Features
- **Multi-Agent Architecture**: Specialized agents for parsing, flights, hotels, attractions, and itinerary building.
- **Real-Time API Integration**: Amadeus (flights/hotels), Google Places (photos/ratings), OpenTripMap (attractions).
- **AI-Powered Parsing**: Uses Google Gemini for natural language query understanding.
- **Budget Management**: Tracks and reports budget allocation.
- **Interactive Workflow**: Step-by-step user interaction for selections.
- **Error Handling**: Robust handling of API failures and fallbacks.

## ⚡ Tech Stack
- **Backend**: Python 3.8+
- **AI**: Google Generative AI (Gemini)
- **APIs**: Amadeus API, Google Places API, OpenTripMap API
- **Libraries**: Pydantic, Requests, python-dotenv
- **Environment**: Virtual environment recommended

## 🛠️ Setup

### Prerequisites
- Python 3.8 or higher
- Git
- API Keys: Amadeus, Google Places, OpenTripMap, Gemini

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/HungryChaos/itinerary_generator.git
   cd itinerary_generator
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env` (if available) or create `multi-agent-ai-system/.env`
   - Add your API keys:
     ```
     GEMINI_API_KEY=your_gemini_key
     AMADEUS_API_KEY=your_amadeus_key
     AMADEUS_API_SECRET=your_amadeus_secret
     GOOGLE_PLACES_API_KEY=your_google_places_key
     OPENTRIPMAP_KEY=your_opentripmap_key
     ```

### API Key Setup
- **Amadeus**: Sign up at [Amadeus Developer Portal](https://developers.amadeus.com/)
- **Google Places**: Enable Places API in [Google Cloud Console](https://console.cloud.google.com/)
- **OpenTripMap**: Get key from [OpenTripMap](https://opentripmap.io/)
- **Gemini**: Get key from [Google AI Studio](https://aistudio.google.com/)

## ▶️ Usage

Run the travel planner:
```bash
cd multi-agent-ai-system
python src/orchestrator/travel_agent_manager.py
```

Example query: "Plan me a 5-day trip from New York to Paris starting on 2025-10-01 under $5000 focused on food & culture for 2 travelers."

The system will:
- Parse the query
- Search for flights and hotels
- (In interactive mode) Wait for user selection
- Fetch attractions
- Generate itinerary

## 📁 Project Structure
```
multi-agent-ai-system/
├── src/
│   ├── agents/
│   │   ├── query_parser.py      # Parses user queries
│   │   ├── flight_agent.py      # Handles flight searches
│   │   ├── hotel_agent.py       # Handles hotel searches
│   │   └── attractions_agent.py # Handles attraction searches
│   ├── services/
│   │   ├── amadeus_services.py  # Amadeus API client
│   │   ├── google_places.py     # Google Places API client
│   │   └── opentripmap.py       # OpenTripMap API client
│   ├── orchestrator/
│   │   └── travel_agent_manager.py # Main orchestrator
│   ├── environment.py           # Environment setup
│   └── utils.py                 # Utility functions
├── .env                         # Environment variables (ignored)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer
This is a demo project using test APIs. For production use, obtain proper API keys and handle rate limits/security.