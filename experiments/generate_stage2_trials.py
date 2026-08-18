from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.esi.stage2_behavioral import (
    Stage2Condition,
    build_stage2_pilot_scenarios,
)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/stage2_trials.jsonl"
        ),
    )

    args = parser.parse_args()

    scenarios = build_stage2_pilot_scenarios(
        depths=(1, 2, 3, 4),
        conditions=(
            Stage2Condition.SEQUENTIAL,
            Stage2Condition.FLATTENED,
        ),
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with args.output.open(
        "w",
        encoding="utf-8",
    ) as handle:

        for scenario in scenarios:

            record = {
                "scenario_id": scenario.scenario_id,
                "domain": scenario.domain,
                "dependency_depth": scenario.dependency_depth,
                "condition": scenario.condition.value,
                "messages": list(
                    scenario.messages
                ),
                "formal_oracle": (
                    scenario.formal_oracle
                ),
            }

            handle.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print(
        f"Generated {len(scenarios)} "
        f"validated trials:"
    )
    print(args.output)


if __name__ == "__main__":
    main()