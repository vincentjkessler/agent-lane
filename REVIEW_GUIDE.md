# Agent Lane Protocol 1.0 Candidate — External Review Guide

This review exists specifically to resolve stability gate `SG-06`.

A reviewer is **not** being asked to endorse marketing language or agree that Agent Lane is novel. The review target is the protocol candidate, its safety semantics, and whether its claims match its evidence.

## Review questions

1. Are the twelve Core invariants internally coherent?
2. Does authority-before-consequence have any semantic loophole?
3. Are execution, verification and settlement sufficiently separated?
4. Are the registered lifecycle/recovery states mutually intelligible and non-contradictory?
5. Does restart behavior fail closed at ambiguous consequence boundaries?
6. Are transport/provider metadata correctly separated from governed semantic identity?
7. Are the seven Core capabilities sufficient and clearly defined?
8. Do compatibility/downgrade rules avoid unsafe silent coercion?
9. Are reference, remote observation and live-production claims clearly distinguished?
10. Are any claims stronger than the evidence presented?
11. Is there any normative MUST/MUST NOT that cannot be implemented without guessing?
12. Is there any missing state transition or failure class that could allow an unsafe consequence?

## What qualifies as substantive outside review

A useful review should include:

- reviewer GitHub identity or otherwise attributable engineering identity;
- what documents were reviewed;
- specific findings, including `NONE FOUND` only after addressing the questions above;
- ambiguities or contradictions found;
- severity for each material issue;
- whether the reviewer believes the candidate can be implemented without relying on undocumented interpretation;
- any recommended change required before stable status.

An independent implementation is stronger evidence but is not mandatory.

## Independent implementation target

A reviewer/implementer may target only Core 1.0 Candidate first. They do not need to implement experimental profiles such as Live Spec Reconciliation, witness federation or protected custody.

A useful independent implementation result should include:

- implementation repository/commit identity;
- supported Core capability declaration;
- conformance-vector results;
- deviations or ambiguities found in the normative text;
- any state/capability meaning that required interpretation outside the spec.

## Current gate state

`SG-03` and `SG-04` now have live evidence and are PASS. `SG-06` is the only remaining stability gate.

A favorable outside review does **not** automatically make the protocol stable. The review must be preserved, the exact frozen candidate must be rerun through its audit, and any substantive finding must be resolved without silently weakening the stability rules.
