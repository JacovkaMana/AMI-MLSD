from llm import LLM
from .base_agent import BaseAgent
from prompts.locations_agent_prompt import LOCATIONS_AGENT_PROMPT
from loguru import logger
from tools.donjon import Locations_Tool


class LocationsAgent(BaseAgent):

    def __init__(self):
        self.name = "Locations Agent"
        self.description = "Generates location descriptions based on given tasks."
        self.locations_tool = Locations_Tool()

    def execute_task(self, task: str) -> str:
        logger.info(f"{self.name} executing task: {task}")
        llm = LLM(
            model_name="mistral-small-latest", system_prompt=LOCATIONS_AGENT_PROMPT
        )

        # Get reference data from tool
        reference = self.locations_tool.call(count=1)

        prompt = f"""Generate a location description based on the following task: {task}.
        
        Reference Data:
        {reference}
        """
        response = llm.complete(prompt)
        return f"**{self.name}**: {response}"
