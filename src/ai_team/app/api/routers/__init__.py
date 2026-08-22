"""
API routers package.
"""

from ai_team.app.api.routers.deployment import router as deployment_router
from ai_team.app.api.routers.feedback import router as feedback_router
from ai_team.app.api.routers.health import router as health_router
from ai_team.app.api.routers.review import router as review_router
from ai_team.app.api.routers.streaming import router as streaming_router
from ai_team.app.api.routers.tasks import router as tasks_router
from ai_team.app.api.routers.templates import router as templates_router
from ai_team.app.api.routers.testing import router as testing_router
from ai_team.app.api.routers.ws import router as ws_router

__all__ = [
    "deployment_router",
    "feedback_router",
    "health_router",
    "review_router",
    "streaming_router",
    "tasks_router",
    "templates_router",
    "testing_router",
    "ws_router",
]
