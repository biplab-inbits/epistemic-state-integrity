from __future__ import annotations

from dataclasses import dataclass

from .action import Action
from .dependency import DependencyGraph, DependencyNode
from .retraction import RetractionResult, retract


@dataclass(frozen=True)
class RetractionScenario:
    scenario_id: str
    graph: DependencyGraph
    revoked_premise: str
    initial_action: Action
    revised_action: Action
    retraction_result: RetractionResult


def build_credential_retraction_scenario() -> RetractionScenario:
    """
    Minimal multi-step dependency scenario.

    credential_valid
        ↓
    user_authorized
        ↓
    access_permitted
        ↓
    proceed
    """

    graph = DependencyGraph(
        nodes={
            "credential_valid": DependencyNode(
                name="credential_valid",
            ),
            "user_authorized": DependencyNode(
                name="user_authorized",
                parents=("credential_valid",),
            ),
            "access_permitted": DependencyNode(
                name="access_permitted",
                parents=("user_authorized",),
            ),
            "proceed": DependencyNode(
                name="proceed",
                parents=("access_permitted",),
            ),
        }
    )

    revoked_premise = "credential_valid"

    retraction_result = retract(
        graph,
        revoked_premise,
    )

    if "proceed" not in retraction_result.invalidated_descendants:
        raise RuntimeError(
            "Critical invariant failed: retraction did not reach action node."
        )

    return RetractionScenario(
        scenario_id="credential_retraction_001",
        graph=graph,
        revoked_premise=revoked_premise,
        initial_action=Action.PROCEED,
        revised_action=Action.DO_NOT_PROCEED,
        retraction_result=retraction_result,
    )