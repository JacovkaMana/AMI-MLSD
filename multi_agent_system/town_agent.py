from llm import LLM
from .base_agent import BaseAgent
from prompts.town_agent_prompt import TOWN_AGENT_PROMPT
from loguru import logger
from tools.donjon import Town_Tool


class TownAgent(BaseAgent):
    def __init__(self):
        self.name = "Town Agent"
        self.description = "Generates town descriptions based on given tasks."
        self.town_tool = Town_Tool()

    async def execute_task(self, task: str) -> str:
        logger.info(f"{self.name} executing task: {task}")
        llm = LLM(model_name="mistral-small-latest", system_prompt=TOWN_AGENT_PROMPT)

        # Get reference data from tool
        reference = self.town_tool.call(count=1)

        prompt = f"""Generate a town description based on the following task: {task}.
        
        Reference Data:
        {reference}
        """
        response = await llm.complete(prompt)
        return f"**{self.name}**: {response}"
