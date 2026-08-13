from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import z3


class EvidenceAction(str, Enum):
    ADD = "add"
    RETRACT = "retract"
    REPLACE = "replace"


@dataclass(frozen=True)
class EvidenceEvent:
    """
    A change to the active evidence base.

    ADD:
        Introduce a new piece of evidence.

    RETRACT:
        Remove an existing piece of evidence.

    REPLACE:
        Remove one piece of evidence and introduce another.
    """

    action: EvidenceAction
    statement: z3.BoolRef
    replacement: z3.BoolRef | None = None
    name: str = ""

    def __post_init__(self) -> None:
        if self.action == EvidenceAction.REPLACE:
            if self.replacement is None:
                raise ValueError(
                    "REPLACE events require a replacement statement."
                )

        elif self.replacement is not None:
            raise ValueError(
                "Only REPLACE events may specify a replacement."
            )