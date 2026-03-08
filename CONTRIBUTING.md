# Contributing

## Prerequisites
- Python 3.12+
- `pip install -e .[dev]`

## Workflow
1. Create a branch.
2. Run `ruff check .`.
3. Run `pytest`.
4. Run the native TraceCore verification loop (`tracecore verify`, `tracecore inspect`, `tracecore runs summary`) for the latest relevant run.
5. Open a PR referencing the relevant TraceCore plan/issue.

## Notes
- Do not commit `.env` or API keys.
- Deterministic verification should pass before pushing.
- Keep example agents deterministic-friendly for TraceCore runs.
