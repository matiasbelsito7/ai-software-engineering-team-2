"""
Database agent implementation.
"""

from __future__ import annotations

from typing import Any

from ai_team.agents.base import BaseAgent
from ai_team.agents.database.prompt_builder import (
    DatabasePromptBuilder,
)
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.database import DatabaseParser
from ai_team.shared.enums import AgentCapability


class DatabaseAgent(BaseAgent[Any]):
    """
    AI agent responsible for designing the persistence layer.
    """

    INFO = AgentInfo(
        name="database",
        capability=AgentCapability.DATABASE,
        description=(
            "Designs database schemas, entities, "
            "relationships and persistence strategies."
        ),
    )

    PARSER = DatabaseParser

    PROMPT_BUILDER = DatabasePromptBuilder
