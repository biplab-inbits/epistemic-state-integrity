import z3

from src.esi.evidence_events import EvidenceAction, EvidenceEvent
from src.esi.formal_state import EpistemicStatus, classify_proposition
from src.esi.revision import RevisableEvidenceState


def test_add_and_retract():
    A = z3.Bool("A")

    state = RevisableEvidenceState()

    state.apply(
        EvidenceEvent(
            action=EvidenceAction.ADD,
            statement=A,
            name="initial_A",
        )
    )

    assert state.evidence == [A]

    state.apply(
        EvidenceEvent(
            action=EvidenceAction.RETRACT,
            statement=A,
            name="retract_A",
        )
    )

    assert state.evidence == []


def test_retraction_changes_epistemic_status():
    A = z3.Bool("A")

    state = RevisableEvidenceState()

    state.apply(
        EvidenceEvent(
            action=EvidenceAction.ADD,
            statement=A,
        )
    )

    status_before = classify_proposition(
        state.evidence,
        A,
    )

    state.apply(
        EvidenceEvent(
            action=EvidenceAction.RETRACT,
            statement=A,
        )
    )

    status_after = classify_proposition(
        state.evidence,
        A,
    )

    assert status_before == EpistemicStatus.ENTAILED
    assert status_after == EpistemicStatus.UNDETERMINED


def test_replacement_changes_state():
    A = z3.Bool("A")
    not_A = z3.Not(A)

    state = RevisableEvidenceState()

    state.apply(
        EvidenceEvent(
            action=EvidenceAction.ADD,
            statement=A,
        )
    )

    state.apply(
        EvidenceEvent(
            action=EvidenceAction.REPLACE,
            statement=A,
            replacement=not_A,
        )
    )

    status = classify_proposition(
        state.evidence,
        A,
    )

    assert status == EpistemicStatus.REFUTED