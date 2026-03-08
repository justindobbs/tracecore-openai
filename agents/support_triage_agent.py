from __future__ import annotations


class SupportTriageAgent:
    def __init__(self) -> None:
        self.reset({})

    def reset(self, task_spec: dict) -> None:
        self.task_spec = task_spec
        self.obs = None
        self.sent_issue = False
        self.captured_route = False

    def observe(self, observation: dict) -> None:
        self.obs = observation

    def act(self) -> dict:
        last_action = self.obs.get("last_action") if self.obs else None
        last_result = self.obs.get("last_action_result") if self.obs else None
        issue = "I was charged twice on my invoice and need a refund."

        if not self.sent_issue:
            self.sent_issue = True
            return {"type": "submit_support_issue", "args": {"message": issue}}

        if (
            last_action
            and last_action.get("type") == "submit_support_issue"
            and isinstance(last_result, dict)
            and last_result.get("ok")
            and not self.captured_route
        ):
            self.captured_route = True
            return {
                "type": "set_output",
                "args": {"key": "triage_route", "value": str(last_result.get("route", ""))},
            }

        return {"type": "wait", "args": {}}
