# Agent Lane

> **Your AI keeps building. You keep testing.**

![Alpha](https://img.shields.io/badge/status-alpha-ec3013)
![Protocol](https://img.shields.io/badge/ALP-1.0--candidate-black)
![Local first](https://img.shields.io/badge/local--first-yes-black)
![No API key](https://img.shields.io/badge/API%20key-not%20required-black)
![No MCP](https://img.shields.io/badge/MCP-not%20required-black)

Agent Lane is a local-first handoff layer for AI-assisted software work. Its immediate job is narrow: **remove the manual gap between an AI finishing a coding task and a human actually testing it.**

A Lane task is routed to the correct product, worked against an isolated copy, surfaced in a product-specific Test Center, and kept in front of the human with only the controls needed to verify that change. The human can test, tweak, approve, or reject without reconstructing the environment from scratch while later work continues.

## The loop

```text
AI task
  ↓
Lane receives + identifies product
  ↓
Safe working copy
  ↓
Correct product browser opens/reuses
  ↓
Isolated Test Center
  ↓
Human tests / tweaks
  ↓
Approve or reject + receipt
  ↓
Next work keeps moving
```

## Alpha contract

A build is not alpha-ready until a person who did not build Lane can complete that loop without the author explaining it.

The current acceptance gate is documented in [`docs/ALPHA-GATE.md`](docs/ALPHA-GATE.md).

## What Lane is — and is not

Lane does **not** claim to invent coding agents, sandboxes, worktrees, browser automation, preview environments, or human-in-the-loop software engineering. Those are established methods.

Lane is focused on a different bottleneck: **the human testing handoff** — getting each finished task into a fast, isolated, product-aware test surface while later work continues.

## Measure it, don't market a guess

The alpha records task-to-test latency, human hands-on time, manual handoffs avoided, tweak-to-preview latency, settlement time, and recovery behavior. The measurement protocol is in [`docs/METRICS.md`](docs/METRICS.md).

## Proof products

Lane is being exercised against real products rather than toy demos, including **RoomForge**, **The Old Keep**, and **Ravenhurst**. They are evidence for the workflow, not separate requirements for understanding Lane.

---

# Agent Lane Protocol 1.0 Candidate — External Review

The deeper execution/governance substrate remains under external review as **ALP `1.0-candidate.1`**.

**Internal candidate audit:** PASS  
**Stable status:** **NOT YET**  
**Remaining stability gate:** `SG-06 — outside implementation/review`

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

## How to review the protocol

1. Read [`SPECIFICATION.md`](SPECIFICATION.md).
2. Read [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md).
3. Check [`EVIDENCE_STATUS.md`](EVIDENCE_STATUS.md) for what is and is not proven.
4. Submit findings using [`REVIEW_RESPONSE_TEMPLATE.md`](REVIEW_RESPONSE_TEMPLATE.md), preferably as a GitHub issue or pull request.

A useful review is critical, not ceremonial. Finding a contradiction, unsafe semantic, ambiguous state, missing capability, or overclaim is more valuable than saying the design looks good.

## What counts for SG-06

A review can satisfy SG-06 when it is attributable to a genuinely outside engineer/reviewer and includes substantive evaluation of the frozen candidate. An independent implementation is even stronger, but is not required if the review itself is technically substantive and preserved.

Internally authored code, automated self-review, reactions, stars, or a vague approval do **not** satisfy SG-06.

## Repository map

- [`SPECIFICATION.md`](SPECIFICATION.md) — frozen ALP candidate specification
- [`EVIDENCE_STATUS.md`](EVIDENCE_STATUS.md) — what is and is not proven
- [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) — external review path
- [`schemas/`](schemas/) — candidate schemas
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — product/test-loop architecture
- [`docs/ALPHA-GATE.md`](docs/ALPHA-GATE.md) — alpha acceptance criteria
- [`docs/METRICS.md`](docs/METRICS.md) — evidence plan for time savings
- [`SECURITY.md`](SECURITY.md) — security reporting
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution rules
- [`CHANGELOG.md`](CHANGELOG.md) — public changes

## Current status

**Product:** alpha construction.  
**Protocol:** `1.0-candidate.1`, not stable until SG-06 is satisfied.
