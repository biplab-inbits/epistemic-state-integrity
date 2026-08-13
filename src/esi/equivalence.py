from __future__ import annotations

import z3

from .evidence import EvidenceHistory


def history_formula(history: EvidenceHistory) -> z3.BoolRef:
    """
    Convert an evidence history into one conjunction representing
    all evidence currently available.

    An empty history is represented as True.
    """

    statements = [step.statement for step in history.steps]

    if not statements:
        return z3.BoolVal(True)

    return z3.And(*statements)


def are_logically_equivalent(
    history_a: EvidenceHistory,
    history_b: EvidenceHistory,
) -> bool:
    """
    Determine whether two evidence histories have logically equivalent
    final evidence states.

    Two formulas F and G are logically equivalent iff:

        F <-> G

    is valid.

    We test validity by asking Z3 whether there exists a counterexample:

        F != G

    If no counterexample exists, the histories are equivalent.
    """

    formula_a = history_formula(history_a)
    formula_b = history_formula(history_b)

    solver = z3.Solver()

    # Search for a model in which the two evidence states differ.
    solver.add(formula_a != formula_b)

    result = solver.check()

    if result == z3.unsat:
        return True

    if result == z3.sat:
        return False

    raise RuntimeError(
        f"Z3 returned unexpected result: {result}"
    )