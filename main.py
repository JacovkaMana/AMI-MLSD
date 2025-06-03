from loguru import logger

from multi_agent_system.character_agent import CharacterAgent
from multi_agent_system.locations_agent import LocationsAgent
from multi_agent_system.town_agent import TownAgent
from multi_agent_system.world_agent import WorldAgent
from multi_agent_system.storyteller import Storyteller
from multi_agent_system.supervisor import Supervisor


def main():

    logger.info("Starting...")
    # Create supervisor instance
    supervisor = Supervisor()

    # Register all agents
    supervisor.define_agent(WorldAgent)
    supervisor.define_agent(LocationsAgent)
    supervisor.define_agent(CharacterAgent)
    supervisor.define_agent(TownAgent)
    # The Storyteller is used for final output synthesis

    # Handle a sample query
    query = (
        "Create a fantasy world with a medieval kingdom, a forest, and a mountain range"
    )
    result = supervisor.handle_query(query)

    logger.info("Final Result:")
    logger.info(result)


if __name__ == "__main__":
    main()
