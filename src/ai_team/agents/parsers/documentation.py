"""
Parser for the Documentation agent.
"""

from __future__ import annotations

from ai_team.agents.documentation.models import (
    DocumentationResult,
)
from ai_team.agents.parsers.base import BaseParser


class DocumentationParser(BaseParser[DocumentationResult]):
    """
    Parser responsible for converting LLM responses
    into DocumentationResult objects.
    """

    MODEL = DocumentationResult
