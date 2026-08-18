from src.esi.dependency import DependencyGraph, DependencyNode
from src.esi.retraction import retract


def build_retraction_graph() -> DependencyGraph:
    return DependencyGraph(
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


def test_retraction_propagates_transitively():
    graph = build_retraction_graph()

    result = retract(
        graph,
        "credential_valid",
    )

    assert result.retracted == "credential_valid"

    assert result.invalidated_descendants == frozenset(
        {
            "user_authorized",
            "access_permitted",
            "proceed",
        }
    )


def test_retraction_does_not_invalidate_unrelated_nodes():
    graph = DependencyGraph(
        nodes={
            "credential_valid": DependencyNode(
                name="credential_valid",
            ),
            "user_authorized": DependencyNode(
                name="user_authorized",
                parents=("credential_valid",),
            ),
            "unrelated_fact": DependencyNode(
                name="unrelated_fact",
            ),
        }
    )

    result = retract(
        graph,
        "credential_valid",
    )

    assert result.invalidated_descendants == frozenset(
        {
            "user_authorized",
        }
    )