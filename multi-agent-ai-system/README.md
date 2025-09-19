# Multi-Agent AI System

This project implements a simple multi-agent AI system where individual agents interact with a simulated environment. The system is designed to demonstrate basic principles of agent-based modeling and reinforcement learning.

## Project Structure

```
multi-agent-ai-system
├── src
│   ├── agents
│   │   ├── query_parser.py    # Contains the Agent class for query parsing
│   │   ├── attractions.py     # Agent for finding attractions
│   │   ├── budget_manager.py  # Agent for budget management
│   │   ├── itinerary_builder.py # Agent for building itineraries
│   ├── environment
│   │   └── environment.py     # Contains the Environment class
│   ├── services
│   │   ├── amadeus_service.py # Amadeus API service for flights/hotels
│   │   └── opentripmap.py     # OpenTripMap API service for attractions
│   ├── utils
│   │   └── utils.py           # Contains utility functions
│   └── main.py                # Entry point of the application
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Installation

To install the necessary dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the simulation, execute the following command:

```
python src/main.py
```

## Classes and Functions

- **Agent**: Represents an individual AI agent with methods to initialize, act, and learn.
- **Environment**: Simulates the environment in which agents operate, with methods to setup, reset, and step through the simulation.
- **Utility Functions**: Includes functions like `generateRandomNumber` and `calculateReward` to assist in various calculations.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.