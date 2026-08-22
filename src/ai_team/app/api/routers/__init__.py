"""
API routers package.
"""

from ai_team.app.api.routers.health import router as health_router
from ai_team.app.api.routers.tasks import router as tasks_router
from ai_team.app.api.routers.ws import router as ws_router

__all__ = [
    "health_router",
    "tasks_router",
    "ws_router",
]
