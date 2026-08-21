from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.memory.manager import MemoryManager
    from ai_team.rag.manager import RAGManager
    from ai_team.tools.filesystem import FilesystemTool


@dataclass(slots=True, frozen=True)
class AgentTools:
    """
    Collection of tools available to AI agents.
    """

    filesystem: FilesystemTool | None = None
    rag: RAGManager | None = None
    memory: MemoryManager | None = None
