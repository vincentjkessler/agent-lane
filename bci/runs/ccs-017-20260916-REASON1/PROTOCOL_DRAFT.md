# CCS-017 — Runtime Reasoning Contribution Benchmark

Status: **DRAFT FOR EXTERNAL REVIEW — DO NOT EXECUTE**  
Experiment ID: `CCS-017-20260916-REASON1`

## Research question

With the same LLM model, task evidence, permitted tools, and resource ceilings, does the CCS compositional architecture produce measurably better decisions or lower total burden than a simpler AI-enabled workflow? Separately, how much does either AI approach improve on a competent deterministic rules/configuration system?

This experiment is designed to separate three possible sources of value:

1. deterministic automation;
2. the underlying LLM's runtime interpretation;
3. the additional CCS architecture around that same LLM.

CCS-017 is not intended to prove that composition is universally superior. A simpler lane may win or tie.

## Motivation from CCS-015 and CCS-016

CCS-015 and CCS-016 used deterministic policy logic. CCS-016 recorded lower line churn for the conventional lane (`10` versus `12`) but external review judged that difference too small to establish a practically meaningful total-effort difference at that scale. CCS-016 also observed a real locality property: the compositional lane changed policy configuration without changing engine code, while the conventional lane changed code. Whether that locality produces value at larger scale remains untested.

CCS-017 therefore tests **runtime interpretation of unstructured evidence**, not another prepared boolean-field policy.

## Task class

Each release case contains ordinary-language evidence snippets with stable evidence IDs. Evidence may include:

- test summaries;
- security-review notes;
- deployment notes;
- migration notes;
- rollback descriptions;
- documentation notes;
- operator comments.

Some cases contain explicit contradictions across sources. Some omit information required to decide safely. The input does **not** include prepared booleans such as `rollback_ready=true`.

### Fixed release requirements

A release may be `APPROVE` only when the evidence supports all required conditions and contains no unresolved contradiction that invalidates them:

1. required tests passed;
2. security review supports release;
3. a workable rollback path actually exists;
4. required release documentation is ready.

Decision semantics:

- `APPROVE`: all requirements are positively supported and no unresolved evidence contradicts them.
- `HOLD`: evidence establishes that at least one required condition fails, including when a nominal claim is contradicted by stronger concrete evidence. Example: a summary says rollback is available, but migration notes state that data required by the prior version will be permanently deleted.
- `CLARIFY`: evidence is insufficient or materially ambiguous for a required condition, but does not establish that the condition fails.

Holding every case cannot score well because the hidden set must contain genuine `APPROVE`, `HOLD`, and `CLARIFY` cases.

## Required output per case

Each lane must emit the same structured record:

```json
{
  "case_id": "...",
  "decision": "APPROVE | HOLD | CLARIFY",
  "evidence_ids": ["E1", "E4"],
  "reason_codes": ["ROLLBACK_CONTRADICTION"],
  "clarification_needed": [],
  "explanation": "Concise evidence-grounded explanation."
}
```

No score is awarded for rhetorical persuasiveness. Decisions, evidence selection, and treatment of uncertainty are graded.

## Three comparison lanes

### Lane A — deterministic rules/configuration

A competent non-LLM implementation.

- Runtime LLM calls: `0`.
- May use arbitrary committed deterministic Python and configuration, including regexes, phrase dictionaries, negation handling, contradiction rules, and other deterministic parsing.
- May be tuned on the public development set.
- May not access the hidden gold labels before outputs are frozen.
- Implementation size and development burden are measured; there is no artificial LOC cap.

This lane answers: **what can conventional automation do on this task class, and at what cost?**

### Lane B — simple same-LLM workflow

A minimal AI-enabled baseline using **GPT-5.6 Sol**.

- One separate cold ordinary ChatGPT conversation.
- Receives the fixed policy, output schema, public development examples, and pointer to the hidden test evidence.
- No prior task conversation context.
- No persistent lane-specific state machine, case ledger, staged runtime, scheduled observer, or CCS continuation protocol.
- May use the same permitted GitHub tools as Lane C within the same ceilings.
- May run the common non-gold schema/citation validator once and make at most one correction within the same assistant turn.

This lane answers: **how much does the model itself contribute with minimal surrounding machinery?**

### Lane C — CCS compositional workflow using the same LLM

Uses **GPT-5.6 Sol**, matching Lane B.

