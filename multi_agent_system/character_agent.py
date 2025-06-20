from llm import LLM
from .base_agent import BaseAgent
from prompts.character_agent_prompt import CHARACTER_AGENT_PROMPT
from loguru import logger
from tools.donjon import Character_Tool


class CharacterAgent(BaseAgent):

    def __init__(self):
        self.name = "Character Agent"
        self.description = "Generates character descriptions based on given tasks."
        self.character_tool = Character_Tool()

    def execute_task(self, task: str) -> str:
        logger.info(f"{self.name} executing task: {task}")
        llm = LLM(
            model_name="mistral-small-latest", system_prompt=CHARACTER_AGENT_PROMPT
        )

        # Get reference data from tool
        reference = self.character_tool.call(count=1)

        prompt = f"""Generate a character description based on the following task: {task}.
        
        Reference Data:
        {reference}
        """
        response = llm.complete(prompt)
        return f"**{self.name}**: {response}"
