```python
"""
Shared type aliases used across the AI Software Engineering Team project.

This module centralizes common type definitions to improve readability,
reduce duplication and avoid circular dependencies.

Guidelines
----------
- Only declare shared type aliases.
- Do not implement business logic.
- Do not import project modules.
- Keep this module lightweight and dependency-free.
"""

from __future__ import annotations

from collections.abc import Mapping
from os import PathLike
from typing import Any, TypeAlias
from uuid import UUID

###############################################################################
# JSON
###############################################################################

JSONPrimitive: TypeAlias = str | int | float | bool | None

JSONValue: TypeAlias = (
    JSONPrimitive
    | list["JSONValue"]
    | dict[str, "JSONValue"]
)

JSONObject: TypeAlias = dict[str, JSONValue]
JSONArray: TypeAlias = list[JSONValue]

###############################################################################
# Generic metadata
###############################################################################

Metadata: TypeAlias = dict[str, Any]
Headers: TypeAlias = Mapping[str, str]

###############################################################################
# Identifiers
###############################################################################

AgentId: TypeAlias = str
TaskId: TypeAlias = UUID
SessionId: TypeAlias = UUID
ConversationId: TypeAlias = UUID
MessageId: TypeAlias = UUID
WorkflowId: TypeAlias = UUID
CheckpointId: TypeAlias = UUID
DocumentId: TypeAlias = UUID

###############################################################################
# Files
###############################################################################

FilePath: TypeAlias = str | PathLike[str]
DirectoryPath: TypeAlias = str | PathLike[str]

###############################################################################
# LLM
###############################################################################

Prompt: TypeAlias = str
Completion: TypeAlias = str
SystemPrompt: TypeAlias = str

TokenCount: TypeAlias = int
Embedding: TypeAlias = list[float]
EmbeddingVector: TypeAlias = list[float]

###############################################################################
# Time
###############################################################################

Timestamp: TypeAlias = float
DurationSeconds: TypeAlias = float

###############################################################################
# Costs
###############################################################################

USD: TypeAlias = float

###############################################################################
# Tool execution
###############################################################################

ToolArguments: TypeAlias = dict[str, Any]
ToolResult: TypeAlias = Any

###############################################################################
# Configuration
###############################################################################

SettingsDict: TypeAlias = dict[str, Any]

###############################################################################
# State
###############################################################################

StateDict: TypeAlias = dict[str, Any]

###############################################################################
# Miscellaneous
###############################################################################

Tags: TypeAlias = list[str]
Labels: TypeAlias = dict[str, str]
```
