import z3

from src.esi.evidence import EvidenceHistory
from src.esi.formal_state import EpistemicStatus


def test_evidence_history_tracks_state_change():
    A = z3.Bool("A")
    B = z3.Bool("B")

    history = EvidenceHistory()

    # At first: A -> B
    history.add("implication", z3.Implies(A, B))

    # Then: A
    history.add("fact_A", A)

    statuses = history.statuses(B)

    assert statuses == [
        EpistemicStatus.UNDETERMINED,
        EpistemicStatus.ENTAILED,
    ]


def test_evidence_history_tracks_refutation():
    A = z3.Bool("A")

    history = EvidenceHistory()

    history.add("not_A", z3.Not(A))

    statuses = history.statuses(A)

    assert statuses == [
        EpistemicStatus.REFUTED,
    ]


def test_evidence_history_detects_contradiction():
    A = z3.Bool("A")

    history = EvidenceHistory()

    history.add("A", A)
    history.add("not_A", z3.Not(A))

    statuses = history.statuses(A)

    assert statuses == [
        EpistemicStatus.ENTAILED,
        EpistemicStatus.CONTRADICTORY,
    ]