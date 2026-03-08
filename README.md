# TraceCore OpenAI

`tracecore-openai` is a Python-first examples repository for building OpenAI Agents SDK applications with the same local `FastAPI` + `uvicorn` workflow already used in TraceCore.

## What this repo includes

- A shared OpenAI Agents runtime adapter
- A `FastAPI` app exposing example agent-powered routes
- Two initial examples:
  - `chat_assistant`
  - `support_triage`
- A deterministic local verification flow for app behavior

## Why no Docker

Docker is optional. These examples call OpenAI-hosted models over HTTPS, so a normal Python process is enough for local development and verification.

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
copy .env.example .env
```

Set `OPENAI_API_KEY` in your environment or `.env` loader of choice.

## Run the app

```bash
uvicorn tracecore_openai.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Deterministic verification

The verification harness runs the app in a fake deterministic mode so you can validate behavior without spending API credits.

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
tracecore-openai-verify
pytest
ruff check .
```
