# ECS-012 / ECS-007 — ECL Release Steward

Experiment ID: `ECS-012-20260916-APP1`

## Objective
Demonstrate a useful application-like system assembled from ordinary ChatGPT reasoning, GitHub durable state, generated executable instruments, GitHub Actions compute/verification, a human interrupt/steer, and resumable state — without a conventional coordinating application, Codex, ChatGPT Work, local terminal, user download/upload loop, or user-supplied API key.

## Useful job
Produce a verified release/status package for the live Emergent Capability Laboratory registry at `bci/emergent-capability-surface/map.json`.

## Stage 1 — Analyze
A push of `trigger-stage1.json` causes GitHub Actions to:
1. read the live capability map;
2. generate `analysis.json` with confirmed/candidate counts, IDs, statuses, boundaries, evidence references, and a canonical digest;
3. independently verify the analysis;
4. update `state.json` to `AWAITING_HUMAN_STEER`;
5. commit the generated analysis/state.

## Human interrupt
The runtime must stop in `AWAITING_HUMAN_STEER`. A later human choice is written to `steer.json` and must be one of:
- `CONSERVATIVE`: publish confirmed capabilities and confirmed boundaries only; candidate details are excluded from the release payload.
- `FRONTIER`: publish confirmed capabilities plus the current candidate frontier and statuses.

This choice materially changes `release.json` and `ECL_STATUS.md`.

## Stage 2 — Resume and finalize
A push of `steer.json` causes GitHub Actions to:
1. require current state `AWAITING_HUMAN_STEER`;
2. render `release.json` and `ECL_STATUS.md` according to the human policy;
3. independently recompute and verify the required release content;
4. update `state.json` to `COMPLETE`, recording `human_interrupt_applied: true` and the selected steer;
5. commit the generated release/state.

## Acceptance — ECS-007
PASS only if Stage 1 reaches `AWAITING_HUMAN_STEER`, no Stage 2 artifact exists beforehand, a human supplies a valid steer after that state exists, and Stage 2 resumes from the durable state and completes with the selected policy reflected in the verified output.

## Acceptance — ECS-012
PASS only if the system delivers its useful job end-to-end through the composition of external state, generated instruments, hosted execution, independent verification, human control, and final durable artifacts, without a conventional monolithic application coordinating the process.

## Non-claims
This does not claim that individual primitives are undocumented or novel. It tests whether their composition behaves as a useful application-like system. It also does not by itself confirm autonomous repair behavior for ECS-010.
