import { Agent } from './agents';
import { Environment } from './environment';

const NUM_AGENTS = 5;
const environment = new Environment();
const agents: Agent[] = [];

function initializeAgents() {
    for (let i = 0; i < NUM_AGENTS; i++) {
        const agent = new Agent();
        agent.initialize();
        agents.push(agent);
    }
}

function runSimulation() {
    environment.setup();
    for (let step = 0; step < 100; step++) {
        environment.step();
        agents.forEach(agent => {
            agent.act();
            agent.learn();
        });
    }
    environment.reset();
}

initializeAgents();
runSimulation();