from __future__ import annotations

from dataclasses import dataclass

import z3

from .action import Action, choose_action
from .evidence_events import EvidenceAction, EvidenceEvent
from .formal_state import EpistemicStatus, classify_proposition
from .revision import RevisableEvidenceState


@dataclass(frozen=True)
class RevisionScenario:
    """A minimal evidence-revision scenario."""

    proposition: z3.BoolRef
    initial_event: EvidenceEvent
    revision_event: EvidenceEvent

    initial_status: EpistemicStatus
    revised_status: EpistemicStatus

    initial_action: Action
    revised_action: Action


def build_authorization_revocation_scenario() -> RevisionScenario:
    """
    Construct the simplest possible state-transition scenario.

    Initial state:
        authorized(Alice) is entailed.

    Revision:
        authorized(Alice) is replaced by not authorized(Alice).

    Therefore the normative action changes:
        ACCESS -> DENY
    """

    authorized = z3.Bool("authorized_Alice")

    initial_event = EvidenceEvent(
        action=EvidenceAction.ADD,
        statement=authorized,
        name="initial_authorization",
    )

    revision_event = EvidenceEvent(
        action=EvidenceAction.REPLACE,
        statement=authorized,
        replacement=z3.Not(authorized),
        name="authorization_revoked",
    )

    state = RevisableEvidenceState()

    state.apply(initial_event)

    initial_status = classify_proposition(
        state.evidence,
        authorized,
    )

    initial_action = choose_action(initial_status)

    state.apply(revision_event)

    revised_status = classify_proposition(
        state.evidence,
        authorized,
    )

    revised_action = choose_action(revised_status)

    return RevisionScenario(
        proposition=authorized,
        initial_event=initial_event,
        revision_event=revision_event,
        initial_status=initial_status,
        revised_status=revised_status,
        initial_action=initial_action,
        revised_action=revised_action,
    )