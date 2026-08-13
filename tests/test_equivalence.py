import z3

from src.esi.evidence import EvidenceHistory
from src.esi.equivalence import are_logically_equivalent


def test_different_order_same_logical_state():
    A = z3.Bool("A")
    B = z3.Bool("B")

    history_a = EvidenceHistory()

    history_a.add(
        "implication",
        z3.Implies(A, B),
    )

    history_a.add(
        "fact_A",
        A,
    )

    history_b = EvidenceHistory()

    history_b.add(
        "fact_A",
        A,
    )

    history_b.add(
        "implication",
        z3.Implies(A, B),
    )

    assert are_logically_equivalent(
        history_a,
        history_b,
    )


def test_different_logical_states_are_not_equivalent():
    A = z3.Bool("A")
    B = z3.Bool("B")

    history_a = EvidenceHistory()

    history_a.add(
        "fact_A",
        A,
    )

    history_b = EvidenceHistory()

    history_b.add(
        "fact_B",
        B,
    )

    assert not are_logically_equivalent(
        history_a,
        history_b,
    )


def test_same_history_is_equivalent():
    A = z3.Bool("A")

    history_a = EvidenceHistory()
    history_a.add("fact_A", A)

    history_b = EvidenceHistory()
    history_b.add("fact_A", A)

    assert are_logically_equivalent(
        history_a,
        history_b,
    )