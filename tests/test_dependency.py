from src.esi.dependency import DependencyGraph, DependencyNode


def build_test_graph() -> DependencyGraph:
    return DependencyGraph(
        nodes={
            "credential_valid": DependencyNode(
                name="credential_valid"
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


def test_direct_descendant():
    graph = build_test_graph()

    descendants = graph.descendants_of("credential_valid")

    assert "user_authorized" in descendants


def test_transitive_descendants():
    graph = build_test_graph()

    descendants = graph.descendants_of("credential_valid")

    assert descendants == {
        "user_authorized",
        "access_permitted",
        "proceed",
    }


def test_leaf_has_no_descendants():
    graph = build_test_graph()

    assert graph.descendants_of("proceed") == set()