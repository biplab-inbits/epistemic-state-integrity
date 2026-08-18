from __future__ import annotations

import json
from pathlib import Path

from src.esi.stage3_commitment import (
    build_stage3_pilot_scenarios,
)
from src.esi.stage3_execution import (
    build_execution_spec,
)


OUTPUT = Path(
    "experiments/stage3_trials.jsonl"
)


def main() -> None:

    scenarios = build_stage3_pilot_scenarios()

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as f:

        for scenario in scenarios:

            spec = build_execution_spec(
                scenario
            )

            record = {
                "scenario_id": spec.scenario_id,
                "domain": spec.domain,
                "dependency_depth": (
                    spec.dependency_depth
                ),
                "condition": spec.condition,

                "initial_messages": list(
                    spec.initial_messages
                ),

                "pre_retraction_task": (
                    spec.pre_retraction_task
                ),

                "retraction_message": (
                    spec.retraction_message
                ),

                "final_messages": list(
                    spec.final_messages
                ),

                "formal_oracle": (
                    spec.formal_oracle
                ),
            }

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print(
        f"Generated {len(scenarios)} "
        "validated Stage-3 execution specs:"
    )

    print(OUTPUT)


if __name__ == "__main__":
    main()