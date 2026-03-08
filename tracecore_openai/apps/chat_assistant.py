from __future__ import annotations

from pydantic import BaseModel

from tracecore_openai.shared.openai_agents_runtime import AgentRunResult, run_chat_assistant


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    app: str
    output: str
    agent_name: str
    meta: dict


async def handle_chat(request: ChatRequest) -> ChatResponse:
    result: AgentRunResult = await run_chat_assistant(request.message)
    return ChatResponse(
        app=result.app,
        output=result.final_output,
        agent_name=result.agent_name,
        meta=result.meta,
    )
