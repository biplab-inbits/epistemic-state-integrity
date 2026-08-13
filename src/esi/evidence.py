from __future__ import annotations

from dataclasses import dataclass, field

import z3

from .formal_state import EpistemicStatus, classify_proposition


@dataclass
class EvidenceStep:
    """One piece of evidence introduced at a particular time step."""

    name: str
    statement: z3.BoolRef


@dataclass
class EvidenceHistory:
    """
    Ordered sequence of evidence presented to an agent.

    The formal epistemic status is computed from all evidence available
    up to each time step.
    """

    steps: list[EvidenceStep] = field(default_factory=list)

    def add(self, name: str, statement: z3.BoolRef) -> None:
        """Append one new evidence item to the history."""
        self.steps.append(EvidenceStep(name=name, statement=statement))

    def statements_up_to(self, time_step: int) -> list[z3.BoolRef]:
        """
        Return all evidence available through `time_step`.

        time_step=0 means the first evidence item.
        """
        if time_step < 0:
            raise ValueError("time_step must be >= 0")

        if time_step >= len(self.steps):
            raise IndexError(
                f"time_step {time_step} is out of range for "
                f"{len(self.steps)} evidence steps"
            )

        return [step.statement for step in self.steps[: time_step + 1]]

    def statuses(
        self,
        proposition: z3.BoolRef,
    ) -> list[EpistemicStatus]:
        """
        Compute the formal epistemic status after every evidence step.
        """
        return [
            classify_proposition(
                self.statements_up_to(time_step),
                proposition,
            )
            for time_step in range(len(self.steps))
        ]