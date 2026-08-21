"""
Parser for Architect agent outputs.
"""

from __future__ import annotations

from ai_team.agents.architect.models import ArchitectureDesign
from ai_team.agents.parsers.base import BaseParser


class ArchitectParser(BaseParser[ArchitectureDesign]):
    """
    Parser for Architect agent responses.
    """

    model = ArchitectureDesign
