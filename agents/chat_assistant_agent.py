from __future__ import annotations


class ChatAssistantAgent:
    def __init__(self) -> None:
        self.reset({})

    def reset(self, task_spec: dict) -> None:
        self.task_spec = task_spec
        self.obs = None
        self.sent_prompt = False
        self.captured_response = False

    def observe(self, observation: dict) -> None:
        self.obs = observation

    def act(self) -> dict:
        last_action = self.obs.get("last_action") if self.obs else None
        last_result = self.obs.get("last_action_result") if self.obs else None
        hidden_prompt = "How do I verify an app with TraceCore?"

        if not self.sent_prompt:
            self.sent_prompt = True
            return {"type": "ask_chat_assistant", "args": {"message": hidden_prompt}}

        if (
            last_action
            and last_action.get("type") == "ask_chat_assistant"
            and isinstance(last_result, dict)
            and last_result.get("ok")
            and not self.captured_response
        ):
            self.captured_response = True
            return {
                "type": "set_output",
                "args": {"key": "chat_response", "value": str(last_result.get("response", ""))},
            }

        return {"type": "wait", "args": {}}
