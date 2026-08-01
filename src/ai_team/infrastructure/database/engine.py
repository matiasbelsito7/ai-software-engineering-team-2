```python
"""
SQLAlchemy async engine.

Creates and exposes the application's shared AsyncEngine.

This module is responsible ONLY for engine creation.

It does NOT create sessions.

Sessions belong to:

    infrastructure/database/session.py
"""

from __future__ import annotations

from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from ai_team.infrastructure.config.settings import settings


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """
    Create the application's shared AsyncEngine.

    The engine is instantiated only once and reused throughout
    the application's lifetime.
    """

    db = settings.database

    return create_async_engine(
        db.url,
        echo=db.echo,
        pool_pre_ping=db.pool_pre_ping,
        pool_size=db.pool_size,
        max_overflow=db.max_overflow,
        pool_timeout=db.pool_timeout,
        pool_recycle=db.pool_recycle,
        future=True,
    )


engine: AsyncEngine = get_engine()
```
