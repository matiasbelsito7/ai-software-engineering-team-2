"""
Typed outputs produced by AI agents.
"""

from ai_team.agents.outputs.architect import (
    ArchitectureComponent,
    ArchitectureDecision,
    ArchitectOutput,
)
from ai_team.agents.outputs.backend import BackendOutput
from ai_team.agents.outputs.database import (
    DatabaseChange,
    DatabaseOutput,
)
from ai_team.agents.outputs.devops import DevOpsOutput
from ai_team.agents.outputs.documentation import (
    DocumentationFile,
    DocumentationOutput,
)
from ai_team.agents.outputs.frontend import (
    FrontendOutput,
    UIComponent,
)
from ai_team.agents.outputs.planner import (
    PlanStep,
    PlannerOutput,
)
from ai_team.agents.outputs.qa import (
    QAOutput,
    TestResult,
)
from ai_team.agents.outputs.reviewer import ReviewerOutput

__all__ = [
    "ArchitectureComponent",
    "ArchitectureDecision",
    "ArchitectOutput",
    "BackendOutput",
    "DatabaseChange",
    "DatabaseOutput",
    "DevOpsOutput",
    "DocumentationFile",
    "DocumentationOutput",
    "FrontendOutput",
    "UIComponent",
    "PlanStep",
    "PlannerOutput",
    "QAOutput",
    "TestResult",
    "ReviewerOutput",
]