# multi_agent_system/base_agent.py
from loguru import logger


class BaseAgent:
    def execute_task(self, task: str) -> str:
        """Base method for agents to execute a task. Must be overridden in subclasses."""
        raise NotImplementedError("Subclasses must implement execute_task method")
