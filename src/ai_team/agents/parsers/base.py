"""
Base parser for AI agent outputs.
"""

from __future__ import annotations

from abc import ABC
from typing import ClassVar
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ValidationError

from ai_team.agents.exceptions import AgentExecutionError
from ai_team.infrastructure.llm.responses import LLMResponse


T = TypeVar(
    "T",
    bound=BaseModel,
)


class BaseParser(
    ABC,
    Generic[T],
):
    """
    Generic parser for converting LLM responses
    into validated Pydantic models.
    """

    model: ClassVar[type[T]]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @classmethod
    def parse(
        cls,
        response: LLMResponse,
    ) -> T:
        """
        Parse and validate an LLM response.
        """

        return cls.parse_json(
            response.content,
        )

    # ------------------------------------------------------------------
    # JSON parsing
    # ------------------------------------------------------------------

    @classmethod
    def parse_json(
        cls,
        content: str,
    ) -> T:
        """
        Parse and validate a JSON response.
        """

        try:
            return cls.model.model_validate_json(
                content,
            )

        except ValidationError as exc:
            raise AgentExecutionError(
                f"{cls.__name__} returned invalid "
                f"{cls.model.__name__} output."
            ) from exc

        except ValueError as exc:
            raise AgentExecutionError(
                f"{cls.__name__} received invalid JSON."
            ) from exc