from src.esi.action import Action
from src.esi.retraction_scenario import (
    build_credential_retraction_scenario,
)


def test_retraction_reaches_action_node():
    scenario = build_credential_retraction_scenario()

    assert (
        "proceed"
        in scenario.retraction_result.invalidated_descendants
    )


def test_retraction_changes_normative_action():
    scenario = build_credential_retraction_scenario()

    assert scenario.initial_action == Action.PROCEED
    assert scenario.revised_action == Action.DO_NOT_PROCEED