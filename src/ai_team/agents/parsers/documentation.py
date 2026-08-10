"""
Documentation agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.documentation import DocumentationOutput
from ai_team.agents.parsers.base import BaseParser


class DocumentationParser(
    BaseParser[DocumentationOutput],
):
    """
    Parse Documentation Agent responses.
    """

    model = DocumentationOutput