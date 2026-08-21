"""
Agent metadata.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from ai_team.shared.enums.agents import AgentCapability


class AgentInfo(BaseModel):
    """
    Static metadata describing an agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    capability: AgentCapability

    description: str

    version: str = "1.0.0"
