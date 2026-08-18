from __future__ import annotations

from dataclasses import dataclass

from .dependency import DependencyGraph


@dataclass(frozen=True)
class RetractionResult:
    """
    Normative consequences of retracting one foundational premise.
    """

    retracted: str
    invalidated_descendants: frozenset[str]


def retract(
    graph: DependencyGraph,
    premise: str,
) -> RetractionResult:
    """
    Compute the nodes whose justification must be reconsidered
    when `premise` is retracted.
    """

    descendants = graph.descendants_of(premise)

    return RetractionResult(
        retracted=premise,
        invalidated_descendants=frozenset(descendants),
    )