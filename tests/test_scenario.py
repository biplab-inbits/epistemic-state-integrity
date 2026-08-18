from src.esi.action import Action
from src.esi.formal_state import EpistemicStatus
from src.esi.scenario import build_authorization_revocation_scenario


def test_authorization_revision_changes_formal_state():
    scenario = build_authorization_revocation_scenario()

    assert scenario.initial_status == EpistemicStatus.ENTAILED
    assert scenario.revised_status == EpistemicStatus.REFUTED


def test_authorization_revision_changes_action():
    scenario = build_authorization_revocation_scenario()

    assert scenario.initial_action == Action.PROCEED
    assert scenario.revised_action == Action.DO_NOT_PROCEED