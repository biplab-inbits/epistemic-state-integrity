from src.esi.retraction_scenario import (
    build_credential_retraction_scenario,
)


def main():
    scenario = build_credential_retraction_scenario()

    print("SCENARIO")
    print("========")
    print(scenario.scenario_id)

    print("\nDEPENDENCY GRAPH")
    print("================")

    for node in scenario.graph.nodes.values():
        if node.parents:
            print(
                f"{' + '.join(node.parents)}"
                f" -> "
                f"{node.name}"
            )
        else:
            print(node.name)

    print("\nRETRACTED PREMISE")
    print("=================")
    print(scenario.revoked_premise)

    print("\nINVALIDATED DESCENDANTS")
    print("=======================")

    for node in sorted(
        scenario.retraction_result.invalidated_descendants
    ):
        print(node)

    print("\nNORMATIVE ACTION")
    print("================")
    print(
        f"{scenario.initial_action.value}"
        f" -> "
        f"{scenario.revised_action.value}"
    )


if __name__ == "__main__":
    main()