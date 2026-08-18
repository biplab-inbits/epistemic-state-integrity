from __future__ import annotations

import json
from pathlib import Path


INPUT = Path(
    "experiments/stage3_trials.jsonl"
)


def main() -> None:
    records = []

    with INPUT.open(
        "r",
        encoding="utf-8",
    ) as f:

        for line in f:
            if line.strip():
                records.append(
                    json.loads(line)
                )

    print("=" * 80)
    print("STAGE-3 TRIAL INSPECTION")
    print("=" * 80)

    print("Records:", len(records))

    for record in records:

        if not (
            record["dependency_depth"] == 4
        ):
            continue

        print("\n" + "-" * 80)

        print(
            record["scenario_id"],
            "| condition =",
            record["condition"],
        )

        print("\nFORMAL ORACLE:")
        print(
            json.dumps(
                record["formal_oracle"],
                indent=2,
            )
        )

        print("\nMESSAGES:")

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