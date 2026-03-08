from __future__ import annotations

from pathlib import Path


def register() -> list[dict[str, object]]:
    root = Path(__file__).resolve().parent / "tasks"
    return [
        {
            "id": "chat_assistant_example",
            "suite": "openai_examples",
            "version": 1,
            "description": "Evaluate the chat assistant example against deterministic prompt/response expectations.",
            "deterministic": True,
            "path": str(root / "chat_assistant_example"),
        },
        {
            "id": "support_triage_example",
            "suite": "openai_examples",
            "version": 1,
            "description": "Evaluate the support triage example against deterministic routing expectations.",
            "deterministic": True,
            "path": str(root / "support_triage_example"),
        },
    ]
