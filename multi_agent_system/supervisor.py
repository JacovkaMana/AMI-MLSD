# multi_agent_system/supervisor.py

import json
from typing import List, Dict, Any
from .storyteller import Storyteller
from .base_agent import BaseAgent
from prompts.supervisor_prompt import SUPERVISOR_PROMPT
from llm import LLM
from loguru import logger


class Supervisor:
    def __init__(self):
        self.defined_agents = {}

    def define_agent(self, agent_class):
        """Define an agent to be used by the supervisor."""
        self.defined_agents[agent_class.__name__] = agent_class()

    def handle_query(self, query: str) -> str:
        """Process a user query by calling defined agents and synthesizing their responses."""
        if not self.defined_agents:
            return "Error: No agents defined. Please define at least one agent using define_agent()."

        agent_descriptions = "\n".join(
            [
                f"#{agent_class.name} : {agent_class.description}"
                for agent_class in self.defined_agents.values()
            ]
        )
        # Analyze the query to determine which agents to call
        task_definition_prompt = (
            f"Available agents: {agent_descriptions} \n\n\n User Query:{query}\n\n"
        )
        llm = LLM(
            model_name="mistral-small-latest",
            system_prompt=SUPERVISOR_PROMPT,
            response_format="json_object",
        )

        logger.info(f"Deciding which tasks to create")
        task_definition = llm.complete(task_definition_prompt)
        logger.info(f"Task definition: {task_definition}")

        tasks = json.loads(task_definition)

        if isinstance(tasks, list):
            tasks = tasks[0]

        if not isinstance(tasks, dict):
            logger.error(f"Invalid task definition: {tasks}")
            raise ValueError("Invalid task definition")

        results = []

        logger.info(f"Running Agents")
        for agent_name, task in tasks.items():
            agent = self.get_agent_class(agent_name)

            if isinstance(task, list):
                for sub_task in task:
                    response = agent.execute_task(sub_task)
                    results.append(response)
            if isinstance(task, str):
                response = agent.execute_task(task)
                results.append(response)

        logger.info(f"Results: {'\n'.join(x[:300] for x in results)}")
        results = "\n\n\n".join(results)

        logger.info(f"Synthesizing response")
        storyteller = Storyteller()
        full_response = storyteller.generate_output(results, query)
        return full_response

    def get_agent_class(self, agent_name: str) -> type:
        """Get the agent class based on the agent name."""
        for agent_class in self.defined_agents.keys():
            if agent_class.lower() == agent_name.replace(" ", "").lower():
                return self.defined_agents[agent_class]
        return None


# Example agent implementation (for demonstration purposes)
class ExampleAgent(BaseAgent):
    def execute_task(self, task: str) -> str:
        """Simple example agent that echoes the task."""
        return f"ExampleAgent: Executed task '{task}' successfully."
