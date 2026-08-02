"""
Base parser for AI agent outputs.
"""

from __future__ import annotations

import json
from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

from ai_team.agents.exceptions import AgentExecutionError
from ai_team.infrastructure.llm.responses import LLMResponse

T = TypeVar("T", bound=BaseModel)


class BaseParser(ABC, Generic[T]):
    """
    Generic parser for converting LLM responses into
    validated Pydantic models.
    """

    model: type[T]

    @classmethod
    def parse(
        cls,
        response: LLMResponse,
    ) -> T:
        """
        Parse an LLM response.
        """
        return cls.parse_json(response.content)

    @classmethod
    def parse_json(
        cls,
        content: str,
    ) -> T:
        """
        Parse a JSON string into the target model.
        """

        try:
            payload = json.loads(content)

        except json.JSONDecodeError as exc:
            raise AgentExecutionError(
                f"{cls.__name__} received invalid JSON."
            ) from exc

        return cls.validate(payload)

    @classmethod
    def validate(
        cls,
        payload: dict,
    ) -> T:
        """
        Validate a parsed JSON payload.
        """

        try:
            return cls.model.model_validate(payload)

        except ValidationError as exc:
            raise AgentExecutionError(
                f"{cls.__name__} returned an invalid "
                f"{cls.model.__name__}."
            ) from exc