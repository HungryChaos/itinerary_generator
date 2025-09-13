from agents.query_parser import Agent
from environment import Environment

NUM_AGENTS = 5
environment = Environment()
agents = []

def initialize_agents():
    for _ in range(NUM_AGENTS):
        agent = Agent()
        agent.initialize()
        agents.append(agent)

def run_simulation():
    environment.setup()
    for step in range(100):
        environment.step()
        for agent in agents:
            agent.act()
            agent.learn()
    environment.reset()

initialize_agents()
run_simulation()