from __future__ import annotations

import z3

from .evidence_events import EvidenceAction, EvidenceEvent


class RevisableEvidenceState:
    """
    Maintains the currently active evidence set.

    Evidence can be added, retracted, or replaced.
    """

    def __init__(self) -> None:
        self._evidence: list[z3.BoolRef] = []

    @property
    def evidence(self) -> list[z3.BoolRef]:
        """Return a copy of the currently active evidence."""
        return list(self._evidence)

    def apply(self, event: EvidenceEvent) -> None:
        """Apply one evidence-changing event."""

        if event.action == EvidenceAction.ADD:
            self._evidence.append(event.statement)
            return

        if event.action == EvidenceAction.RETRACT:
            self._retract(event.statement)
            return

        if event.action == EvidenceAction.REPLACE:
            self._retract(event.statement)

            assert event.replacement is not None
            self._evidence.append(event.replacement)
            return

        raise ValueError(f"Unknown evidence action: {event.action}")

    def _retract(self, statement: z3.BoolRef) -> None:
        """Remove exactly one matching statement."""

        for index, existing in enumerate(self._evidence):
            if z3.eq(existing, statement):
                del self._evidence[index]
                return

        raise ValueError(
            f"Cannot retract evidence that is not active: {statement}"
        )