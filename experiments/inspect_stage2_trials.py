from __future__ import annotations

import json
from pathlib import Path


TRIALS_PATH = Path("experiments/stage2_trials.jsonl")


def main() -> None:
    if not TRIALS_PATH.exists():
        raise FileNotFoundError(
            f"Missing: {TRIALS_PATH}"
        )

    records = []

    with TRIALS_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        for line in f:
            line = line.strip()

            if line:
                records.append(json.loads(line))

    print("=" * 80)
    print("STAGE-2 TRIAL INSPECTION")
    print("=" * 80)
    print(f"Records: {len(records)}")

    # --------------------------------------------------------
    # Basic integrity check
    # --------------------------------------------------------

    expected_conditions = {
        "sequential",
        "flattened",
    }

    depths = sorted(
        {
            record["dependency_depth"]
            for record in records
        }
    )

    domains = sorted(
        {
            record["domain"]
            for record in records
        }
    )

    conditions = {
        record["condition"]
        for record in records
    }

    print(f"Domains: {domains}")
    print(f"Depths: {depths}")
    print(f"Conditions: {sorted(conditions)}")

    assert conditions == expected_conditions

    # --------------------------------------------------------
    # Print representative cases
    #
    # We want:
    # - every domain at depth 1 sequential
    # - every domain at depth 4 sequential
    # - every domain at depth 4 flattened
    # --------------------------------------------------------

    selected = []

    for record in records:
        domain = record["domain"]
        depth = record["dependency_depth"]
        condition = record["condition"]

        if (
            depth == 1
            and condition == "sequential"
        ):
            selected.append(record)

        elif (
            depth == 4
            and condition in {
                "sequential",
                "flattened",
            }
        ):
            selected.append(record)

    selected.sort(
        key=lambda r: (
            r["domain"],
            r["dependency_depth"],
            r["condition"],
        )
    )

    print("\n" + "=" * 80)
    print("REPRESENTATIVE PROMPTS")
    print("=" * 80)

    for record in selected:
        print("\n" + "-" * 80)
        print(
            f"Scenario: {record['scenario_id']}"
        )
        print(
            f"Domain: {record['domain']}"
        )
        print(
            f"Depth: {record['dependency_depth']}"
        )
        print(
            f"Condition: {record['condition']}"
        )

        print("\nFormal oracle:")
        print(
            json.dumps(
                record["formal_oracle"],
                indent=2,
                ensure_ascii=False,
            )
        )

        print("\nMessages:")
        for i, message in enumerate(
            record["messages"],
            start=1,
        ):
            print(
                f"\n--- Message {i} ---"
            )
            print(message)

    print("\n" + "=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()