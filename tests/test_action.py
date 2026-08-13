from src.esi.action import Action, choose_action
from src.esi.formal_state import EpistemicStatus


def test_entailed_allows_access():
    assert choose_action(EpistemicStatus.ENTAILED) == Action.ACCESS


def test_refuted_denies_access():
    assert choose_action(EpistemicStatus.REFUTED) == Action.DENY


def test_undetermined_requires_verification():
    assert choose_action(EpistemicStatus.UNDETERMINED) == Action.VERIFY


def test_contradictory_requires_verification():
    assert choose_action(EpistemicStatus.CONTRADICTORY) == Action.VERIFY