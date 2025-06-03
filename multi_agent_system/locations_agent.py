from llm import LLM
from .base_agent import BaseAgent
from prompts.locations_agent_prompt import LOCATIONS_AGENT_PROMPT
from loguru import logger


class LocationsAgent(BaseAgent):

    def __init__(self):
        self.name = "Locations Agent"
        self.description = "Generates location descriptions based on given tasks."

    def execute_task(self, task: str) -> str:

        logger.info(f"{self.name} executing task: {task}")
        llm = LLM(
            model_name="mistral-small-latest", system_prompt=LOCATIONS_AGENT_PROMPT
        )
        prompt = f"Generate a location description based on the following task: {task}. Use the location generation tool if available."
        response = llm.complete(prompt)
        return f"**{self.name}**: {response}"
