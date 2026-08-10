"""
Database agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.database import DatabaseOutput
from ai_team.agents.parsers.base import BaseParser


class DatabaseParser(
    BaseParser[DatabaseOutput],
):
    """
    Parse Database Agent responses.
    """

    model = DatabaseOutput