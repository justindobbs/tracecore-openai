from __future__ import annotations

from pydantic import BaseModel

from tracecore_openai.shared.openai_agents_runtime import AgentRunResult, run_support_triage


class TriageRequest(BaseModel):
    message: str


class TriageResponse(BaseModel):
    app: str
    output: str
    agent_name: str
    meta: dict


async def handle_triage(request: TriageRequest) -> TriageResponse:
    result: AgentRunResult = await run_support_triage(request.message)
    return TriageResponse(
        app=result.app,
        output=result.final_output,
        agent_name=result.agent_name,
        meta=result.meta,
    )
