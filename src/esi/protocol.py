from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MessageRole(str, Enum):
    EVIDENCE = "evidence"
    UPDATE = "update"
    QUESTION = "question"


@dataclass(frozen=True)
class ScenarioMessage:
    role: MessageRole
    content: str


@dataclass(frozen=True)
class DecisionScenario:
    """
    A sequential decision scenario.

    The model receives the messages in order:
        initial evidence -> new evidence -> question

    The formal ground-truth states are stored separately.
    """

    initial_message: ScenarioMessage
    update_message: ScenarioMessage
    question_message: ScenarioMessage

    initial_status: str
    revised_status: str

    initial_action: str
    revised_action: str

    scenario_id: str