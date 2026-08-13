from src.esi.prompting import build_revision_prompt
from src.esi.scenario import build_authorization_revocation_scenario


def main():
    scenario = build_authorization_revocation_scenario()

    print("FORMAL PROPOSITION")
    print("===================")
    print(scenario.proposition)

    print("\nFORMAL INITIAL STATUS")
    print("=====================")
    print(scenario.initial_status.value)

    print("\nFORMAL INITIAL ACTION")
    print("=====================")
    print(scenario.initial_action.value)

    print("\nFORMAL REVISED STATUS")
    print("=====================")
    print(scenario.revised_status.value)

    print("\nFORMAL REVISED ACTION")
    print("=====================")
    print(scenario.revised_action.value)

    print("\nMODEL PROMPT")
    print("============")
    print(build_revision_prompt(scenario))


if __name__ == "__main__":
    main()