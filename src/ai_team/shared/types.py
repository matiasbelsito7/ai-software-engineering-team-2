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
from typing import Any
from uuid import UUID

###############################################################################
# JSON
###############################################################################

type JSONPrimitive = str | int | float | bool | None

type JSONValue = JSONPrimitive | list["JSONValue"] | dict[str, "JSONValue"]

type JSONObject = dict[str, JSONValue]
type JSONArray = list[JSONValue]

###############################################################################
# Generic metadata
###############################################################################

type Metadata = dict[str, Any]
type Headers = Mapping[str, str]

###############################################################################
# Identifiers
###############################################################################

type AgentId = str
type TaskId = UUID
type SessionId = UUID
type ConversationId = UUID
type MessageId = UUID
type WorkflowId = UUID
type CheckpointId = UUID
type DocumentId = UUID

###############################################################################
# Files
###############################################################################

type FilePath = str | PathLike[str]
type DirectoryPath = str | PathLike[str]

###############################################################################
# LLM
###############################################################################

type Prompt = str
type Completion = str
type SystemPrompt = str

type TokenCount = int
type Embedding = list[float]
type EmbeddingVector = list[float]

###############################################################################
# Time
###############################################################################

type Timestamp = float
type DurationSeconds = float

###############################################################################
# Costs
###############################################################################

type USD = float

###############################################################################
# Tool execution
###############################################################################

type ToolArguments = dict[str, Any]
type ToolResult = Any

###############################################################################
# Configuration
###############################################################################

type SettingsDict = dict[str, Any]

###############################################################################
# State
###############################################################################

type StateDict = dict[str, Any]

###############################################################################
# Miscellaneous
###############################################################################

type Tags = list[str]
type Labels = dict[str, str]
