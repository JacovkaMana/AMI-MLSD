from llm import LLM
from .base_agent import BaseAgent
from prompts.character_agent_prompt import CHARACTER_AGENT_PROMPT
from loguru import logger


class CharacterAgent(BaseAgent):

    def __init__(self):
        self.name = "Character Agent"
        self.description = "Generates character descriptions based on given tasks."

    def execute_task(self, task: str) -> str:

        logger.info(f"{self.name} executing task: {task}")
        llm = LLM(
            model_name="mistral-small-latest", system_prompt=CHARACTER_AGENT_PROMPT
        )
        prompt = f"Generate a character description based on the following task: {task}. Use the character generation tool if available."
        response = llm.complete(prompt)
        return f"**{self.name}**: {response}"
