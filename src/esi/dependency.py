from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyNode:
    """
    A proposition or action-relevant state in the dependency graph.

    parents:
        Nodes that this node depends on.

    A -> B means:
        B depends on A.
    """

    name: str
    parents: tuple[str, ...] = ()


@dataclass(frozen=True)
class DependencyGraph:
    """
    Directed acyclic dependency structure.

    The graph describes normative dependency, not model behavior.
    """

    nodes: dict[str, DependencyNode]

    def descendants_of(self, name: str) -> set[str]:
        """
        Return all nodes that transitively depend on `name`.
        """

        if name not in self.nodes:
            raise KeyError(f"Unknown node: {name}")

        descendants: set[str] = set()
        frontier = [name]

        while frontier:
            current = frontier.pop()

            for node in self.nodes.values():
                if node.name in descendants:
                    continue

                if current in node.parents:
                    descendants.add(node.name)
                    frontier.append(node.name)

        return descendants

    def dependencies_of(self, name: str) -> set[str]:
        """
        Return all nodes that the given node transitively depends on.
        """

        if name not in self.nodes:
            raise KeyError(f"Unknown node: {name}")

        dependencies: set[str] = set()
        frontier = list(self.nodes[name].parents)

        while frontier:
            current = frontier.pop()

            if current in dependencies:
                continue

            dependencies.add(current)
            frontier.extend(self.nodes[current].parents)

        return dependencies