- One separate cold ordinary ChatGPT conversation.
- Same policy, development examples, hidden test evidence, GitHub permissions, and resource ceilings as Lane B.
- Begins from one frozen external-state pointer.
- May use the frozen CCS scaffold: durable state, case/evidence index, staged retrieval, structured receipts, and deterministic schema/citation validation.
- The scaffold must not contain hidden gold decisions, gold evidence sets, or case-specific hints.
- May run the same common non-gold validator once and make at most one correction within the same assistant turn.

This lane answers: **does the CCS architecture add measurable value beyond the same underlying model?**

## AI-lane parity controls

Lanes B and C must use:

- the exact same model/version: GPT-5.6 Sol;
- separate cold conversations;
- the same policy wording;
- the same public development set;
- the same hidden test cases;
- the same permitted connected tool: GitHub only;
- no web browsing, Work, Codex, other LLMs, scheduled tasks, or local terminal during test execution;
- one human initiation and one assistant turn per lane;
- at most 25 GitHub read calls;
- at most 2 GitHub write calls;
- at most 1 hosted non-gold validator run;
- at most 1 correction attempt after that validator;
- no human clarification or steering after test execution begins.

Actual model/tool usage is recorded. If the product does not expose token counts or dollar cost, those values must be reported as unavailable rather than estimated.

## Public development set and hidden test set

### Development set

Before freezing implementations, all lanes receive a public development set of **9 cases**:

- 3 APPROVE;
- 3 HOLD;
- 3 CLARIFY.

The development set demonstrates the schema and decision semantics but must not duplicate hidden test language.

### Hidden test set

After all three implementations/prompts/scaffolds are frozen, an external case author who is not GPT-5.6 Sol creates a hidden test set of **30 cases**:

- 10 gold APPROVE;
- 10 gold HOLD;
- 10 gold CLARIFY.

Requirements for the hidden set:

- each case has stable evidence IDs;
- at least 10 cases contain cross-document contradictions;
- at least 8 cases require distinguishing missing information from demonstrated failure;
- wording must include paraphrases not present in the public development set;
- no case may depend on stylistic preference or an unspecified risk threshold;
- every gold decision must be derivable from the fixed release requirements.

The external author produces two separate artifacts:

1. `test-cases.json` — evidence only, revealed after freeze;
2. `gold.json` — decision/evidence/reason gold, kept sealed until all three lane outputs and hashes are frozen.

Astra 6 may serve as the external case author, but this is not required by the protocol.

## Gold validation and evaluator boundary

Model agreement alone is not treated as human validation.

Before unsealing gold for scoring, record whether a human reviewer validated the gold labels/evidence rationales. Preferred status is `HUMAN-VALIDATED-GOLD`.

If full human validation is unavailable, the experiment may proceed but final status must be `PROVISIONAL-GOLD-NOT-FULLY-HUMAN-VALIDATED`. At minimum, any available human spot-check method and sample must be recorded.

Opus 4.6 or another model may provide secondary external review, but that review must explicitly state whether it:

- reviewed only a summary;
- inspected the artifacts;
- reran any checker;
- had access to gold;
- performed model-based qualitative grading.

No model review is described as independent human validation.

## Common non-gold validator

Before gold is revealed, both AI lanes may use the same deterministic validator. It may check only:

- JSON/schema validity;
- valid decision labels;
- cited evidence IDs actually exist in that case;
- no duplicate case IDs;
- all required test cases are present.

It must not contain or reveal gold decisions, expected evidence sets, or correctness feedback.

Lane A may use the same validator after producing its output.

## Scoring — fixed before execution

Primary objective score: **100 points**.

### 1. Decision correctness — 60 points

Exact decision match against sealed gold. Each of 30 cases contributes 2 points.

### 2. Evidence identification — 25 points

Micro-averaged F1 between cited `evidence_ids` and the gold-required evidence IDs across all cases. Score = `25 * F1`.

Gold may specify multiple acceptable evidence sets when genuinely equivalent evidence exists.

### 3. Reason/uncertainty handling — 15 points

Micro-averaged F1 over structured `reason_codes` and, for CLARIFY cases, `clarification_needed` categories. Score = `15 * F1`.

### Safety/error counts reported separately

Do not hide these inside the composite score:

- false approvals: gold HOLD or CLARIFY predicted APPROVE;
- unnecessary holds: gold APPROVE predicted HOLD;
- missed clarifications: gold CLARIFY predicted APPROVE or HOLD;
- unsupported citations: cited evidence IDs not valid/relevant under gold;
- omitted cases.

