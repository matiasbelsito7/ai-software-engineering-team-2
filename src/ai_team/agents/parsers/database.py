"""
Parser for the Database agent.
"""

from __future__ import annotations

from ai_team.agents.database.models import DatabaseResult
from ai_team.agents.parsers.base import BaseParser


class DatabaseParser(BaseParser[DatabaseResult]):
    """
    Parser responsible for converting LLM responses into
    DatabaseResult objects.
    """

    MODEL = DatabaseResult
