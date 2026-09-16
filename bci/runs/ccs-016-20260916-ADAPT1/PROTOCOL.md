# CCS-016 — Adaptive Comparative Baseline

Experiment ID: `CCS-016-20260916-ADAPT1`

## Research question
When a useful task receives an unanticipated natural-language policy change after both implementations are frozen, can a ChatGPT-centered compositional approach absorb that change with less measured adaptation burden than conventional automation while preserving verification?

## Roles
- Human: principal investigator; supplies the disruption only after both lanes are frozen.
- Ordinary ChatGPT: authors/finalizes experiment machinery, applies the human disruption to the compositional lane, and records evidence.
- GitHub Actions: hosted execution/verification substrate.

## Task
Given `input/releases.json`, produce a release-readiness report. Initial frozen policy:
1. APPROVE items where `tests_passed=true`, `security_review="pass"`, and `rollback_ready=true`.
2. HOLD all others.
3. Sort APPROVE first, then HOLD; within each group sort by `id`.
4. Output JSON and Markdown summaries with a deterministic digest.

The input contains additional fields intentionally not used by the initial policy. Their existence does not imply which field a later disruption will concern.

## Freeze rule
Before the disruption is supplied:
- conventional implementation must be committed and passing;
- compositional implementation must be committed and passing;
- both must produce semantically identical initial outputs;
- implementation files and their hashes are recorded in `freeze.json`;
- no policy-change file exists.

After `freeze.json` exists, the human supplies one natural-language policy change not disclosed before freeze.

## Adaptation measurement
For each lane measure from the frozen commit to verified adapted completion:
- implementation files touched;
- implementation lines added/deleted;
- human messages required after disruption;
- failed workflow attempts before success;
- successful workflow runs required;
- elapsed runner time from first disruption-triggered run start to verified successful run completion;
- whether pre-disruption output semantics were preserved except where the new policy requires change;
- whether an independent verifier confirms the adapted result.

ChatGPT conversation latency is not treated as a precise wall-clock performance measure. GitHub workflow timestamps are the authoritative timing source.

## Conventional lane
Plain Python + GitHub Actions. The initial policy is encoded directly in code. After disruption, any required behavior change must be implemented by changing conventional code/configuration. No LLM interprets the policy at runtime.

## Compositional lane
Durable task state + policy artifact + ordinary ChatGPT reasoning + generated/updated executable policy adapter + hosted execution + independent verifier. The disruption arrives as natural-language durable input after freeze. Any adaptation performed by ChatGPT must be explicit in the repository diff and evidence.

## Fairness constraints
- Same input dataset.
- Same initial policy and required report schema.
- Same human disruption wording for both lanes.
- Same final semantic acceptance tests.
- Do not weaken verifier criteria after seeing a failure.
- A lane may lose. Report the measured outcome without reinterpretation.

## Outcome classification
`COMPOSITION_LOWER_ADAPTATION_BURDEN`, `CONVENTIONAL_LOWER_ADAPTATION_BURDEN`, `MIXED_TRADEOFF`, or `INCONCLUSIVE`.

A PASS means the comparison was controlled and measured, not that either architecture won.
