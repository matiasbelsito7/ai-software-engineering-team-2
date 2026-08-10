"""
Backend agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.backend import BackendOutput
from ai_team.agents.parsers.base import BaseParser


class BackendParser(BaseParser[BackendOutput]):
    """
    Parse Backend Agent responses.
    """

    model = BackendOutput