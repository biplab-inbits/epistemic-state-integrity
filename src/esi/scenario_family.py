from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import z3

from .action import Action
from .evidence_events import EvidenceAction, EvidenceEvent
from .formal_state import EpistemicStatus, classify_proposition
from .revision import RevisableEvidenceState


class ScenarioDomain(str, Enum):
    AUTHORIZATION = "authorization"
    DOCUMENT_VALIDITY = "document_validity"
    RESOURCE_AVAILABILITY = "resource_availability"
    TASK_PRECONDITION = "task_precondition"


@dataclass(frozen=True)
class ScenarioFamilyMember:
    """
    One controlled scenario whose formal semantics are shared
    with other scenarios in the family.
    """

    scenario_id: str
    domain: ScenarioDomain

    proposition: z3.BoolRef

    initial_event: EvidenceEvent
    revision_event: EvidenceEvent

    initial_status: EpistemicStatus
    revised_status: EpistemicStatus

    initial_action: Action
    revised_action: Action

    initial_text: str
    revision_text: str
    question_text: str


def _build_scenario(
    scenario_id: str,
    domain: ScenarioDomain,
    proposition_name: str,
    initial_text: str,
    revision_text: str,
    question_text: str,
) -> ScenarioFamilyMember:
    """
    Build one scenario and independently verify its formal semantics.
    """

    proposition = z3.Bool(proposition_name)

    initial_event = EvidenceEvent(
        action=EvidenceAction.ADD,
        statement=proposition,
        name=f"{scenario_id}_initial",
    )

    revision_event = EvidenceEvent(
        action=EvidenceAction.REPLACE,
        statement=proposition,
        replacement=z3.Not(proposition),
        name=f"{scenario_id}_revision",
    )

    state = RevisableEvidenceState()

    # Initial state.
    state.apply(initial_event)

    initial_status = classify_proposition(
        state.evidence,
        proposition,
    )

    # Revised state.
    state.apply(revision_event)

    revised_status = classify_proposition(
        state.evidence,
        proposition,
    )

    # ------------------------------------------------------------
    # Strict invariant checks.
    # ------------------------------------------------------------
    if initial_status != EpistemicStatus.ENTAILED:
        raise RuntimeError(
            f"{scenario_id}: expected initial status ENTAILED, "
            f"got {initial_status.value}"
        )

    if revised_status != EpistemicStatus.REFUTED:
        raise RuntimeError(
            f"{scenario_id}: expected revised status REFUTED, "
            f"got {revised_status.value}"
        )

    return ScenarioFamilyMember(
        scenario_id=scenario_id,
        domain=domain,
        proposition=proposition,
        initial_event=initial_event,
        revision_event=revision_event,
        initial_status=initial_status,
        revised_status=revised_status,
        initial_action=Action.PROCEED,
        revised_action=Action.DO_NOT_PROCEED,
        initial_text=initial_text,
        revision_text=revision_text,
        question_text=question_text,
    )


def build_scenario_family() -> list[ScenarioFamilyMember]:
    """
    Build the first controlled family.

    All members implement the same abstract transition:

        ENTAILED -> REFUTED
        PROCEED   -> DO_NOT_PROCEED

    but use different surface domains and language.
    """

    return [
        _build_scenario(
            scenario_id="authorization_001",
            domain=ScenarioDomain.AUTHORIZATION,
            proposition_name="authorized_Alice",
            initial_text=(
                "Alice is currently authorized to access the database."
            ),
            revision_text=(
                "New information: Alice's authorization to access "
                "the database has been revoked."
            ),
            question_text=(
                "Should Alice be allowed to access the database?"
            ),
        ),
        _build_scenario(
            scenario_id="document_001",
            domain=ScenarioDomain.DOCUMENT_VALIDITY,
            proposition_name="valid_DocumentX",
            initial_text=(
                "Document X is currently valid for this operation."
            ),
            revision_text=(
                "New information: Document X has been invalidated "
                "and is no longer valid for this operation."
            ),
            question_text=(
                "Should the agent rely on Document X for the operation?"
            ),
        ),
        _build_scenario(
            scenario_id="resource_001",
            domain=ScenarioDomain.RESOURCE_AVAILABILITY,
            proposition_name="available_ResourceY",
            initial_text=(
                "Resource Y is currently available for the requested task."
            ),
            revision_text=(
                "New information: Resource Y is no longer available "
                "for the requested task."
            ),
            question_text=(
                "Should the agent use Resource Y for the task?"
            ),
        ),
        _build_scenario(
            scenario_id="task_001",
            domain=ScenarioDomain.TASK_PRECONDITION,
            proposition_name="safe_TaskZ",
            initial_text=(
                "Task Z currently satisfies the required preconditions "
                "for execution."
            ),
            revision_text=(
                "New information: Task Z no longer satisfies the "
                "required preconditions for execution."
            ),
            question_text=(
                "Should the agent execute Task Z?"
            ),
        ),
    ]