from .tool_manager import Tool_Manager
from .donjon import (
    Town_Tool,
    Locations_Tool,
    LLM_Tool,
    World_Tool,
    Adventure_Tool,
    Character_Tool,
)

ToolManager = Tool_Manager(
    tools=[
        Town_Tool(),
        Locations_Tool(),
        World_Tool(),
        Adventure_Tool(),
        Character_Tool(),
    ]
)
