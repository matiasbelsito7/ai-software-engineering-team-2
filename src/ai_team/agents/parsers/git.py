"""
Parser for the Git agent.
"""

from __future__ import annotations

from ai_team.agents.git.models import GitResult
from ai_team.agents.parsers.base import BaseParser


class GitParser(BaseParser[GitResult]):
    """
    Parser responsible for converting LLM responses
    into GitResult objects.
    """

    MODEL = GitResult