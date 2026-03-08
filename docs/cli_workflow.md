# TraceCore CLI workflow for tracecore-openai

This guide shows how to use the existing `tracecore-openai` example repo as a real-world TraceCore CLI workflow rather than only as a UI demo.

## Mental model

Use the app UI to see the agent behave.
Use the TraceCore CLI to decide whether that behavior is reliable.

That means the normal loop looks like this:

1. Run the app.
2. Try the agent in the UI.
3. Verify the latest run.
4. Inspect the artifact.
5. Diff revisions after changes.
6. Review run history and summaries.
7. Seal a bundle when the behavior is stable.

## Start the app

```bash
uvicorn tracecore_openai.main:app --reload
```

Then open `http://127.0.0.1:8000` and interact with the Chat Assistant or Support Triage example.

## Verify the latest run

```bash
tracecore verify --latest
```

This is the TraceCore equivalent of asking, “does the current agent behavior meet the expected standard?”

## Inspect a stored run

```bash
tracecore inspect --run <run_id>
```

Use this when you want to look more closely at what happened in a specific run artifact.

## Diff two revisions

```bash
tracecore diff <run_a> <run_b>
```

Use this after changing prompts, tools, routing logic, or instructions.

This is one of the strongest everyday TraceCore workflows: make an edit, rerun, and compare what changed.

## Compare baselines

```bash
tracecore baseline --agent <agent> --task <task> --compare <run_a> <run_b>
```

Use baseline when you want to compare reliability across revisions or export a stronger point of reference.

## Review recent history

```bash
tracecore runs list --limit 5
tracecore runs summary --limit 5
```

Use these commands to understand what has been happening recently without manually tracking run IDs.

## Move toward release evidence

Once the behavior is stable:

```bash
tracecore bundle seal --latest
tracecore bundle verify <bundle_dir>
tracecore bundle sign <bundle_dir>
```

This is how the example transitions from “the agent seems to work” to “we have evidence attached to a release artifact.”

## Recommended everyday loop

```bash
uvicorn tracecore_openai.main:app --reload
tracecore verify --latest
tracecore inspect --run <run_id>
tracecore diff <run_a> <run_b>
tracecore runs summary --limit 5
tracecore bundle seal --latest
```

That is the real value proposition this repo is meant to teach: TraceCore gives you a repeatable CLI loop for evaluating agents the way developers already use `pytest` to evaluate code changes.
