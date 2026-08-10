"""
DevOps agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.devops import DevOpsOutput
from ai_team.agents.parsers.base import BaseParser


class DevOpsParser(BaseParser[DevOpsOutput]):
    """
    Parse DevOps Agent responses.
    """

    model = DevOpsOutput