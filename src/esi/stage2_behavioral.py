from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import z3

from .action import Action, choose_action
from .dependency import DependencyGraph, DependencyNode
from .evidence_events import EvidenceAction, EvidenceEvent
from .formal_state import EpistemicStatus, classify_proposition
from .retraction import RetractionResult, retract
from .revision import RevisableEvidenceState


class Stage2Condition(str, Enum):
    """Presentation conditions for the first controlled behavioral study."""

    SEQUENTIAL = "sequential"
    FLATTENED = "flattened"


@dataclass(frozen=True)
class Stage2DomainTemplate:
    """Surface-language template for one semantic dependency family."""

    name: str
    premise: str
    rules: tuple[str, ...]
    action_question: str
    retraction: str


@dataclass(frozen=True)
class Stage2Scenario:
    """One formally validated Stage-2 behavioral scenario."""

    scenario_id: str
    domain: str
    dependency_depth: int
    condition: Stage2Condition

    graph: DependencyGraph
    revoked_premise: str
    action_node: str
    retraction_result: RetractionResult

    initial_status: EpistemicStatus
    revised_status: EpistemicStatus
    initial_action: Action
    revised_action: Action

    messages: tuple[str, ...]

    @property
    def formal_oracle(self) -> dict[str, str]:
        return {
            "initial_status": self.initial_status.value,
            "revised_status": self.revised_status.value,
            "initial_action": self.initial_action.value,
            "revised_action": self.revised_action.value,
        }


def _templates() -> tuple[Stage2DomainTemplate, ...]:
    """
    Existing repository domains, rendered as explicit dependency chains.

    The four domains are the same domain families already present in
    scenario_family.py.
    """

    return (
        Stage2DomainTemplate(
            name="authorization",
            premise=(
                "The security credential required for the operation "
                "is currently valid."
            ),
            rules=(
                "A valid security credential establishes that the user "
                "is authorized to access the system.",
                "An authorized user is permitted to perform the "
                "requested operation.",
                "An operation that is permitted to be performed "
                "is cleared for execution.",
                "An operation cleared for execution is ready to proceed.",
            ),
            action_question="Should the operation proceed?",
            retraction=(
                "New information: the security credential has now been revoked."
            ),
        ),
        Stage2DomainTemplate(
            name="document_validity",
            premise=(
                "The document required for the operation is currently valid."
            ),
            rules=(
                "A valid document is acceptable for the operation.",
                "An operation with an acceptable document satisfies "
                "the document requirement.",
                "An operation that satisfies the document requirement "
                "is cleared under that requirement.",
                "An operation cleared under the document requirement "
                "is ready to proceed.",
            ),
            action_question="Should the operation proceed?",
            retraction=(
                "New information: the document has now been invalidated "
                "and is no longer valid for the operation."
            ),
        ),
        Stage2DomainTemplate(
            name="resource_availability",
            premise=(
                "The resource required for the task is currently available."
            ),
            rules=(
                "An available resource can be used by the task.",
                "A task that can use the resource has the required "
                "resource support.",
                "A task with the required resource support is ready "
                "for execution.",
                "A task ready for execution is cleared to proceed.",
            ),
            action_question="Should the task proceed?",
            retraction=(
                "New information: the resource is no longer available "
                "for the task."
            ),
        ),
        Stage2DomainTemplate(
            name="task_precondition",
            premise=(
                "The task currently satisfies the required preconditions "
                "for execution."
            ),
            rules=(
                "A task satisfying the required preconditions is eligible "
                "for execution.",
                "A task eligible for execution is approved for execution.",
                "A task approved for execution is cleared for execution.",
                "A task cleared for execution is ready to proceed.",
            ),
            action_question="Should the task proceed?",
            retraction=(
                "New information: the task no longer satisfies the "
                "required preconditions for execution."
            ),
        ),
    )


def available_stage2_domains() -> tuple[str, ...]:
    return tuple(template.name for template in _templates())


def _build_graph(
    depth: int,
) -> tuple[DependencyGraph, str, str]:
    """
    Build:

        premise -> c1 -> ... -> c_depth -> action

    where `depth` is the number of intermediate dependency nodes.
    """

    if not 1 <= depth <= 4:
        raise ValueError(
            "Stage-2 dependency depth must be between 1 and 4."
        )

    nodes: dict[str, DependencyNode] = {
        "premise": DependencyNode(name="premise")
    }

    for index in range(1, depth + 1):
        parent = (
            "premise"
            if index == 1
            else f"c{index - 1}"
        )

        nodes[f"c{index}"] = DependencyNode(
            name=f"c{index}",
            parents=(parent,),
        )

    nodes["action"] = DependencyNode(
        name="action",
        parents=(f"c{depth}",),
    )

    return (
        DependencyGraph(nodes=nodes),
        "premise",
        "action",
    )


def _action_rule(
    template: Stage2DomainTemplate,
    depth: int,
) -> str:
    """
    Render the final natural-language dependency edge:

        c_depth -> action

    This edge must always be explicit in the prompt.
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
        f"Unknown Stage-2 domain: {template.name}"
    )


def _action_rule(
    template: Stage2DomainTemplate,
    depth: int,
) -> str:
    """
    Render the final natural-language dependency edge:

        c_depth -> action

    This edge must always be explicit in the prompt.
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
        f"Unknown Stage-2 domain: {template.name}"
    )


