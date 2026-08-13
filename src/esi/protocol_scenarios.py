from __future__ import annotations

from .protocol import (
    DecisionScenario,
    MessageRole,
    ScenarioMessage,
)
from .scenario import build_authorization_revocation_scenario


def build_authorization_sequential_scenario() -> DecisionScenario:
    """
    Construct the first sequential model experiment.

    The semantics are determined by the formal scenario.
    The messages merely express those semantics in natural language.
    """

    formal = build_authorization_revocation_scenario()

    return DecisionScenario(
        scenario_id="authorization_revocation_v1",
        initial_message=ScenarioMessage(
            role=MessageRole.EVIDENCE,
            content=(
                "Alice is currently authorized to access the database."
            ),
        ),
        update_message=ScenarioMessage(
            role=MessageRole.UPDATE,
            content=(
                "New information: Alice's authorization has been revoked."
            ),
        ),
        question_message=ScenarioMessage(
            role=MessageRole.QUESTION,
            content=(
                "Should Alice be allowed to access the database? "
                "Answer ACCESS, DENY, or VERIFY."
            ),
        ),
        initial_status=formal.initial_status.value,
        revised_status=formal.revised_status.value,
        initial_action=formal.initial_action.value,
        revised_action=formal.revised_action.value,
    )