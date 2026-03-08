# TraceCore OpenAI

[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?logo=python&logoColor=white)](pyproject.toml)
[![TraceCore Project](https://img.shields.io/badge/TraceCore-Main%20Repo-0d9488.svg)](https://github.com/justindobbs/Tracecore)

`tracecore-openai` is a Python-first examples repository for building OpenAI Agents SDK applications with the same local `FastAPI` + `uvicorn` workflow already used in TraceCore.

## What this repo includes

- A shared OpenAI Agents runtime adapter
- A `FastAPI` app exposing example agent-powered routes
- Two initial examples:
  - `chat_assistant`
  - `support_triage`
- A deterministic local verification flow for app behavior

## Recommended mental model

Use this repo in two modes:

- live mode to see a normal OpenAI Agents app in action
- deterministic mode to verify behavior repeatedly with the native `tracecore` workflow

The live app helps you evaluate whether the UX is useful. The deterministic mode helps you prove that the app still behaves the way you expect on fixed scenarios without spending API credits on every iteration.

## Start here if you are evaluating the repo

Read `docs/repo_scope.md` for a short explanation of what this repository demonstrates, what it does not demonstrate, and how it fits TraceCore's core mission as an agent evaluation tool.

## Why no Docker

Docker is optional. These examples call OpenAI-hosted models over HTTPS, so a normal Python process is enough for local development and verification.

## Quickstart

Everything needed to run this example is declared in `pyproject.toml`, so once you clone the repo you can install it with a single command.

```bash
git clone https://github.com/justindobbs/tracecore-openai.git
cd tracecore-openai
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
copy .env.example .env
```

Set `OPENAI_API_KEY` in your environment or `.env` loader of choice.

This install also brings in `tracecore>=1.1.2`, so the `tracecore` command should be available in the same environment.

## Recommended first run

Follow this sequence the first time you open the repo:

```bash
uvicorn tracecore_openai.main:app --reload
```

Open `http://127.0.0.1:8000` and try both example routes so you can see the app in normal hosted mode first.

Then switch to deterministic verification mode:

```bash
set TRACECORE_OPENAI_FAKE_RUNNER=1
tracecore run --agent agents/chat_assistant_agent.py --task chat_assistant_example@1 --seed 0
tracecore verify --latest
tracecore bundle seal --latest
```

That is the core TraceCore loop this repo is meant to teach.

## Run the app

```bash
uvicorn tracecore_openai.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Deterministic verification

The verification harness runs the app in a fake deterministic mode so you can validate behavior without spending API credits while staying inside the native TraceCore workflow.

This is intentional. The fake runner is not trying to replace the real OpenAI Agents SDK path. It gives you a repeatable evaluation mode so you can inspect, diff, and bundle behavior in a way that is stable enough for local regression checks.

```bash
set TRACECORE_OPENAI_FAKE_RUNNER=1
tracecore run --agent agents/chat_assistant_agent.py --task chat_assistant_example@1 --seed 0
tracecore verify --latest
```

Use the rest of the CLI to inspect and compare agent behavior as you iterate:

```bash
tracecore inspect --run <run_id>
tracecore diff <run_a> <run_b>
tracecore baseline --agent <agent> --task <task> --compare <run_a> <run_b>
tracecore runs list --limit 5
tracecore runs summary --limit 5
```

## Real OpenAI Agents mode

By default, the app uses the OpenAI Agents SDK. Use this mode when you want to interact with the app normally and validate that the product experience makes sense.

For deterministic verification and local regression checks, set:

```bash
set TRACECORE_OPENAI_FAKE_RUNNER=1
```

## API routes

- `GET /`
- `POST /api/chat-assistant`
- `POST /api/support-triage`
- `GET /healthz`

## Suggested workflow

```bash
# 1. Run the app in hosted mode
uvicorn tracecore_openai.main:app --reload

# 2. Switch to deterministic verification mode
set TRACECORE_OPENAI_FAKE_RUNNER=1

# 3. Run the native TraceCore loop
tracecore run --agent agents/chat_assistant_agent.py --task chat_assistant_example@1 --seed 0
tracecore verify --latest
tracecore inspect --run <run_id>
tracecore diff <run_a> <run_b>
tracecore baseline --agent agents/chat_assistant_agent.py --task chat_assistant_example@1 --compare <run_a> <run_b>
tracecore runs list --limit 5
tracecore runs summary --limit 5
tracecore bundle seal --latest

pytest
ruff check .
```

## How this maps to your own repo

This repo is meant to be copied conceptually, not literally. The reusable pattern is:

- keep your normal OpenAI Agents app surface
- add a deterministic verification mode for fixed scenarios
- expose TraceCore-compatible agent adapters for those scenarios
- register repo-local tasks so `tracecore` can run them naturally

If you want the broader explanation from the main TraceCore repo, see the OpenAI Agents onboarding guide there.
