from __future__ import annotations

import asyncio
import os

from tracecore_openai.shared.openai_agents_runtime import run_support_triage

_ENV = None


def set_env(env):
    global _ENV
    _ENV = env


def submit_support_issue(message: str) -> dict:
    previous = os.environ.get("TRACECORE_OPENAI_FAKE_RUNNER")
    os.environ["TRACECORE_OPENAI_FAKE_RUNNER"] = "1"
    try:
        result = asyncio.run(run_support_triage(message))
    finally:
        if previous is None:
            os.environ.pop("TRACECORE_OPENAI_FAKE_RUNNER", None)
        else:
            os.environ["TRACECORE_OPENAI_FAKE_RUNNER"] = previous
    return {
        "ok": True,
        "response": result.final_output,
        "agent_name": result.agent_name,
        "route": result.meta.get("route"),
        "meta": result.meta,
    }


def set_output(key: str, value: str) -> dict:
    _ENV.set_agent_output(key, value)
    return {"ok": True}
