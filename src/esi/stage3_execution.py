from __future__ import annotations

from dataclasses import dataclass

from .stage3_commitment import (
    Stage3Condition,
    Stage3Scenario,
)


@dataclass(frozen=True)
class Stage3ExecutionSpec:
    """
    Defines what the model executor must do.

    Important:
    The late conditions require TWO model generations.
    """

    scenario_id: str
    domain: str
    dependency_depth: int
    condition: str

    initial_messages: tuple[str, ...]

    # For late conditions, this is the user request that triggers
    # the first model generation.
    pre_retraction_task: str | None

    # Evidence added after the first model generation.
    retraction_message: str

    # Final user request after the retraction.
    final_messages: tuple[str, ...]

    formal_oracle: dict[str, str]


def build_execution_spec(
    scenario: Stage3Scenario,
) -> Stage3ExecutionSpec:

    messages = list(scenario.messages)

    if scenario.condition == Stage3Condition.EARLY_RETRACTION:

        # One model generation:
        #
        # initial evidence
        # -> retraction
        # -> final question
        #
        return Stage3ExecutionSpec(
            scenario_id=scenario.scenario_id,
            domain=scenario.domain,
            dependency_depth=scenario.dependency_depth,
            condition=scenario.condition.value,

            initial_messages=(
                messages[0],
            ),

            pre_retraction_task=None,

            retraction_message=messages[1],

            final_messages=(
                messages[2],
            ),

            formal_oracle=scenario.formal_oracle,
        )

    if scenario.condition == Stage3Condition.LATE_RETRACTION:

        # TWO model generations:
        #
        # initial evidence
        # -> model generates R0
        # -> retraction
        # -> final question
        #
        return Stage3ExecutionSpec(
            scenario_id=scenario.scenario_id,
            domain=scenario.domain,
            dependency_depth=scenario.dependency_depth,
            condition=scenario.condition.value,

            initial_messages=(
                messages[0],
            ),

            pre_retraction_task=messages[1],

            retraction_message=messages[2],

            final_messages=(
                messages[3],
            ),

            formal_oracle=scenario.formal_oracle,
        )

    if (
        scenario.condition
        == Stage3Condition.LATE_RETRACTION_REDERIVE
    ):

        # TWO model generations:
        #
        # initial evidence
        # -> model generates R0
        # -> retraction
        # -> explicit reassessment + final action request
        # -> model generates R1/action
        #
        return Stage3ExecutionSpec(
            scenario_id=scenario.scenario_id,
            domain=scenario.domain,
            dependency_depth=scenario.dependency_depth,
            condition=scenario.condition.value,

            initial_messages=(
                messages[0],
            ),

            pre_retraction_task=messages[1],

            retraction_message=messages[2],

            final_messages=(
                messages[3],
                messages[4],
            ),

            formal_oracle=scenario.formal_oracle,
        )

    raise ValueError(
        f"Unsupported condition: {scenario.condition}"
    )