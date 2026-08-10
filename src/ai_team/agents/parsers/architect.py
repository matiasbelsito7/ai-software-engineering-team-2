"""
Architect agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.architect import ArchitectOutput
from ai_team.agents.parsers.base import BaseParser


class ArchitectParser(BaseParser[ArchitectOutput]):
    """
    Parse Architect Agent responses.
    """

    model = ArchitectOutput