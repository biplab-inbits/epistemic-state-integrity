from src.esi.model_prompts import build_retraction_prompt


def test_prompt_contains_initial_and_new_information():
    prompt = build_retraction_prompt()

    assert "Credential C is valid." in prompt
    assert "Credential C has been revoked." in prompt


def test_prompt_contains_decision_options():
    prompt = build_retraction_prompt()

    assert "PROCEED" in prompt
    assert "DO_NOT_PROCEED" in prompt
    assert "VERIFY" in prompt


def test_prompt_does_not_explicitly_instruct_revision():
    prompt = build_retraction_prompt()

    forbidden = [
        "update your belief",
        "update your state",
        "propagate",
        "reconsider the previous conclusion",
    ]

    lowered = prompt.lower()

    for phrase in forbidden:
        assert phrase not in lowered