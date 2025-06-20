from llm import LLM
from .base_agent import BaseAgent
from prompts.storyteller_prompt import STORYTELLER_SYSTEM_PROMPT
from loguru import logger


class Storyteller:

    def __init__(self):
        self.name = "StoryTeller"
        self.description = "StoryTeller"

    def generate_output(self, agent_responses, query: str) -> str:

        logger.info(f"{self.name} executing user query : {query}")
        llm = LLM(
            model_name="qwen/qwen3-32b-04-28:free",
            system_prompt=STORYTELLER_SYSTEM_PROMPT,
        )
        prompt = f"Agent Responses:\n{agent_responses}\n\nUser Query: '{query}'"
        response = llm.complete(prompt)
        return response
