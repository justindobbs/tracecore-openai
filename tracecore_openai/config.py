from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    fake_runner: bool
    host: str
    port: int


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5-nano"),
        fake_runner=os.getenv("TRACECORE_OPENAI_FAKE_RUNNER", "0").lower() in {"1", "true", "yes", "on"},
        host=os.getenv("TRACECORE_OPENAI_HOST", "127.0.0.1"),
        port=int(os.getenv("TRACECORE_OPENAI_PORT", "8000")),
    )


settings = get_settings()
