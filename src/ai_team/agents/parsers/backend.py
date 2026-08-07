"""
Backend agent parser.
"""

from __future__ import annotations

import json

from ai_team.agents.parsers.base import BaseParser
from ai_team.agents.patches import (
    CodePatch,
    DependencyChange,
    PatchOperation,
)
from ai_team.infrastructure.llm.responses import LLMResponse


class BackendParser(BaseParser[dict]):
    """
    Parse the backend agent response.
    """

    @classmethod
    def parse(
        cls,
        response: LLMResponse,
    ) -> dict:

        data = cls._load_json(
            response.content,
        )

        patches = [
            CodePatch(
                path=patch["path"],
                operation=PatchOperation(
                    patch["operation"],
                ),
                content=patch.get("content"),
                reason=patch["reason"],
            )
            for patch in data.get(
                "patches",
                [],
            )
        ]

        dependencies = [
            DependencyChange(
                package=dependency["package"],
                version=dependency.get(
                    "version",
                ),
                reason=dependency["reason"],
            )
            for dependency in data.get(
                "dependencies",
                [],
            )
        ]

        return {
            "summary": data.get(
                "summary",
                "",
            ),
            "patches": patches,
            "dependencies": dependencies,
            "notes": data.get(
                "notes",
                [],
            ),
        }

    # ---------------------------------------------------------

    @staticmethod
    def _load_json(
        content: str,
    ) -> dict:

        try:
            return json.loads(
                content,
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "Backend agent returned invalid JSON."
            ) from exc