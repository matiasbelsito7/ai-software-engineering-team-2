"""
Parser for the DevOps agent.
"""

from __future__ import annotations

from ai_team.agents.devops.models import DevOpsResult
from ai_team.agents.parsers.base import BaseParser


class DevOpsParser(BaseParser[DevOpsResult]):
    """
    Parser responsible for converting LLM responses
    into DevOpsResult objects.
    """

    MODEL = DevOpsResult