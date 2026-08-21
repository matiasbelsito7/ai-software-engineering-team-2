from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .container import Container
    from .workspace import Workspace


def __getattr__(name: str) -> object:
    if name == "Container":
        from .container import Container

        return Container
    if name == "Workspace":
        from .workspace import Workspace

        return Workspace
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["Container", "Workspace"]
