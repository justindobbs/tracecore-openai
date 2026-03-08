from __future__ import annotations


def validate(env) -> dict:
    provided = env.get_agent_output("chat_response")
    if provided and "native tracecore cli" in str(provided).lower():
        return {"ok": True, "message": "chat assistant returned TraceCore verification guidance"}
    return {"ok": False, "message": "chat assistant response did not include expected verification guidance"}
