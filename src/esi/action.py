from __future__ import annotations

from enum import Enum

from .formal_state import EpistemicStatus


class Action(str, Enum):
    ACCESS = "access"
    DENY = "deny"
    VERIFY = "verify"


def choose_action(status: EpistemicStatus) -> Action:
    """
    Normative action policy for the controlled experiment.

    ENTAILED:
        Access is justified.

    REFUTED:
        Access is not justified.

    UNDETERMINED:
        Verify before acting.

    CONTRADICTORY:
        Verify before acting.
    """

    if status == EpistemicStatus.ENTAILED:
        return Action.ACCESS

    if status == EpistemicStatus.REFUTED:
        return Action.DENY

    return Action.VERIFY