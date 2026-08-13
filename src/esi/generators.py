from __future__ import annotations

from dataclasses import dataclass
import random

import z3

from .evidence import EvidenceHistory
from .equivalence import are_logically_equivalent
from .formal_state import EpistemicStatus, classify_proposition


@dataclass(frozen=True)
class HistoryPair:
    """
    Two evidence histories containing the same logical evidence
    but presented in different orders.
    """

    history_a: EvidenceHistory
    history_b: EvidenceHistory
    proposition: z3.BoolRef
    expected_status: EpistemicStatus


def generate_history_pair(
    seed: int,
    num_atoms: int = 4,
    num_rules: int = 2,
    num_facts: int = 2,
) -> HistoryPair:
    """
    Generate two histories containing identical logical evidence
    in different orders.

    The random seed makes the experiment exactly reproducible.
    """

    if num_atoms < 2:
        raise ValueError("num_atoms must be at least 2.")

    if num_rules < 1:
        raise ValueError("num_rules must be at least 1.")

    if num_facts < 1:
        raise ValueError("num_facts must be at least 1.")

    rng = random.Random(seed)

    atoms = [
        z3.Bool(f"A{i}")
        for i in range(num_atoms)
    ]

    # ------------------------------------------------------------
    # Generate simple implication rules.
    # ------------------------------------------------------------
    rules: list[z3.BoolRef] = []

    used_pairs: set[tuple[int, int]] = set()

    while len(rules) < num_rules:
        source_index, target_index = rng.sample(
            range(num_atoms),
            2,
        )

        pair = (source_index, target_index)

        if pair in used_pairs:
            continue

        used_pairs.add(pair)

        rules.append(
            z3.Implies(
                atoms[source_index],
                atoms[target_index],
            )
        )

    # ------------------------------------------------------------
    # Generate facts.
    # ------------------------------------------------------------
    facts: list[z3.BoolRef] = []

    fact_indices = rng.sample(
        range(num_atoms),
        min(num_facts, num_atoms),
    )

    for index in fact_indices:
        facts.append(atoms[index])

    evidence = rules + facts

    # ------------------------------------------------------------
    # Choose a proposition already represented in the environment.
    # ------------------------------------------------------------
    proposition = rng.choice(atoms)

    # ------------------------------------------------------------
    # Construct History A.
    # ------------------------------------------------------------
    history_a = EvidenceHistory()

    for index, statement in enumerate(evidence):
        history_a.add(
            name=f"evidence_{index}",
            statement=statement,
        )

    # ------------------------------------------------------------
    # Construct History B using a deterministic permutation.
    # ------------------------------------------------------------
    permutation = list(range(len(evidence)))
    rng.shuffle(permutation)

    # Avoid accidentally producing exactly the same ordering.
    if permutation == list(range(len(evidence))) and len(permutation) > 1:
        permutation[0], permutation[1] = (
            permutation[1],
            permutation[0],
        )

    history_b = EvidenceHistory()

    for new_index, old_index in enumerate(permutation):
        history_b.add(
            name=f"evidence_{new_index}",
            statement=evidence[old_index],
        )

    # ------------------------------------------------------------
    # Verify our generator's own invariant.
    # ------------------------------------------------------------
    if not are_logically_equivalent(history_a, history_b):
        raise RuntimeError(
            "Generator produced histories that are not logically equivalent."
        )

    # ------------------------------------------------------------
    # Determine formal ground truth.
    # ------------------------------------------------------------
    expected_status = classify_proposition(
        [step.statement for step in history_a.steps],
        proposition,
    )

    return HistoryPair(
        history_a=history_a,
        history_b=history_b,
        proposition=proposition,
        expected_status=expected_status,
    )