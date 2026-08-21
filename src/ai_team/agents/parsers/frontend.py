"""
Parser for the Frontend agent.
"""

from __future__ import annotations

from ai_team.agents.frontend.models import FrontendResult
from ai_team.agents.parsers.base import BaseParser


class FrontendParser(BaseParser[FrontendResult]):
    """
    Parser responsible for converting LLM responses
    into FrontendResult objects.
    """

    MODEL = FrontendResult
