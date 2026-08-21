"""
Models used by the Database agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ai_team.agents.database_models import (
        DatabaseEntity,
        DatabaseRelationship,
    )
    from ai_team.agents.patches import (
        CodePatch,
        DependencyChange,
    )

# ============================================================================
# Database Result
# ============================================================================


class DatabaseResult(BaseModel):
    """
    Result produced by the Database agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    entities: list[DatabaseEntity]

    relationships: list[
        DatabaseRelationship
    ] = Field(
        default_factory=list,
    )

    code_patches: list[
        CodePatch
    ] = Field(
        default_factory=list,
    )

    dependencies: list[
        DependencyChange
    ] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )
