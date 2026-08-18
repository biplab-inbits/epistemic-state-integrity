from src.esi.action import Action, choose_action
from src.esi.formal_state import EpistemicStatus


def test_entailed_allows_proceed():
    assert choose_action(EpistemicStatus.ENTAILED) == Action.PROCEED


def test_refuted_blocks_proceeding():
    assert choose_action(EpistemicStatus.REFUTED) == Action.DO_NOT_PROCEED


def test_undetermined_requires_verification():
    assert choose_action(EpistemicStatus.UNDETERMINED) == Action.VERIFY


def test_contradictory_requires_verification():
    assert choose_action(EpistemicStatus.CONTRADICTORY) == Action.VERIFY