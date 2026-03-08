# TraceCore OpenAI

[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?logo=python&logoColor=white)](pyproject.toml)
[![TraceCore Project](https://img.shields.io/badge/TraceCore-Main%20Repo-0d9488.svg)](https://github.com/justindobbs/Tracecore)

`tracecore-openai` is a Python-first examples repository for building OpenAI Agents SDK applications with the same local `FastAPI` + `uvicorn` workflow already used in TraceCore.

Main TraceCore repo: https://github.com/justindobbs/Tracecore

## What this repo includes

- A shared OpenAI Agents runtime adapter
- A `FastAPI` app exposing example agent-powered routes
- Two initial examples:
  - `chat_assistant`
  - `support_triage`
- A deterministic local verification flow for app behavior

## Start here if you are evaluating the repo

Read `docs/repo_scope.md` for a short explanation of what this repository demonstrates, what it does not demonstrate, and how it fits TraceCore's core mission as an agent evaluation tool.

## Why no Docker

Docker is optional. These examples call OpenAI-hosted models over HTTPS, so a normal Python process is enough for local development and verification.

## Quickstart

### Option A: install the published TraceCore CLI

Install the main `tracecore` CLI first if you want to use bundle and verification-adjacent commands from the broader TraceCore toolchain.

```bash
uv tool install "tracecore[openai_agents]"
```

Or with `pip` in your virtual environment:

```bash
pip install "tracecore[openai_agents]"
```

### Option B: clone and install TraceCore from source

If you want to work on the main TraceCore repo locally, clone it and install it in editable mode:

```bash
git clone https://github.com/justindobbs/Tracecore.git
python -m venv .venv-tracecore
.venv-tracecore\Scripts\activate
pip install -e .[dev,openai_agents]
```

### Install and run this `tracecore-openai` example repo

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
copy .env.example .env
```

Set `OPENAI_API_KEY` in your environment or `.env` loader of choice.

If you installed `tracecore` in a different environment, make sure the `tracecore` command is available in your shell before running bundle commands from this repo.

## Run the app

```bash
uvicorn tracecore_openai.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Deterministic verification

The verification harness runs the app in a fake deterministic mode so you can validate behavior without spending API credits.

`tracecore-openai-verify` is a helper command defined by this example repository. In the main TraceCore CLI, the native verification workflow uses `tracecore verify`.

```bash
tracecore-openai-verify
```

This writes a JSON report to `deliverables/verification/latest.json`.

## Real OpenAI Agents mode

By default, the app uses the OpenAI Agents SDK. For deterministic tests, set:

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
uvicorn tracecore_openai.main:app --reload

# repo-specific example helper command
tracecore-openai-verify

# native TraceCore CLI workflow
# tracecore verify ...

pytest
ruff check .
```
