from __future__ import annotations

import asyncio
import json
from pathlib import Path

from tracecore_openai.verify import run_verification


def test_run_verification_passes_and_writes_report() -> None:
    payload = asyncio.run(run_verification())
    assert payload["ok"] is True
    assert payload["scenario_count"] == 5
    report = Path.cwd() / "deliverables" / "verification" / "latest.json"
    assert report.exists()
    loaded = json.loads(report.read_text(encoding="utf-8"))
    assert loaded["passed_count"] == 5