def _action_rule(
    template: Stage2DomainTemplate,
    depth: int,
) -> str:
    """
    Render the final natural-language dependency edge:

        c_depth -> action

    This edge must always be explicit in the prompt.
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
        f"Unknown Stage-2 domain: {template.name}"
    )


def _action_rule(
    template: Stage2DomainTemplate,
    depth: int,
) -> str:
    """
    Render the final natural-language dependency edge:

        c_depth -> action

    This edge must always be explicit in the prompt.
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
        f"Unknown Stage-2 domain: {template.name}"
    )


def _render_messages(
    template: Stage2DomainTemplate,
    depth: int,
    condition: Stage2Condition,
) -> tuple[str, ...]:
    """
    Render the complete dependency chain:

        premise
        -> c1
        -> ...
        -> c_depth
        -> action

    Therefore the natural-language prompt contains exactly
    `depth + 1` implication rules.
    """

    chain_rules = list(
        template.rules[:depth]
    )

    chain_rules.append(
        _action_rule(
            template,
            depth,
        )
    )

    initial_block = "\n".join(
        [
            template.premise,
            *chain_rules,
        ]
    )

    question = (
        f"{template.action_question}\n\n"
        "Choose one:\n"
        "PROCEED\n"
        "DO_NOT_PROCEED\n"
        "VERIFY"
    )

    if condition == Stage2Condition.SEQUENTIAL:
        return (
            initial_block,
            template.retraction,
            question,
        )

    if condition == Stage2Condition.FLATTENED:
        return (
            initial_block + "\n" + template.retraction,
            question,
        )

    raise ValueError(
        f"Unsupported Stage-2 condition: {condition}"
    )


def build_stage2_scenario(
    *,
    domain: str,
    depth: int,
    condition: Stage2Condition,
    scenario_id: str,
) -> Stage2Scenario:
    """
    Build one Stage-2 scenario and validate both:

    1. proposition-level ENTAILED -> REFUTED transition
    2. dependency-graph retraction to the action node
    """

    template_by_name = {
        template.name: template
        for template in _templates()
    }

    if domain not in template_by_name:
        raise ValueError(
            f"Unknown Stage-2 domain: {domain}"
        )

    template = template_by_name[domain]

    # ------------------------------------------------------------
    # Formal epistemic-state validation
    # ------------------------------------------------------------

    proposition = z3.Bool(
        f"{scenario_id}_premise"
    )

    initial_event = EvidenceEvent(
        action=EvidenceAction.ADD,
        statement=proposition,
        name=f"{scenario_id}_initial",
    )

    revision_event = EvidenceEvent(
        action=EvidenceAction.REPLACE,
        statement=proposition,
        replacement=z3.Not(proposition),
        name=f"{scenario_id}_revision",
    )

    state = RevisableEvidenceState()

    state.apply(initial_event)

    initial_status = classify_proposition(
        state.evidence,
        proposition,
    )

    initial_action = choose_action(
        initial_status
    )

    state.apply(revision_event)

    revised_status = classify_proposition(
        state.evidence,
        proposition,
    )

    revised_action = choose_action(
        revised_status
    )

    if initial_status != EpistemicStatus.ENTAILED:
        raise RuntimeError(
            f"{scenario_id}: expected ENTAILED, "
            f"got {initial_status.value}"
        )

    if revised_status != EpistemicStatus.REFUTED:
        raise RuntimeError(
            f"{scenario_id}: expected REFUTED, "
            f"got {revised_status.value}"
        )

    if initial_action != Action.PROCEED:
        raise RuntimeError(
            f"{scenario_id}: expected PROCEED, "
            f"got {initial_action.value}"
        )

    if revised_action != Action.DO_NOT_PROCEED:
        raise RuntimeError(
            f"{scenario_id}: expected DO_NOT_PROCEED, "
            f"got {revised_action.value}"
        )

    # ------------------------------------------------------------
    # Formal dependency validation
    # ------------------------------------------------------------

    graph, revoked_premise, action_node = _build_graph(
        depth
    )

    retraction_result = retract(
        graph,
        revoked_premise,
    )

    expected_descendants = {
        f"c{i}"
        for i in range(1, depth + 1)
    } | {action_node}

    if (
        retraction_result.invalidated_descendants
        != frozenset(expected_descendants)
    ):
        raise RuntimeError(
            f"{scenario_id}: dependency retraction invariant failed."
        )

    # ------------------------------------------------------------
    # Natural-language experimental condition
    # ------------------------------------------------------------

    messages = _render_messages(
        template=template,
        depth=depth,
        condition=condition,
    )

    return Stage2Scenario(
        scenario_id=scenario_id,
        domain=domain,
        dependency_depth=depth,
        condition=condition,
        graph=graph,
        revoked_premise=revoked_premise,
        action_node=action_node,
        retraction_result=retraction_result,
        initial_status=initial_status,
        revised_status=revised_status,
        initial_action=initial_action,
        revised_action=revised_action,
        messages=messages,
    )


def build_stage2_pilot_scenarios(
    *,
    depths: tuple[int, ...] = (1, 2, 3, 4),
    conditions: tuple[Stage2Condition, ...] = (
        Stage2Condition.SEQUENTIAL,
        Stage2Condition.FLATTENED,
    ),
) -> list[Stage2Scenario]:

    scenarios: list[Stage2Scenario] = []

    for domain in available_stage2_domains():
        for depth in depths:
            for condition in conditions:

                scenario_id = (
                    f"stage2_"
                    f"{domain}_"
                    f"d{depth}_"
                    f"{condition.value}"
                )

                scenarios.append(
                    build_stage2_scenario(
                        domain=domain,
                        depth=depth,
                        condition=condition,
                        scenario_id=scenario_id,
                    )
                )
                
    return scenarios