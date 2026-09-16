# ECS-006B — Autonomous Wake + Verified State Transition

Experiment ID: `ECS-006B-20260916-WAKE2`

## Objective
Test whether ordinary ChatGPT Scheduled can autonomously wake after an externally produced durable state transition, read and verify the resulting GitHub state, and notify the user without any user-started chat after the monitor is armed.

This experiment deliberately separates mutation from observation:

1. The monitor is armed while state is `WAITING_FOR_TRIGGER` and `trigger.json` does not exist.
2. Only after the monitor is armed, `trigger.json` is created with `status: READY`.
3. The push triggers `.github/workflows/ecs-006b-wake.yml`.
4. GitHub Actions performs the computation, independently verifies it, writes `receipt.json`, updates `state.json` to `COMPLETE`, and commits those durable state changes back to `bci-wire`.
5. Scheduled ChatGPT must later wake without a new user-started chat, observe `COMPLETE`, independently verify the GitHub Actions run/logs against `receipt.json` and `state.json`, and notify the user of PASS.

## Control constraints
- Ordinary consumer ChatGPT only; no ChatGPT Work and no Codex.
- No local terminal.
- No user download/upload loop.
- No user-supplied API key.
- No user-started chat after the monitor is armed.
- Scheduled ChatGPT performs no external mutation for acceptance; all durable mutation is performed by GitHub Actions.
- The scheduled observer must not call PASS unless the workflow run succeeded, the verifier printed `ECS006B_VERIFY=PASS`, and GitHub contains both a matching `receipt.json` and `state.json` with `status: COMPLETE`.

## Challenge
Read `input.json` and compute:

- `x = seed`
- for `i = 1..iterations`: `x = (multiplier*x + (i*i + 43*i + 211)) mod modulus`
- whenever `i % checkpoint_interval == 0`, append decimal `x` to the checkpoint list
- `checkpoint_sha256` is lowercase SHA-256 of the comma-joined checkpoint decimals, no spaces

Result schema `ecs-006b-result/v1` fields:
- `final_x`
- `checkpoint_count`
- `checkpoint_sha256`
- `schema`

## Required machine-readable evidence
Workflow logs must contain:
- `ECS006B_RESULT=<compact sorted JSON>`
- `ECS006B_VERIFY=PASS`

GitHub Actions must commit:
- `bci/runs/ecs-006b-20260916-WAKE2/receipt.json`
- updated `bci/runs/ecs-006b-20260916-WAKE2/state.json`

## PASS criteria
PASS only if:
1. monitor was armed before trigger creation;
2. trigger was created after arming and caused the hosted workflow;
3. hosted compute + independent verifier both passed;
4. Actions, not Scheduled ChatGPT, wrote the durable receipt and COMPLETE state;
5. Scheduled ChatGPT later woke without a user-started chat, read those durable outputs, checked the corresponding workflow run/job/logs, and notified the user of PASS.

A scheduled wake that requires a user message, a failed verifier, missing durable write-back, or an observer that merely trusts `state.json` without checking the run/logs is not a PASS.
