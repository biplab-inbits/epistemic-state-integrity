from src.esi.action import Action
from src.esi.formal_state import EpistemicStatus

from src.esi.stage3_commitment import (
    Stage3Condition,
    build_stage3_pilot_scenarios,
    build_stage3_scenario,
)


def test_stage3_formal_oracle_is_identical_across_conditions():
    scenarios = [
        build_stage3_scenario(
            domain="authorization",
            depth=4,
            condition=condition,
            scenario_id=f"oracle_{condition.value}",
        )
        for condition in Stage3Condition
    ]

    for scenario in scenarios:
        assert (
            scenario.formal_oracle["initial_status"]
            == EpistemicStatus.ENTAILED.value
        )

        assert (
            scenario.formal_oracle["revised_status"]
            == EpistemicStatus.REFUTED.value
        )

        assert (
            scenario.formal_oracle["initial_action"]
            == Action.PROCEED.value
        )

        assert (
            scenario.formal_oracle["revised_action"]
            == Action.DO_NOT_PROCEED.value
        )


def test_stage3_dependency_depth():
    for depth in (2, 4):

        scenario = build_stage3_scenario(
            domain="authorization",
            depth=depth,
            condition=Stage3Condition.LATE_RETRACTION,
            scenario_id=f"depth_{depth}",
        )

        assert (
            len(scenario.dependency_nodes)
            == depth
        )


def test_early_retraction_has_three_messages():
    scenario = build_stage3_scenario(
        domain="authorization",
        depth=2,
        condition=Stage3Condition.EARLY_RETRACTION,
        scenario_id="early",
    )

    assert len(scenario.messages) == 3


def test_late_retraction_has_pre_retraction_derivation():
    scenario = build_stage3_scenario(
        domain="authorization",
        depth=2,
        condition=Stage3Condition.LATE_RETRACTION,
        scenario_id="late",
    )

    assert len(scenario.messages) == 4

    assert (
        "prepare the operation for execution"
        in scenario.messages[1].lower()
    )

    assert (
        "retracted"
        not in scenario.messages[1].lower()
    )


def test_rederive_condition_explicitly_requests_reassessment():
    scenario = build_stage3_scenario(
        domain="authorization",
        depth=2,
        condition=Stage3Condition.LATE_RETRACTION_REDERIVE,
        scenario_id="rederive",
    )

    assert len(scenario.messages) == 5

    assert (
        "re-evaluate the current information"
        in scenario.messages[3].lower()
    )


def test_stage3_pilot_size():
    scenarios = build_stage3_pilot_scenarios()

    # 4 domains × 2 depths × 3 conditions.
    assert len(scenarios) == 24