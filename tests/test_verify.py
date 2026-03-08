from __future__ import annotations

import asyncio
import json
from pathlib import Path

from tracecore_openai.verify import main, run_verification


def test_run_verification_passes_and_writes_report() -> None:
    payload = asyncio.run(run_verification())
    assert payload["ok"] is True
    assert payload["scenario_count"] == 5
    report = Path.cwd() / "deliverables" / "verification" / "latest.json"
    assert report.exists()
    loaded = json.loads(report.read_text(encoding="utf-8"))
    assert loaded["passed_count"] == 5


def test_verify_main_prints_summary_and_bundle_next_steps(capsys) -> None:
    main()
    captured = capsys.readouterr().out

    assert "TraceCore OpenAI verification report" in captured
    assert "Result: PASSED" in captured
    assert "Scenarios: 5/5 passed" in captured
    assert "tracecore bundle seal --latest" in captured
    assert "tracecore bundle verify <bundle_dir>" in captured
    assert "tracecore bundle sign <bundle_dir>" in captured
