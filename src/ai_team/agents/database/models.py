"""
Models used by the Database agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.database_models import (
    DatabaseEntity,
    DatabaseRelationship,
)

from ai_team.agents.models import (
    CodePatch,
    DependencyChange,
)


class DatabaseResult(BaseModel):

    ...

    entities: list[DatabaseEntity]

    relationships: list[
        DatabaseRelationship
    ] = Field(default_factory=list)

    code_patches: list[
        CodePatch
    ] = Field(default_factory=list)

    dependencies: list[
        DependencyChange
    ] = Field(default_factory=list)

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )