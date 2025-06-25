class Tool_Manager:
    def __init__(self, tools: list = []) -> None:
        self.tools = tools

        self.tool_schema = [
            {
                "type": "function",
                "function": {
                    "name": x.get_name(),
                    "description": x.get_description(),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "count": {
                                "type": "integer",
                                "description": "Количество локаций для генерации",
                                "default": 1,
                            }
                        },
                        "required": [],
                    },
                },
            }
            for x in self.tools
        ]

        self.tool_dict = {x.get_name(): x for x in self.tools}

    def fetch_tool_data(self, tool_name, count=1):
        return self.tool_dict[tool_name].call(count)

    def supervisor_decide(self, query):
        if "world" in query.lower():
            return {"agent": "random_world", "parameters": {"count": 1}}
        elif "location" in query.lower():
            return {"agent": "random_location", "parameters": {"count": 1}}
        elif "character" in query.lower():
            return {"agent": "random_character", "parameters": {"count": 1}}
        elif "town" in query.lower():
            return {"agent": "random_town", "parameters": {"count": 1}}
        elif "adventure" in query.lower():
            return {"agent": "random_adventure", "parameters": {"count": 1}}
        else:
            return {"agent": None, "parameters": None}