### Explanation review

Free-text explanations are not scored for style. Human or external qualitative review may check whether explanations faithfully connect the cited evidence to the decision. Any such review is reported separately from the 100-point objective score.

## Effort and cost metrics

Record for each lane separately:

### Build/freeze burden

- implementation files;
- implementation LOC;
- prompt/config LOC;
- human messages needed to prepare/freeze;
- model-assisted implementation turns;
- failed build/test attempts;
- workflow/runner seconds used before hidden testing.

### Hidden-test execution burden

- runtime model turns;
- GitHub read calls;
- GitHub write calls;
- hosted validator runs;
- correction attempts;
- failed execution attempts;
- workflow/runner seconds;
- human messages/interventions after test start;
- durable artifacts produced.

### Cost

Record exact token counts and monetary cost only if the product exposes them. Otherwise record `UNAVAILABLE` and do not fabricate estimates.

Shared evaluation work such as test-case ingestion, gold scoring, and common validator execution must be separated from lane-specific burden.

## Predeclared interpretation thresholds

These thresholds are practical decision rules, not claims of statistical equivalence.

### Material quality difference

A difference of **8 or more points** on the 100-point objective score is treated as materially different for this 30-case experiment.

A reduction of **3 or more false approvals** may also be treated as materially safety-relevant if the overall score is not more than 4 points worse.

### Practical quality tie

If two lanes differ by fewer than 8 score points and fewer than 3 false approvals, report `PRACTICAL_QUALITY_TIE` between those lanes. Do not convert tiny LOC or timing differences into a winner.

### Burden difference

For lanes in a practical quality tie, a burden advantage is called material only if one lane reduces at least **two independent observable burden measures by 25% or more** without increasing another primary burden measure by 25% or more. Primary burden measures are:

- human interventions;
- runtime model turns;
- GitHub tool calls;
- workflow/runner seconds;
- implementation + prompt/config LOC required for the tested system.

If this threshold is not met, report no meaningful burden difference established.

## Outcome interpretations

### Evidence supporting the CCS architecture

`CCS_ARCHITECTURE_ADDS_MEASURABLE_VALUE` only if Lane C versus Lane B shows either:

1. a material quality advantage under the rules above with no worse false-approval count; or
2. a practical quality tie plus a material burden advantage under the predeclared burden rule.

### Evidence favoring the simple same-LLM workflow

`SIMPLE_LLM_WORKFLOW_PREFERRED_FOR_THIS_TASK` if Lane B versus Lane C shows the symmetric quality/burden advantage.

### Evidence favoring deterministic automation

`DETERMINISTIC_AUTOMATION_SUFFICIENT_FOR_THIS_TASK` if Lane A is in a practical quality tie with the best AI lane and has a material burden advantage.

### Mixed result

`MIXED_TRADEOFF` when one approach is materially better on quality but materially worse on burden, or safety metrics conflict with the aggregate score.

### Unresolved

`INCONCLUSIVE` if any critical control is violated, including:

- hidden cases leaked before freeze;
- AI lanes use different model versions;
- one AI lane receives extra evidence or materially different tool permissions;
- gold cannot be traced to a sealed pre-score artifact;
- outputs are modified after gold reveal;
- execution exceeds resource ceilings without a predeclared exception.

If gold lacks adequate human validation, use a provisional qualifier even if the technical comparison otherwise completes.

## Freeze sequence

1. External reviewers approve or revise this protocol.
2. Create the 9-case public development set.
3. Build/tune Lane A.
4. Freeze Lane B prompt/harness.
5. Freeze Lane C protocol/state/scaffold.
6. Verify the three lanes on the public development set.
7. Record all source/prompt/config hashes and resource ceilings.
8. Declare `FROZEN_AWAITING_HIDDEN_TEST`.
9. External case author creates hidden `test-cases.json` and sealed `gold.json` after freeze.
10. Reveal only `test-cases.json`.
11. Execute all three lanes and freeze their output hashes.
12. Reveal `gold.json`.
13. Run deterministic scoring.
14. Perform and document any human/secondary external review.
15. Report correctness and safety first, then burden and cost, then the predeclared interpretation.

## Current stop condition

**Do not build implementations or create evaluation cases yet.**

CCS-017 remains `DRAFT FOR EXTERNAL REVIEW` until the principal investigator returns protocol feedback. This avoids designing the benchmark after seeing results and lets reviewers challenge the fairness controls, scoring, and thresholds before execution.
