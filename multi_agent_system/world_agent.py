from llm import LLM
from .base_agent import BaseAgent
from prompts.world_agent_prompt import WORLD_AGENT_PROMPT
from loguru import logger
from tools.donjon import World_Tool


class WorldAgent(BaseAgent):
    def __init__(self):
        self.name = "World Agent"
        self.description = "Generates world descriptions based on given tasks."
        self.world_tool = World_Tool()

    def execute_task(self, task: str) -> str:
        logger.info(f"{self.name} executing task: {task}")
        llm = LLM(model_name="mistral-small-latest", system_prompt=WORLD_AGENT_PROMPT)

        # Get reference data from tool
        reference = self.world_tool.call(count=1)

        prompt = f"""Generate a world description based on the following task: {task}.
        
        Reference Data:
        {reference}
        """
        response = llm.complete(prompt)
        return f"**{self.name}**: {response}"
