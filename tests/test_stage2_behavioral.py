from src.esi.action import Action
from src.esi.formal_state import EpistemicStatus

from src.esi.stage2_behavioral import (
    Stage2Condition,
    available_stage2_domains,
    build_stage2_pilot_scenarios,
    build_stage2_scenario,
)


def test_stage2_uses_existing_domains():
    assert set(available_stage2_domains()) == {
        "authorization",
        "document_validity",
        "resource_availability",
        "task_precondition",
    }


def test_stage2_exact_dependency_depth():
    for depth in (1, 2, 3, 4):

        scenario = build_stage2_scenario(
            domain="authorization",
            depth=depth,
            condition=Stage2Condition.SEQUENTIAL,
            scenario_id=f"test_depth_{depth}",
        )

        expected = {
            *(f"c{i}" for i in range(1, depth + 1)),
            "action",
        }

        assert (
            scenario.retraction_result.invalidated_descendants
            == frozenset(expected)
        )


def test_stage2_formal_transition():
    scenario = build_stage2_scenario(
        domain="document_validity",
        depth=4,
        condition=Stage2Condition.SEQUENTIAL,
        scenario_id="test_formal_transition",
    )

    assert (
        scenario.initial_status
        == EpistemicStatus.ENTAILED
    )

    assert (
        scenario.revised_status
        == EpistemicStatus.REFUTED
    )

    assert (
        scenario.initial_action
        == Action.PROCEED
    )

    assert (
        scenario.revised_action
        == Action.DO_NOT_PROCEED
    )


def test_sequential_and_flattened_share_formal_semantics():
    sequential = build_stage2_scenario(
        domain="resource_availability",
        depth=3,
        condition=Stage2Condition.SEQUENTIAL,
        scenario_id="seq",
    )

    flattened = build_stage2_scenario(
        domain="resource_availability",
        depth=3,
        condition=Stage2Condition.FLATTENED,
        scenario_id="flat",
    )

    assert (
        sequential.formal_oracle
        == flattened.formal_oracle
    )

    assert (
        sequential.retraction_result
        == flattened.retraction_result
    )

    assert sequential.graph == flattened.graph

    assert len(sequential.messages) == 3
    assert len(flattened.messages) == 2


def test_stage2_pilot_has_expected_count():
    scenarios = build_stage2_pilot_scenarios()

    # 4 domains × 4 depths × 2 conditions.
    assert len(scenarios) == 32


def test_stage2_messages_are_nonempty():
    for scenario in build_stage2_pilot_scenarios():
        assert all(
            message.strip()
            for message in scenario.messages
        )

        assert (
            "DO_NOT_PROCEED"
            in scenario.messages[-1]
        )