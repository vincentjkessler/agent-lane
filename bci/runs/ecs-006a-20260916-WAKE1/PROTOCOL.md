# ECS-006A — Condition-Triggered Scheduled Runtime

Experiment ID: `ECS-006A-20260916-WAKE1`

## Objective
Test whether ordinary ChatGPT Scheduled monitoring can advance an external runtime after an external GitHub condition becomes true, without the user opening or sending a new chat after the monitor is armed.

This is deliberately **not** a webhook/event-triggered Work task. It tests the strongest ordinary-ChatGPT-compatible mechanism: scheduled monitoring for a changing external condition.

## Authoritative paths
- State: `bci/runs/ecs-006a-20260916-WAKE1/state.json`
- Trigger: `bci/runs/ecs-006a-20260916-WAKE1/trigger.json`
- Compute: `bci/runs/ecs-006a-20260916-WAKE1/compute.py`
- Verifier: `bci/runs/ecs-006a-20260916-WAKE1/verify.py`
- Workflow: `.github/workflows/ecs-006a-wake.yml`
- Final receipt: `bci/runs/ecs-006a-20260916-WAKE1/receipt.json`

## Trigger semantics
The monitor is armed while `trigger.json` does not yet exist. After arming, a new `trigger.json` commit is created. That commit launches the hosted workflow. The monitor must later detect the trigger and successful hosted run, retrieve the externally computed result and independent verification, then write `receipt.json` and advance `state.json` to `COMPLETE`.

## Challenge
`trigger.json` supplies:
- seed: 24681357
- modulus: 2147483647
- multiplier: 48271
- iterations: 60000
- checkpoint_interval: 1009

For i = 1..iterations:
`x = (multiplier*x + i*i + 53*i + 211) mod modulus`

At every exact checkpoint interval, append decimal x. Result fields:
- schema = `ecs-006a-result/v1`
- final_x
- checkpoint_count
- checkpoints_sha256 = lowercase SHA-256 of comma-joined checkpoint decimal values, no spaces

`compute.py` produces the result. `verify.py` independently recomputes it and must print `ECS006A_VERIFY=PASS` or fail nonzero. The workflow must print `ECS006A_RESULT=<compact-json>`.

## Acceptance
PASS only if:
1. The Scheduled monitor was created before `trigger.json` was committed.
2. No user message or manually opened continuation chat is needed after arming.
3. The trigger commit causes a distinct GitHub Actions hosted run.
4. The hosted compute and independent verifier succeed.
5. A later Scheduled monitor invocation discovers the external condition/result.
6. That invocation writes `receipt.json` with trigger commit, workflow run/job IDs, external result, verification PASS, and `manual_chat_after_arm=false`.
7. That invocation updates `state.json` to `status: COMPLETE`.

If connected-app write approval blocks the scheduled invocation, classify INCONCLUSIVE rather than PASS.