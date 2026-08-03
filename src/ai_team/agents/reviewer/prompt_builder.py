"""
Prompt builder for the Reviewer agent.
"""

from ai_team.agents.prompt_builder import BasePromptBuilder

class ReviewerPromptBuilder(BasePromptBuilder):

    PROMPT_PACKAGE = "ai_team.agents.reviewer.prompts"

    TASK_PROMPT = "review.md"