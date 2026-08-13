import z3

from src.esi.equivalence import are_logically_equivalent
from src.esi.formal_state import EpistemicStatus, classify_proposition
from src.esi.generators import generate_history_pair


def test_generated_histories_are_logically_equivalent():
    pair = generate_history_pair(
        seed=42,
        num_atoms=4,
        num_rules=2,
        num_facts=2,
    )

    assert are_logically_equivalent(
        pair.history_a,
        pair.history_b,
    )


def test_generated_histories_have_same_length():
    pair = generate_history_pair(
        seed=123,
        num_atoms=5,
        num_rules=3,
        num_facts=2,
    )

    assert len(pair.history_a.steps) == len(pair.history_b.steps)


def test_generation_is_reproducible():
    pair_a = generate_history_pair(
        seed=999,
        num_atoms=4,
        num_rules=2,
        num_facts=2,
    )

    pair_b = generate_history_pair(
        seed=999,
        num_atoms=4,
        num_rules=2,
        num_facts=2,
    )

    statements_a = [
        str(step.statement)
        for step in pair_a.history_a.steps
    ]

    statements_b = [
        str(step.statement)
        for step in pair_b.history_a.steps
    ]

    assert statements_a == statements_b
    assert str(pair_a.proposition) == str(pair_b.proposition)
    assert pair_a.expected_status == pair_b.expected_status


def test_expected_status_is_valid():
    pair = generate_history_pair(
        seed=7,
        num_atoms=4,
        num_rules=2,
        num_facts=2,
    )

    assert pair.expected_status in {
        EpistemicStatus.ENTAILED,
        EpistemicStatus.REFUTED,
        EpistemicStatus.UNDETERMINED,
        EpistemicStatus.CONTRADICTORY,
    }


def test_both_histories_have_same_final_status():
    pair = generate_history_pair(
        seed=2026,
        num_atoms=5,
        num_rules=3,
        num_facts=2,
    )

    evidence_a = [
        step.statement
        for step in pair.history_a.steps
    ]

    evidence_b = [
        step.statement
        for step in pair.history_b.steps
    ]

    status_a = classify_proposition(
        evidence_a,
        pair.proposition,
    )

    status_b = classify_proposition(
        evidence_b,
        pair.proposition,
    )

    assert status_a == status_b
    assert status_a == pair.expected_status