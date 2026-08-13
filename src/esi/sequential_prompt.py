from __future__ import annotations

from .protocol import DecisionScenario


def render_sequential_messages(
    scenario: DecisionScenario,
) -> list[str]:
    """
    Return the messages in temporal order.

    The model should receive these sequentially rather than as one
    flattened static description.
    """

    return [
        scenario.initial_message.content,
        scenario.update_message.content,
        scenario.question_message.content,
    ]