"""
Parser for Spec agent outputs.
"""

from __future__ import annotations

from ai_team.agents.parsers.base import BaseParser
from ai_team.agents.spec.models import AppSpecification


class SpecParser(BaseParser[AppSpecification]):
    """
    Parser for Spec agent responses.
    """

    model = AppSpecification
