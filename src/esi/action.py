from __future__ import annotations

from enum import Enum

from .formal_state import EpistemicStatus


class Action(str, Enum):
    PROCEED = "proceed"
    DO_NOT_PROCEED = "do_not_proceed"
    VERIFY = "verify"


def choose_action(status: EpistemicStatus) -> Action:
    """
    Normative policy for the controlled experiments.

    ENTAILED:
        The relevant proposition is established, so proceed.

    REFUTED:
        The proposition is ruled out, so do not proceed.

    UNDETERMINED / CONTRADICTORY:
        The evidence does not support a decisive action, so verify.
    """

    if status == EpistemicStatus.ENTAILED:
        return Action.PROCEED

    if status == EpistemicStatus.REFUTED:
        return Action.DO_NOT_PROCEED

    return Action.VERIFY