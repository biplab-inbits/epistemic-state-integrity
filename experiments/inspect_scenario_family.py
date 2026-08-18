from src.esi.scenario_family import build_scenario_family


def main():
    family = build_scenario_family()

    for scenario in family:
        print("=" * 70)
        print(f"ID: {scenario.scenario_id}")
        print(f"DOMAIN: {scenario.domain.value}")
        print(f"PROPOSITION: {scenario.proposition}")

        print("\nINITIAL EVIDENCE:")
        print(scenario.initial_text)

        print("\nREVISION EVIDENCE:")
        print(scenario.revision_text)

        print("\nQUESTION:")
        print(scenario.question_text)

        print("\nFORMAL GROUND TRUTH:")
        print(
            f"{scenario.initial_status.value}"
            f" -> "
            f"{scenario.revised_status.value}"
        )

        print("\nNORMATIVE ACTION:")
        print(
            f"{scenario.initial_action.value}"
            f" -> "
            f"{scenario.revised_action.value}"
        )

        print()


if __name__ == "__main__":
    main()