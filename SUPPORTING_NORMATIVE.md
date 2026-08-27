# ALP 1.0 Candidate — Supporting Normative Text

## Status and State Registry

### Transaction lifecycle states

| State | Normative meaning |
|---|---|
| `RECEIVED` | Job observed but not yet validated |
| `VALIDATING` | Structural/policy validation in progress |
| `AUTHORIZED` | Authority validated for declared consequence |
| `CLAIMING` | Ownership/claim attempt is being established |
| `CLAIMED` | Ownership has been durably established |
| `EXECUTING` | Consequential execution in progress |
| `VERIFYING` | Independent completion verification in progress |
| `PUBLISHED` | Verified/current result is published |
| `FAILED` | Attempt failed and is not represented as successful |
| `ROLLED_BACK` | Previously accepted/current result deliberately reversed |
| `INVALIDATED` | Previously published result is no longer valid |
| `BLOCKED_AMBIGUOUS` | Safe ownership/consequence cannot be proven |
| `HELD_DEPENDENCY` | Ancestor/dependency prevents execution/publication |
| `RETRYABLE` | Explicitly safe retry is permitted |
| `VERIFY_REQUIRED` | External effect must be checked before settlement/retry |

Verification statuses are `PASS`, `FAIL`, `NOT_ASSERTABLE`. `NOT_ASSERTABLE` MUST NOT be rendered as PASS.

Production conformance statuses are `REFERENCE_PRODUCTION_BRIDGE_PASS`, `REMOTE_TRANSPORT_OBSERVED`, `LIVE_CAPTURE_INCOMPLETE`, `LIVE_PRODUCTION_CONFORMANT`, and `INVALID`. Only `LIVE_PRODUCTION_CONFORMANT` certifies the full declared live production profile.

Evidence statuses are `VERIFIED`, `SIGNED_VERIFIED`, `FEDERATED_VERIFIED`, `SPLIT_VIEW`, and `INVALID`. A later layer MUST NOT erase failure at an earlier layer.

Release statuses are `EXPERIMENTAL`, `RELEASE_CANDIDATE`, and `STABLE`.

## Capability Registry

The proposed stable Core 1.0 capability IDs are:

| Capability | Meaning |
|---|---|
| `core.job-envelope` | Canonical governed job identity |
| `core.authority` | Scoped authority validation |
| `core.idempotency` | Duplicate-consequence control |
| `core.verification` | Independently attributable completion verification |
| `core.receipts` | Settlement evidence |
| `core.failure-recovery` | Explicit failure/retry/block/rollback semantics |
| `core.readiness` | Liveness/transport/transaction/execution separation |

A Core 1.0 implementation MUST declare all seven.

Profile/extension capabilities MAY use namespaces such as `transport.*`, `security.*`, `durability.*`, `evidence.*`, `custody.*`, `production.*`, `interop.*`, `benchmark.*`, and `exp.*`.

A profile capability MUST state its own version and stability status. Core 1.0 stability MUST NOT silently upgrade an alpha profile capability to stable.

After peers establish a required capability/security floor, a later negotiation MUST reject an offer that strips a required capability or lowers the established security epoch unless an explicit operator-approved downgrade procedure exists.

## Conformance Classes

### Core Conformant
MUST pass all Core invariants and normative Core conformance vectors and implement all seven `core.*` capabilities.

### Transport Conformant
MUST be Core Conformant and MUST pass transport integrity, stable delivery identity, acknowledgement, re-observation, no-authority-inference, metadata non-semantic, corruption fail-closed and duplicate-delivery vectors for its declared durability class. Transport conformance is per adapter/profile.

### Verifier Conformant
MUST consume declared inputs and produce independently attributable `PASS`/`FAIL`/`NOT_ASSERTABLE` results with enough evidence to recompute the declared assertions.

### Durable Continuation Conformant
MUST reconstruct declared governed state after process restart and preserve consequence-aware ambiguity/idempotency semantics.

### Evidence Bundle Conformant
MUST enforce strict file identity, semantic evidence requirements and fail closed on tamper. Signed/federated evidence are separate higher profiles.

### Production Conformant
MUST satisfy the applicable live production profile. Reference fixtures and remote-only observations MUST NOT be counted as production conformance.

### Extension Conformant
Extension conformance is version-specific. Passing an experimental extension does not make it stable.

No implementation or project MAY claim `ALP 1.0 STABLE` until the Stability Gate Audit records every mandatory gate PASS. A stable specification does not automatically certify a deployment.

## Versioning and Compatibility

The proposed stable core version is `1.0`. Until the Stability Gate Audit passes, the publication label MUST remain `ALP 1.0 Candidate`.

An implementation MUST explicitly declare supported protocol versions. Unsupported major versions MUST be rejected unless a separately specified compatibility adapter is used.

Within major version 1, additive optional fields MAY be introduced when old implementations can safely ignore them without changing governed semantics.

A change is breaking if it changes authority interpretation, consequence/idempotency semantics, normalized state meaning, receipt/evidence meaning, required capability meaning, verification requirements, or migration safety. Breaking changes require a new major protocol version.

Security profile epochs and required capability floors are monotonic unless an explicit, separately authorized downgrade procedure exists. Negotiation MUST reject silent downgrade and capability stripping.

A migration MUST preserve governed state required by the target profile, including authority freshness, receipts/evidence lineage and extension state. Unknown source data SHOULD be preserved where safe. Automatic downgrade migration SHOULD NOT be provided; if downgrade/export is supported, it MUST be explicitly named and separately authorized.

## Claims and Contribution Boundary

> Agent Lane defines a provider-neutral governed execution architecture in which probabilistic or deterministic reasoning sources propose work while authority, consequential execution, durable continuation, independent verification, recovery and evidence remain governed outside the reasoning model.

The contribution is the coherent execution model and protocol composition, not a claim to have invented agents, sandboxes, permissions, workflow durability, checkpoints, human-in-the-loop steering or audit logs individually.

The candidate MUST NOT claim live multi-provider API conformance, outside third-party implementation adoption, globally trusted signing/witness infrastructure, HSM-grade or Windows CNG custody, universal exactly-once side effects, distributed consensus, novelty/patentability/freedom to operate, or ALP 1.0 stable status before every stability gate passes.

Live Spec Reconciliation remains a separately versioned experimental profile. Core 1.0 Candidate status does not convert it into a stable extension.

## Implementation Guide

A minimal implementation should proceed in this order:

1. canonical governed job identity;
2. external/scoped authority validation;
3. idempotency or explicit consequence recovery class;
4. execution boundary;
5. independent verifier boundary;
6. receipt settlement;
7. failure/recovery state machine;
8. readiness separation;
9. transport adapter;
10. durable replay where continuation is supported.

Do not give the model/provider implicit authority. Treat provider output as proposed intent.

Before replaying after a crash, ask whether you can prove the consequence did not happen, prove exactly what effect happened, or safely replay by idempotency. If none are true, classify ambiguity rather than guessing.

A green executor result is not sufficient. The verifier should inspect the actual final state or artifact whenever independent observation is possible.
