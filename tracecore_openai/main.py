from __future__ import annotations

from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from tracecore_openai.apps.chat_assistant import ChatRequest, handle_chat
from tracecore_openai.apps.support_triage import TriageRequest, handle_triage
from tracecore_openai.config import get_settings

TEMPLATES_DIR = Path(__file__).with_suffix("").with_name("templates")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app = FastAPI(title="TraceCore OpenAI", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat-assistant")
async def chat_assistant(request: Request, message: str = Form("")) -> JSONResponse:
    if request.headers.get("content-type", "").startswith("application/json"):
        body = await request.json()
        message = body.get("message", "")
    response = await handle_chat(ChatRequest(message=message))
    return JSONResponse(response.model_dump())


@app.post("/api/support-triage")
async def support_triage(request: Request, message: str = Form("")) -> JSONResponse:
    if request.headers.get("content-type", "").startswith("application/json"):
        body = await request.json()
        message = body.get("message", "")
    response = await handle_triage(TriageRequest(message=message))
    return JSONResponse(response.model_dump())


def cli() -> None:
    settings = get_settings()
    uvicorn.run("tracecore_openai.main:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    cli()
