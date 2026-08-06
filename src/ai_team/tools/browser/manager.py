"""
Browser manager.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    async_playwright,
)

from ai_team.tools.browser.models import (
    BrowserSession,
)


class BrowserManager:
    """
    Thin wrapper around Playwright.
    """

    def __init__(self) -> None:

        self._playwright = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

        self._sessions: dict[
            UUID,
            Page,
        ] = {}

    # ---------------------------------------------------------

    async def start(
        self,
    ) -> None:

        if self._browser is not None:
            return

        self._playwright = (
            await async_playwright().start()
        )

        self._browser = (
            await self._playwright.chromium.launch(
                headless=True,
            )
        )

        self._context = (
            await self._browser.new_context()
        )

    async def stop(
        self,
    ) -> None:

        for page in self._sessions.values():
            await page.close()

        self._sessions.clear()

        if self._context:
            await self._context.close()

        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()

        self._context = None
        self._browser = None
        self._playwright = None

    # ---------------------------------------------------------

    async def goto(
        self,
        url: str,
    ) -> BrowserSession:

        await self.start()

        page = await self._context.new_page()

        await page.goto(
            url,
            wait_until="networkidle",
        )

        session = BrowserSession(
            id=uuid4(),
        )

        self._sessions[
            session.id
        ] = page

        return session

    # ---------------------------------------------------------

    async def content(
        self,
        session: BrowserSession,
    ) -> str:

        return await self._page(
            session,
        ).content()

    async def title(
        self,
        session: BrowserSession,
    ) -> str:

        return await self._page(
            session,
        ).title()

    async def click(
        self,
        session: BrowserSession,
        selector: str,
    ) -> None:

        await self._page(
            session,
        ).click(
            selector,
        )

    async def fill(
        self,
        session: BrowserSession,
        selector: str,
        value: str,
    ) -> None:

        await self._page(
            session,
        ).fill(
            selector,
            value,
        )

    async def evaluate(
        self,
        session: BrowserSession,
        javascript: str,
    ) -> Any:

        return await self._page(
            session,
        ).evaluate(
            javascript,
        )

    async def screenshot(
        self,
        session: BrowserSession,
        path: str,
    ) -> None:

        await self._page(
            session,
        ).screenshot(
            path=path,
            full_page=True,
        )

    async def close(
        self,
        session: BrowserSession,
    ) -> None:

        page = self._page(
            session,
        )

        await page.close()

        self._sessions.pop(
            session.id,
            None,
        )

    # ---------------------------------------------------------

    def _page(
        self,
        session: BrowserSession,
    ) -> Page:

        page = self._sessions.get(
            session.id,
        )

        if page is None:
            raise ValueError(
                f"Unknown browser session: {session.id}"
            )

        return page