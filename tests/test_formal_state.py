import z3

from src.esi.formal_state import (
    EpistemicStatus,
    classify_proposition,
)


def test_entailed():
    A = z3.Bool("A")
    B = z3.Bool("B")

    evidence = [
        z3.Implies(A, B),
        A,
    ]

    result = classify_proposition(evidence, B)

    assert result == EpistemicStatus.ENTAILED


def test_refuted():
    A = z3.Bool("A")

    evidence = [
        z3.Not(A),
    ]

    result = classify_proposition(evidence, A)

    assert result == EpistemicStatus.REFUTED


def test_undetermined():
    A = z3.Bool("A")

    evidence = []

    result = classify_proposition(evidence, A)

    assert result == EpistemicStatus.UNDETERMINED


def test_contradictory():
    A = z3.Bool("A")

    evidence = [
        A,
        z3.Not(A),
    ]

    result = classify_proposition(evidence, A)

    assert result == EpistemicStatus.CONTRADICTORY