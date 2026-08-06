"""
Browser tool factory.
"""

from __future__ import annotations

from ai_team.tools.browser.browser import (
    BrowserTool,
)
from ai_team.tools.browser.manager import (
    BrowserManager,
)
from ai_team.tools.browser.policy import (
    BrowserPolicy,
)


def build_browser_tool(
    *,
    manager: BrowserManager,
) -> BrowserTool:

    policy = BrowserPolicy()

    return BrowserTool(
        manager=manager,
        policy=policy,
    )