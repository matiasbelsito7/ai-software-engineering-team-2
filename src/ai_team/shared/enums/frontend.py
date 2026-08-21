"""
Enums shared by the Frontend agent.
"""

from __future__ import annotations

from enum import StrEnum

# ============================================================================
# UI Component Type
# ============================================================================


class UIComponentType(StrEnum):
    """
    High-level UI component types.
    """

    PAGE = "page"

    LAYOUT = "layout"

    COMPONENT = "component"

    FORM = "form"

    MODAL = "modal"

    TABLE = "table"

    CARD = "card"

    NAVIGATION = "navigation"


# ============================================================================
# User Interaction
# ============================================================================


class InteractionType(StrEnum):
    """
    User interaction types.
    """

    CLICK = "click"

    INPUT = "input"

    SUBMIT = "submit"

    DRAG_DROP = "drag_drop"

    NAVIGATION = "navigation"

    KEYBOARD = "keyboard"


# ============================================================================
# Responsive Breakpoint
# ============================================================================


class ResponsiveBreakpoint(StrEnum):
    """
    Responsive layout breakpoints.
    """

    MOBILE = "mobile"

    TABLET = "tablet"

    DESKTOP = "desktop"
