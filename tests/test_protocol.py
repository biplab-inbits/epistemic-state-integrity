from src.esi.protocol_scenarios import (
    build_authorization_sequential_scenario,
)
from src.esi.sequential_prompt import render_sequential_messages


def test_sequential_scenario_has_three_messages():
    scenario = build_authorization_sequential_scenario()

    messages = render_sequential_messages(scenario)

    assert len(messages) == 3


def test_messages_are_in_temporal_order():
    scenario = build_authorization_sequential_scenario()

    messages = render_sequential_messages(scenario)

    assert "currently authorized" in messages[0]
    assert "revoked" in messages[1]
    assert "allowed" in messages[2]


def test_formal_ground_truth_is_preserved():
    scenario = build_authorization_sequential_scenario()

    assert scenario.initial_status == "entailed"
    assert scenario.revised_status == "refuted"

    assert scenario.initial_action == "proceed"
    assert scenario.revised_action == "do_not_proceed"