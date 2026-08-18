from src.esi.action import Action
from src.esi.formal_state import EpistemicStatus
from src.esi.scenario_family import (
    ScenarioDomain,
    build_scenario_family,
)


def test_family_contains_expected_domains():
    family = build_scenario_family()

    domains = {
        scenario.domain
        for scenario in family
    }

    assert domains == {
        ScenarioDomain.AUTHORIZATION,
        ScenarioDomain.DOCUMENT_VALIDITY,
        ScenarioDomain.RESOURCE_AVAILABILITY,
        ScenarioDomain.TASK_PRECONDITION,
    }


def test_family_members_have_unique_ids():
    family = build_scenario_family()

    ids = [
        scenario.scenario_id
        for scenario in family
    ]

    assert len(ids) == len(set(ids))


def test_all_members_have_expected_initial_state():
    family = build_scenario_family()

    for scenario in family:
        assert (
            scenario.initial_status
            == EpistemicStatus.ENTAILED
        )

        assert scenario.initial_action == Action.PROCEED


def test_all_members_have_expected_revised_state():
    family = build_scenario_family()

    for scenario in family:
        assert (
            scenario.revised_status
            == EpistemicStatus.REFUTED
        )

        assert scenario.revised_action == Action.DO_NOT_PROCEED


def test_all_members_contain_natural_language_fields():
    family = build_scenario_family()

    for scenario in family:
        assert scenario.initial_text.strip()
        assert scenario.revision_text.strip()
        assert scenario.question_text.strip()