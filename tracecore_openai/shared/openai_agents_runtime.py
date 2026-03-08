from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tracecore_openai.config import get_settings

try:
    from agents import Agent, Runner, function_tool
except Exception:  # pragma: no cover
    Agent = None  # type: ignore[assignment]
    Runner = None  # type: ignore[assignment]

    def function_tool(func: Any) -> Any:
        return func


@dataclass
class AgentRunResult:
    app: str
    final_output: str
    agent_name: str
    meta: dict[str, Any]


def _fake_chat_response(message: str) -> AgentRunResult:
    lowered = message.lower()
    if "price" in lowered or "pricing" in lowered:
        output = "Our example stack is Python-first: FastAPI, uvicorn, and the OpenAI Agents SDK."
    elif "verify" in lowered or "tracecore" in lowered:
        output = "Use the native TraceCore CLI to verify and inspect the latest agent run, then compare revisions with diff and baseline commands."
    else:
        output = f"Chat assistant received: {message.strip()}"
    return AgentRunResult(app="chat_assistant", final_output=output, agent_name="Chat Assistant", meta={"mode": "fake"})


def _fake_triage_response(message: str) -> AgentRunResult:
    lowered = message.lower()
    route = "general"
    if any(term in lowered for term in ("refund", "billing", "charged", "invoice")):
        route = "billing"
    elif any(term in lowered for term in ("bug", "error", "stack", "crash", "broken")):
        route = "technical"
    elif any(term in lowered for term in ("password", "login", "sign in", "access")):
        route = "account"
    output = f"Route to {route} queue. Summary: {message.strip()}"
    return AgentRunResult(app="support_triage", final_output=output, agent_name="Support Triage", meta={"mode": "fake", "route": route})


@function_tool
def lookup_pricing_policy() -> str:
    """Return pricing guidance for the example application."""
    return "Pricing is usage-based and verified examples should document their expected run path."


@function_tool
def lookup_support_policy(issue_type: str) -> str:
    """Return routing guidance for the example support workflow."""
    mapping = {
        "billing": "Billing issues go to the billing queue.",
        "technical": "Technical issues go to the engineering support queue.",
        "account": "Account issues go to identity support.",
    }
    return mapping.get(issue_type, "General issues stay with the front-line support queue.")


async def run_chat_assistant(message: str) -> AgentRunResult:
    settings = get_settings()
    if settings.fake_runner:
        return _fake_chat_response(message)
    if Agent is None or Runner is None:
        raise RuntimeError("openai-agents is not available. Install dependencies before running the app.")
    agent = Agent(
        name="Chat Assistant",
        instructions=(
            "You are a concise product assistant for TraceCore OpenAI example apps. "
            "Answer clearly, mention local verification when relevant, and use tools if they help."
        ),
        model=settings.openai_model,
        tools=[lookup_pricing_policy],
    )
    result = await Runner.run(agent, message)
    return AgentRunResult(
        app="chat_assistant",
        final_output=str(result.final_output),
        agent_name=getattr(result.last_agent, "name", "Chat Assistant"),
        meta={"mode": "live", "model": settings.openai_model},
    )


async def run_support_triage(message: str) -> AgentRunResult:
    settings = get_settings()
    if settings.fake_runner:
        return _fake_triage_response(message)
    if Agent is None or Runner is None:
        raise RuntimeError("openai-agents is not available. Install dependencies before running the app.")

    billing_agent = Agent(
        name="Billing Specialist",
        handoff_description="Handles billing and refund issues.",
        instructions="Handle billing and refund questions. Be concrete and concise.",
        model=settings.openai_model,
        tools=[lookup_support_policy],
    )
    technical_agent = Agent(
        name="Technical Specialist",
        handoff_description="Handles app bugs, crashes, and technical troubleshooting.",
        instructions="Handle technical support issues and summarize next steps clearly.",
        model=settings.openai_model,
        tools=[lookup_support_policy],
    )
    account_agent = Agent(
        name="Account Specialist",
        handoff_description="Handles login, password, and account access issues.",
        instructions="Handle account access issues and explain the next step clearly.",
        model=settings.openai_model,
        tools=[lookup_support_policy],
    )
    triage_agent = Agent(
        name="Support Triage",
        instructions=(
            "Read the user's issue and hand off to the right specialist. "
            "Use billing for refunds/invoices, technical for bugs/errors, and account for access issues."
        ),
        model=settings.openai_model,
        handoffs=[billing_agent, technical_agent, account_agent],
    )
    result = await Runner.run(triage_agent, message)
    return AgentRunResult(
        app="support_triage",
        final_output=str(result.final_output),
        agent_name=getattr(result.last_agent, "name", "Support Triage"),
        meta={"mode": "live", "model": settings.openai_model},
    )
