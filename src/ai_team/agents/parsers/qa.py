"""
Parser for the QA agent.
"""

from __future__ import annotations

from ai_team.agents.parsers.base import BaseParser
from ai_team.agents.qa.models import QAResult


class QAParser(BaseParser[QAResult]):
    """
    Parser responsible for converting LLM responses
    into QAResult objects.
    """

    MODEL = QAResult