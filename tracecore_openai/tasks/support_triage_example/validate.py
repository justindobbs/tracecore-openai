from __future__ import annotations


def validate(env) -> dict:
    provided = env.get_agent_output("triage_route")
    if provided and str(provided).lower() == "billing":
        return {"ok": True, "message": "support triage routed the issue correctly"}
    return {"ok": False, "message": "support triage route did not match the expected queue"}
