# CCS-015 — Comparative Baseline: Composition vs Conventional Automation

## Objective

Measure what the previously confirmed CCS-012 Release Steward composition actually buys or costs versus a conventional implementation for the same deterministic useful task.

This experiment is explicitly allowed to conclude that the conventional baseline is simpler or better.

## Source task

Reproduce the FRONTIER release produced by the CCS-012 / legacy ECS-012 Release Steward from the same historical capability-map input and the same human policy choice.

Historical source commit: `72c9af58af075baa9e73311b208d7263a8890255`
Historical source path: `bci/emergent-capability-surface/map.json`
Human policy: `FRONTIER`
Reference release: `bci/runs/ecs-012-20260916-APP1/release.json`

## Lane A — Existing compositional implementation

Observed components:
- `collect.py`
- `render.py`
- `verify.py`
- `.github/workflows/ecs-012-applicationless.yml`
- durable `state.json`
- human `steer.json`

Observed required semantic stages:
1. analyze and persist;
2. pause for human policy;
3. resume and render;
4. independently verify;
5. persist final state.

Observed workflow runs:
- Stage 1 success: `35138405247`
- First Stage 2 attempt failed because the ChatGPT-written steer adapter used the wrong JSON field: `35138607616`
- Corrected Stage 2 success: `35138660013`

## Lane B — Conventional baseline

Implement the same deterministic transformation as a conventional one-shot automation:
- one Python program `baseline.py`;
- one GitHub Actions workflow;
- policy supplied as a normal input constant `FRONTIER`;
- no ChatGPT reasoning required at runtime;
- no durable pause/resume state machine;
- no custom agent runtime.

The workflow must reconstruct the exact historical source map with `git show`, run `baseline.py`, and commit its generated outputs.

## Independent comparison

A separate lab measurement program `measure.py` must:
1. compare the conventional `baseline_release.json` byte-semantic JSON object with the reference CCS-012 `release.json`;
2. count nonblank/noncomment implementation LOC for both approaches;
3. count implementation files for both approaches;
4. record required policy-decision events;
5. record required successful workflow stages and observed workflow attempts;
6. record whether each approach supports an explicit durable human-interrupt point;
7. produce `comparison.json` and `CONCLUSION.md`.

## Interpretation

For this deterministic task, if the conventional baseline reproduces the same release correctly with fewer implementation files, fewer LOC, and fewer runtime stages, then CCS-015 must conclude that the compositional architecture does **not** demonstrate practical advantage for this task class. The human-interrupt/resume behavior may still be a distinct feature, but it must not be counted as a net advantage unless the task requires it.

If the compositional implementation shows a measurable advantage, the report must name the exact dimension rather than giving an overall marketing verdict.

## Acceptance

PASS means the comparison is reproducible and honestly reports the measured result. PASS does not mean the compositional approach wins.
