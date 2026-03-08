from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tracecore_openai.apps.chat_assistant import ChatRequest, handle_chat
from tracecore_openai.apps.support_triage import TriageRequest, handle_triage

SCENARIOS_DIR = Path(__file__).resolve().parent / "evals" / "scenarios"
OUTPUT_DIR = Path.cwd() / "deliverables" / "verification"


@dataclass
class ScenarioResult:
    app: str
    name: str
    passed: bool
    output: str
    expected_substring: str
    agent_name: str
    meta: dict[str, Any]


def _load_scenarios(name: str) -> list[dict[str, Any]]:
    path = SCENARIOS_DIR / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


async def _run_chat_scenario(payload: dict[str, Any]) -> ScenarioResult:
    response = await handle_chat(ChatRequest(message=payload["input"]))
    expected = payload["expected_substring"]
    return ScenarioResult(
        app="chat_assistant",
        name=payload["name"],
        passed=expected.lower() in response.output.lower(),
        output=response.output,
        expected_substring=expected,
        agent_name=response.agent_name,
        meta=response.meta,
    )


async def _run_triage_scenario(payload: dict[str, Any]) -> ScenarioResult:
    response = await handle_triage(TriageRequest(message=payload["input"]))
    expected = payload["expected_substring"]
    return ScenarioResult(
        app="support_triage",
        name=payload["name"],
        passed=expected.lower() in response.output.lower(),
        output=response.output,
        expected_substring=expected,
        agent_name=response.agent_name,
        meta=response.meta,
    )


async def run_verification() -> dict[str, Any]:
    previous = os.environ.get("TRACECORE_OPENAI_FAKE_RUNNER")
    os.environ["TRACECORE_OPENAI_FAKE_RUNNER"] = "1"
    results: list[ScenarioResult] = []
    try:
        for scenario in _load_scenarios("chat_assistant"):
            results.append(await _run_chat_scenario(scenario))
        for scenario in _load_scenarios("support_triage"):
            results.append(await _run_triage_scenario(scenario))
    finally:
        if previous is None:
            os.environ.pop("TRACECORE_OPENAI_FAKE_RUNNER", None)
        else:
            os.environ["TRACECORE_OPENAI_FAKE_RUNNER"] = previous
    passed = all(item.passed for item in results)
    payload = {
        "ok": passed,
        "scenario_count": len(results),
        "passed_count": sum(1 for item in results if item.passed),
        "results": [item.__dict__ for item in results],
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "latest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    payload = asyncio.run(run_verification())
    print(json.dumps(payload, indent=2))
    if not payload["ok"]:
        raise SystemExit(1)
