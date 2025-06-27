from loguru import logger
import asyncio
import aiohttp
from tools import ToolManager, Tool_Manager
from prompts.main import SYSTEM_PROMPT
import json
import os
from dotenv import load_dotenv


class LLM:
    def __init__(
        self,
        system_prompt: str,
        tool_manager: Tool_Manager = None,
        model_name: str = "mistral-large-latest",
        response_format: str = None,
        temperature: float = None,
    ) -> None:
        self.tool_manager = tool_manager
        load_dotenv()

        if "mistral" in model_name.lower():
            self.url = "https://api.mistral.ai/v1/chat/completions"
            api_key = os.environ.get("MISTRAL_KEY")
        else:
            self.url = "https://openrouter.ai/api/v1/chat/completions"
            api_key = os.environ.get("OPENROUTER_KEY")

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        self.params = {
            "model": model_name,
            "temperature": 0.7,
            # "max_tokens": 10000,
            # "top_p": 0.9,
            # "presence_penalty": 0.2,
            # "frequency_penalty": 0.3,
        }

        if temperature:
            self.params["temperature"] = temperature

        self.system_prompt = system_prompt
        self.response_format = response_format

    def get_default_messages(self, prompt: str):
        return [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {"role": "user", "content": f"{prompt}"},
        ]

    async def complete(self, prompt: str, messages=None):
        params = self.params.copy()

        if self.response_format:
            params["response_format"] = {}
            params["response_format"]["type"] = self.response_format

        # if self.tool_manager:
        #     params["tools"] = self.tool_manager.tool_schema
        #     params["tool_choice"] = "auto"

        if not messages:
            messages = self.get_default_messages(prompt)

        params["messages"] = messages

        logger.info(f"Query to the {self.url}")
        await asyncio.sleep(3)  # Rate limiting
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, headers=self.headers, json=params, timeout=120
            ) as response:
                result = await response.json()

        choice = result.get("choices", [{}])[0]
        message = choice.get("message", {})

        # if message.get("tool_calls", None):
        #     tool_calls = message["tool_calls"]
        #     messages.append(message)

        #     for tool_call in tool_calls:
        #         function_name = tool_call["function"]["name"]
        #         arguments = json.loads(tool_call["function"]["arguments"])
        #         count = arguments["count"]

        #         try:
        #             tool_result = self.tool_manager.fetch_tool_data(
        #                 function_name, count
        #             )
        #         except Exception as error:
        #             tool_result = f"Инструмент {function_name} не найден."

        #         messages.append(
        #             {
        #                 "role": "tool",
        #                 "name": function_name,
        #                 "content": tool_result,
        #                 "tool_call_id": tool_call["id"],
        #             },
        #         )

        #     return self.complete(prompt, messages)
        try:
            return message["content"]
        except:
            logger.error("Error in model response: {}", message)
            raise Exception(f"Ошибка в ответе модели - {response.text}")
