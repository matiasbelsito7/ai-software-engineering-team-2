"""
Backend agent response parser.
"""

from __future__ import annotations

from ai_team.agents.backend.models import BackendResult
from ai_team.agents.parsers.base import BaseParser


class BackendParser(BaseParser[BackendResult]):
    """
    Parse Backend Agent responses.
    """

    model = BackendResult