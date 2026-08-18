from __future__ import annotations

from dataclasses import dataclass

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "Qwen/Qwen3-4B-Thinking-2507-FP8"


@dataclass(frozen=True)
class GenerationResult:
    model_name: str
    prompt: str
    raw_output: str


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
    )

    model.eval()

    return tokenizer, model


def generate_response(
    tokenizer,
    model,
    prompt: str,
    max_new_tokens: int = 2048,
) -> GenerationResult:
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True,
    )

    inputs = tokenizer(
        [text],
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.6,
            top_p=0.95,
            top_k=20,
            min_p=0.0,
        )

    generated_ids = outputs[0][inputs.input_ids.shape[1]:]

    raw_output = tokenizer.decode(
        generated_ids,
        skip_special_tokens=True,
    )

    return GenerationResult(
        model_name=MODEL_NAME,
        prompt=prompt,
        raw_output=raw_output,
    )