from src.esi.formal_state import classify_proposition
from src.esi.generators import generate_history_pair


def print_history(label, history, proposition):
    print(f"\n{label}")
    print("=" * len(label))

    for time_step, step in enumerate(history.steps):
        evidence = [
            previous_step.statement
            for previous_step in history.steps[: time_step + 1]
        ]

        status = classify_proposition(
            evidence,
            proposition,
        )

        print(
            f"t={time_step} | "
            f"{step.statement} | "
            f"formal status = {status.value}"
        )


def main():
    pair = generate_history_pair(
        seed=42,
        num_atoms=4,
        num_rules=2,
        num_facts=2,
    )

    print("PROPOSITION")
    print("===========")
    print(pair.proposition)

    print_history(
        "HISTORY A",
        pair.history_a,
        pair.proposition,
    )

    print_history(
        "HISTORY B",
        pair.history_b,
        pair.proposition,
    )

    print("\nFINAL CHECK")
    print("===========")
    print(
        f"Expected final status: "
        f"{pair.expected_status.value}"
    )


if __name__ == "__main__":
    main()