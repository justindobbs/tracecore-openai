# What This Repo Shows

`tracecore-openai` is a small, intentionally opinionated example repository.

Its purpose is not to show every part of TraceCore. Its purpose is to give a normal user a concrete, runnable example of the TraceCore evaluation loop:

1. Run an agent-powered application.
2. Confirm the agent appears useful in a real interface.
3. Verify the agent against deterministic expectations.
4. Use the verification result as evidence of reliability.
5. Move toward bundle verification and certification once the behavior is stable.

## What this repo demonstrates

This repository demonstrates several things clearly.

### 1. Agent applications can be evaluated, not just demoed

The two included examples, `chat_assistant` and `support_triage`, are intentionally simple enough to understand quickly.

They let a user see two distinct truths:

- an agent can produce a plausible response in a UI
- a plausible response is not the same thing as a reliable system

That distinction is central to TraceCore.

### 2. Deterministic verification is part of the development loop

The `tracecore-openai-verify` command runs the included scenarios in deterministic mode and writes a structured report to `deliverables/verification/latest.json`.

This shows that evaluation can be part of normal local development, not only a late-stage release activity.

### 3. Verification produces evidence, not vibes

The verification flow checks whether known scenarios produce the expected outputs or routing behavior.

A passing run gives the user evidence that the current agent behavior satisfies the defined expectations.
A failing run gives the user a concrete starting point for remediation.

### 4. The same agent surface can support both live use and repeatable testing

This repo shows a practical pattern:

- real app routes for interactive use
- deterministic mode for repeatable verification
- a simple report artifact for inspection and follow-up

This is useful because many teams can already build a demo, but they still need a disciplined way to evaluate whether that demo is dependable.

### 5. Evaluation can lead into certification workflows

Once verification is passing, the workflow points toward bundle operations such as:

- `tracecore bundle seal --latest`
- `tracecore bundle verify <bundle_dir>`
- `tracecore bundle sign <bundle_dir>`

This shows the bridge from local evaluation to release evidence.

## What this repo does not demonstrate

This repository is intentionally narrow. It does **not** try to represent the full TraceCore platform.

### 1. It is not a complete benchmark suite

This repo includes only a small number of example scenarios.

It does not show the full breadth of TraceCore task coverage, large scenario portfolios, or broad cross-domain benchmarking.

### 2. It is not a production hardening guide

Although the repo includes tests, linting, verification, and bundle-oriented next steps, it is still an example project.

It does not, by itself, prove:

- full operational readiness
- organization-wide governance
- production observability maturity
- security review completeness
- broad regression coverage across many agent types

### 3. It does not show every TraceCore capability

TraceCore as a broader system includes concerns such as richer artifacts, larger task sets, bundle workflows, and other evaluation surfaces.

This repo is only one small entry point into that vision.

### 4. It does not prove general intelligence or universal agent quality

A passing result in this repository means the included agent examples met the expectations defined here.

It does **not** mean the agent is universally correct, safe in every environment, or ready for every deployment context.

TraceCore is about bounded, explicit evaluation claims.

### 5. It does not replace human judgment

TraceCore helps users measure whether an agent meets declared expectations.
It does not remove the need to choose good scenarios, define meaningful acceptance criteria, and decide whether the measured behavior is sufficient for a given use case.

## How this fits the core TraceCore mission

The core mission of TraceCore is to help people evaluate agents in a way that is structured, repeatable, and evidence-based.

This repository supports that mission by making the core idea easy to grasp:

- first, you can run the agent and see that it works
- then, you can verify whether it behaves reliably on known scenarios
- then, you can inspect the evidence and improve the agent if needed
- finally, you can carry that evidence forward into bundle-oriented trust workflows

In other words, this repo is a teaching example for the TraceCore mindset.

It helps users understand that the goal is not merely to build agents that look impressive in a single interaction. The goal is to evaluate whether they meet explicit standards in repeatable conditions.

## Who this repo is for

This repo is especially useful for:

- developers trying TraceCore for the first time
- teams evaluating whether agent verification fits their workflow
- users who want a small, understandable example before adopting broader TraceCore tooling
- people who need a practical explanation of the difference between a live demo and an evaluated agent

## Recommended mental model

A good way to think about `tracecore-openai` is:

- **not** the whole TraceCore system
- **not** the final word on agent quality
- **but** a concrete example of how TraceCore turns agent behavior into evaluation evidence

If you understand that loop after using this repo, then the repo has done its job.
