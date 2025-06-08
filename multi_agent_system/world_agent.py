from llm import LLM
from .base_agent import BaseAgent
from prompts.world_agent_prompt import WORLD_AGENT_PROMPT
from loguru import logger


class WorldAgent(BaseAgent):
    def __init__(self):
        self.name = "World Agent"
        self.description = "Generates world descriptions based on given tasks."

    def execute_task(self, task: str) -> str:

        logger.info(f"{self.name} executing task: {task}")
        llm = LLM(model_name="mistral-small-latest", system_prompt=WORLD_AGENT_PROMPT)
        prompt = f"Generate a world description based on the following task: {task}."
        response = llm.complete(prompt)
        return f"**{self.name}**: {response}"
