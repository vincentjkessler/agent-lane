# Agent Lane Protocol 1.0 Candidate — External Review

**Candidate:** `1.0-candidate.1`  
**Internal candidate audit:** PASS  
**Stable status:** **NOT YET**  
**Remaining stability gate:** `SG-06 — outside implementation/review`

This repository is a deliberately bounded public review surface for the Agent Lane Protocol (ALP) 1.0 Candidate. It is not a marketing page and it is not asking reviewers to endorse the project.

## What Agent Lane is

ALP specifies a governed consequential-execution substrate between probabilistic or deterministic reasoning systems and real execution environments. The reasoning system proposes work; authority, consequential execution, durable continuation, independent verification, recovery and evidence remain governed outside the reasoning model.

## Current stability-gate status

- **SG-03 — Live Drive Adapter 001:** PASS. A live Windows Receiver consumed a real Google Drive activation, executed an authorized workspace effect, independently verified it, and emitted a matching immutable receipt.
- **SG-04 — Second materially different real adapter:** PASS. Local Folder Adapter 002 and the live Google Drive sync-folder adapter passed the same seven normalized transport semantics with 7/7 equivalence.
- **SG-06 — Outside implementation/review:** BLOCKED. This public review is intended to resolve that gate.

ALP **must not be called 1.0 Stable** until SG-06 is satisfied and the frozen candidate audit is rerun.

## Frozen candidate identities

- Candidate freeze SHA-256: `cd0119c4cd4cb24035bb9e7b375747961ba36f1be93e8da40757559190c6c8dd`
- Normative document set SHA-256: `b46365ee97c1797f8872a2cbee51b15e604cb680183db41afec205fc8525ce0c`
- Candidate schema set SHA-256: `ea5e435e5e237155e897b7285623d97e4db85b00825b19c04aa956466251407b`
- v0.18 engineering RC freeze SHA-256: `ab29be6c5de8ef8147e1cc7327fae105e80ed6f8a8a4667fb1b11f1321a8e55d`

## How to review

1. Read [`SPECIFICATION.md`](SPECIFICATION.md).
2. Read [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md).
3. Check [`EVIDENCE_STATUS.md`](EVIDENCE_STATUS.md) for what is and is not proven.
4. Submit findings using [`REVIEW_RESPONSE_TEMPLATE.md`](REVIEW_RESPONSE_TEMPLATE.md), preferably as a GitHub issue or pull request.

A useful review is critical, not ceremonial. Finding a contradiction, unsafe semantic, ambiguous state, missing capability, or overclaim is more valuable than saying the design looks good.

## What counts for SG-06

A review can satisfy SG-06 when it is attributable to a genuinely outside engineer/reviewer and includes substantive evaluation of the frozen candidate. An independent implementation is even stronger, but is not required if the review itself is technically substantive and preserved.

Internally authored code, automated self-review, reactions, stars, or a vague approval do **not** satisfy SG-06.
