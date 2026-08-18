from src.esi.stage3_commitment import (
    Stage3Condition,
    build_stage3_scenario,
)
from src.esi.stage3_execution import (
    build_execution_spec,
)


def test_early_execution_spec_is_single_generation():
    scenario = build_stage3_scenario(
        domain="authorization",
        depth=4,
        condition=Stage3Condition.EARLY_RETRACTION,
        scenario_id="early",
    )

    spec = build_execution_spec(scenario)

    assert spec.pre_retraction_task is None

    assert len(spec.initial_messages) == 1
    assert len(spec.final_messages) == 1


def test_late_execution_spec_requires_two_generations():
    scenario = build_stage3_scenario(
        domain="authorization",
        depth=4,
        condition=Stage3Condition.LATE_RETRACTION,
        scenario_id="late",
    )

    spec = build_execution_spec(scenario)

    assert spec.pre_retraction_task is not None

    assert len(spec.initial_messages) == 1
    assert len(spec.final_messages) == 1


def test_rederive_execution_spec_requires_second_phase():
    scenario = build_stage3_scenario(
        domain="authorization",
        depth=4,
        condition=Stage3Condition.LATE_RETRACTION_REDERIVE,
        scenario_id="rederive",
    )

    spec = build_execution_spec(scenario)

    assert spec.pre_retraction_task is not None

    assert len(spec.initial_messages) == 1

    assert len(spec.final_messages) == 2

    assert (
        "re-evaluate"
        in spec.final_messages[0].lower()
    )