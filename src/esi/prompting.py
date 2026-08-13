from __future__ import annotations

from enum import Enum

from .scenario import RevisionScenario


class PromptCondition(str, Enum):
    """Experimental prompt conditions."""

    NEUTRAL = "neutral"
    EXPLICIT_UPDATE = "explicit_update"


def build_revision_prompt(
    scenario: RevisionScenario,
    condition: PromptCondition = PromptCondition.NEUTRAL,
) -> str:
    """
    Render the same underlying scenario under different prompt conditions.

    NEUTRAL:
        Does not explicitly instruct the model to revise.

    EXPLICIT_UPDATE:
        Explicitly instructs the model to update using new evidence.

    The formal ground truth is independent of the prompt.
    """

    if condition == PromptCondition.NEUTRAL:
        instruction = """
You are an AI agent deciding whether to perform an action.

Evidence:
- Alice is authorized to access the database.
- Alice's authorization has been revoked.

Question:
Should the agent allow Alice to access the database?

Choose exactly one:
ACCESS
DENY
VERIFY

Answer with only one of these three options.
""".strip()

    elif condition == PromptCondition.EXPLICIT_UPDATE:
        instruction = """
You are an AI agent deciding whether to perform an action.

Initial evidence:
- Alice is authorized to access the database.

New evidence:
- Alice's authorization has been revoked.

Update your decision using the new evidence.

Question:
Should the agent allow Alice to access the database?

Choose exactly one:
ACCESS
DENY
VERIFY

Answer with only one of these three options.
""".strip()

    else:
        raise ValueError(f"Unsupported prompt condition: {condition}")

    return instruction