from src.esi.prompting import (
    PromptCondition,
    build_revision_prompt,
)
from src.esi.scenario import build_authorization_revocation_scenario


def test_neutral_prompt_does_not_explicitly_request_update():
    scenario = build_authorization_revocation_scenario()

    prompt = build_revision_prompt(
        scenario,
        PromptCondition.NEUTRAL,
    )

    assert "Update your decision using the new evidence." not in prompt


def test_explicit_update_prompt_contains_update_instruction():
    scenario = build_authorization_revocation_scenario()

    prompt = build_revision_prompt(
        scenario,
        PromptCondition.EXPLICIT_UPDATE,
    )

    assert "Update your decision using the new evidence." in prompt