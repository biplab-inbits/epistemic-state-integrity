from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import z3


class EpistemicStatus(str, Enum):
    """Epistemic status of a proposition relative to a body of evidence."""

    ENTAILED = "entailed"
    REFUTED = "refuted"
    UNDETERMINED = "undetermined"
    CONTRADICTORY = "contradictory"


@dataclass(frozen=True)
class EpistemicState:
    """Ground-truth epistemic state for one proposition."""

    status: EpistemicStatus
    proposition: str


def classify_proposition(
    evidence: list[z3.BoolRef],
    proposition: z3.BoolRef,
) -> EpistemicStatus:
    """
    Determine the logical status of `proposition` given `evidence`.

    Definitions:

    ENTAILED:
        evidence logically entails proposition.

    REFUTED:
        evidence logically entails the negation of proposition.

    UNDETERMINED:
        both proposition and its negation are compatible with the evidence.

    CONTRADICTORY:
        the evidence itself has no satisfying model.
    """

    # ------------------------------------------------------------
    # Step 1: Is the evidence internally consistent?
    # ------------------------------------------------------------
    evidence_solver = z3.Solver()
    evidence_solver.add(*evidence)

    evidence_result = evidence_solver.check()

    if evidence_result == z3.unsat:
        return EpistemicStatus.CONTRADICTORY

    if evidence_result != z3.sat:
        raise RuntimeError(
            f"Z3 returned unexpected result for evidence: {evidence_result}"
        )

    # ------------------------------------------------------------
    # Step 2: Is proposition compatible with the evidence?
    # ------------------------------------------------------------
    proposition_solver = z3.Solver()
    proposition_solver.add(*evidence)
    proposition_solver.add(proposition)

    proposition_result = proposition_solver.check()

    if proposition_result == z3.unknown:
        raise RuntimeError(
            "Z3 returned unknown while checking proposition satisfiability."
        )

    # ------------------------------------------------------------
    # Step 3: Is NOT proposition compatible with the evidence?
    # ------------------------------------------------------------
    negation_solver = z3.Solver()
    negation_solver.add(*evidence)
    negation_solver.add(z3.Not(proposition))

    negation_result = negation_solver.check()

    if negation_result == z3.unknown:
        raise RuntimeError(
            "Z3 returned unknown while checking negated proposition satisfiability."
        )

    proposition_possible = proposition_result == z3.sat
    negation_possible = negation_result == z3.sat

    # ------------------------------------------------------------
    # Step 4: Classify the epistemic status.
    # ------------------------------------------------------------
    if proposition_possible and not negation_possible:
        return EpistemicStatus.ENTAILED

    if not proposition_possible and negation_possible:
        return EpistemicStatus.REFUTED

    if proposition_possible and negation_possible:
        return EpistemicStatus.UNDETERMINED

    # For internally consistent evidence this should not be reachable.
    raise RuntimeError(
        "Inconsistent solver results: neither proposition nor its negation "
        "is satisfiable despite consistent evidence."
    )