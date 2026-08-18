from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .action import Action
from .formal_state import EpistemicStatus
from .stage2_behavioral import (
    Stage2DomainTemplate,
    _build_graph,
    _templates,
)


class Stage3Condition(str, Enum):
    """
    Behavioral presentation conditions.

    EARLY_RETRACTION:
        evidence -> retraction -> final action

    LATE_RETRACTION:
        evidence -> prior downstream derivation
        -> retraction -> final action

    LATE_RETRACTION_REDERIVE:
        evidence -> prior downstream derivation
        -> retraction -> explicit fresh reassessment -> final action

    The third condition is a rescue/control condition. It is deliberately
    explicit about reassessment and should not be treated as a neutral
    condition.
    """

    EARLY_RETRACTION = "early_retraction"
    LATE_RETRACTION = "late_retraction"
    LATE_RETRACTION_REDERIVE = "late_retraction_rederive"


@dataclass(frozen=True)
class Stage3Scenario:
    scenario_id: str
    domain: str
    dependency_depth: int
    condition: Stage3Condition

    messages: tuple[str, ...]

    formal_oracle: dict[str, str]

    revoked_premise: str
    action_node: str
    dependency_nodes: tuple[str, ...]


def _action_question(template: Stage2DomainTemplate) -> str:
    return (
        f"{template.action_question}\n\n"
        "Choose one:\n"
        "PROCEED\n"
        "DO_NOT_PROCEED\n"
        "VERIFY"
    )


def _pre_retraction_derivation(
    template: Stage2DomainTemplate,
    depth: int,
) -> str:
    """
    Ask the model to construct and use the downstream reasoning before
    the premise is retracted.

    We deliberately do NOT say:
        update your belief
        maintain a state
        remember this
        revise later

    The request is purely to prepare the action basis under the current
    information.
    """

    rules = template.rules[:depth]

    chain = "\n".join(
        rules
    )

    return (
        "Based only on the information currently available, "
        "prepare the operation for execution. "
        "State the reasoning basis for the operation and the action "
        "you would take if the current information remained unchanged.\n\n"
        f"{chain}"
    )


def _build_messages(
    template: Stage2DomainTemplate,
    depth: int,
    condition: Stage3Condition,
) -> tuple[str, ...]:

    initial_information = "\n".join(
        [
            template.premise,
            *template.rules[:depth],
            _stage3_action_rule(template, depth),
        ]
    )

    retraction = template.retraction
    final_question = _action_question(template)

    if condition == Stage3Condition.EARLY_RETRACTION:
        return (
            initial_information,
            retraction,
            final_question,
        )

    if condition == Stage3Condition.LATE_RETRACTION:
        return (
            initial_information,
            _pre_retraction_derivation(
                template,
                depth,
            ),
            retraction,
            final_question,
        )

    if condition == Stage3Condition.LATE_RETRACTION_REDERIVE:
        return (
            initial_information,
            _pre_retraction_derivation(
                template,
                depth,
            ),
            retraction,
            (
                "Re-evaluate the current information and the "
                "authorization basis before deciding."
            ),
            final_question,
        )

    raise ValueError(
        f"Unsupported Stage-3 condition: {condition}"
    )


def _stage3_action_rule(
    template: Stage2DomainTemplate,
    depth: int,
) -> str:
    """
    Explicit final edge from c_depth to the action.

    This mirrors the Stage-2 natural-language construction.
    """

    if template.name == "authorization":
        predicates = (
            "the user is authorized to access the system",
            "the user is permitted to perform the requested operation",
            "the operation is cleared for execution",
            "the operation is ready to proceed",
        )

        return (
            f"If {predicates[depth - 1]}, "
            "the operation should proceed."
        )

    if template.name == "document_validity":
        predicates = (
            "the document is acceptable for the operation",
            "the operation satisfies the document requirement",
            "the operation is cleared under the document requirement",
            "the operation is ready to proceed",
        )

        return (
            f"If {predicates[depth - 1]}, "
            "the operation should proceed."
        )

    if template.name == "resource_availability":
        predicates = (
            "the resource can be used by the task",
            "the task has the required resource support",
            "the task is ready for execution",
            "the task is cleared to proceed",
        )

        return (
            f"If {predicates[depth - 1]}, "
            "the task should proceed."
        )

    if template.name == "task_precondition":
        predicates = (
            "the task is eligible for execution",
            "the task is approved for execution",
            "the task is cleared for execution",
            "the task is ready to proceed",
        )

        return (
            f"If {predicates[depth - 1]}, "
            "the task should proceed."
        )

    raise ValueError(
        f"Unknown Stage-3 domain: {template.name}"
    )


def build_stage3_scenario(
    *,
    domain: str,
    depth: int,
    condition: Stage3Condition,
    scenario_id: str,
) -> Stage3Scenario:

    templates = {
        template.name: template
        for template in _templates()
    }

    if domain not in templates:
        raise ValueError(
            f"Unknown Stage-3 domain: {domain}"
        )

    if depth not in (1, 2, 3, 4):
        raise ValueError(
            "Stage-3 depth must be 1, 2, 3, or 4."
        )

    template = templates[domain]

    graph, revoked_premise, action_node = _build_graph(
        depth
    )

    expected_descendants = {
        f"c{i}"
        for i in range(1, depth + 1)
    } | {action_node}

    # The graph's node structure is the canonical dependency object.
    actual_nodes = set(graph.nodes)

    if not expected_descendants.issubset(actual_nodes):
        raise RuntimeError(
            f"{scenario_id}: dependency graph does not contain "
            f"the requested depth."
        )

    messages = _build_messages(
        template=template,
        depth=depth,
        condition=condition,
    )

    return Stage3Scenario(
        scenario_id=scenario_id,
        domain=domain,
        dependency_depth=depth,
        condition=condition,
        messages=messages,
        formal_oracle={
            "initial_status": EpistemicStatus.ENTAILED.value,
            "revised_status": EpistemicStatus.REFUTED.value,
            "initial_action": Action.PROCEED.value,
            "revised_action": Action.DO_NOT_PROCEED.value,
        },
        revoked_premise=revoked_premise,
        action_node=action_node,
        dependency_nodes=tuple(
            f"c{i}"
            for i in range(1, depth + 1)
        ),
    )


def build_stage3_pilot_scenarios(
    *,
    depths: tuple[int, ...] = (2, 4),
) -> list[Stage3Scenario]:

    scenarios: list[Stage3Scenario] = []

    for template in _templates():
        for depth in depths:
            for condition in Stage3Condition:

                scenario_id = (
                    f"stage3_"
                    f"{template.name}_"
                    f"d{depth}_"
                    f"{condition.value}"
                )

                scenarios.append(
                    build_stage3_scenario(
                        domain=template.name,
                        depth=depth,
                        condition=condition,
                        scenario_id=scenario_id,
                    )
                )

    return scenarios