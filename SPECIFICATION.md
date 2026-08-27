# Agent Lane Protocol 1.0 Candidate

**Document status:** Normative candidate  
**Stability status:** `V1_STABLE_BLOCKED` until the Stability Gate Audit is satisfied  
**Normative keywords:** MUST, MUST NOT, SHOULD, SHOULD NOT, MAY

## 1. Purpose

Agent Lane Protocol (ALP) specifies a governed consequential-execution substrate
between probabilistic or deterministic reasoning systems and real execution
environments.

ALP standardizes the semantics of authority, job identity, idempotency,
execution, verification, receipts, failure, recovery, readiness, transport,
capabilities and evidence.

ALP does not standardize a model, user interface, transport vendor, programming
language or reasoning algorithm.

## 2. Logical roles

A conforming deployment has the following logical roles:

```text
INTELLIGENCE / INTENT SOURCE
            ↓
TRANSPORT
            ↓
LANE CORE
            ↓
EXECUTION BOUNDARY
            ↓
VERIFICATION / EVIDENCE
```

An implementation MAY combine roles in one process. Conformance is determined
by semantic behavior, not process topology.

## 3. Core invariants

### ALP-I001 — Intelligence independence
Lane Core MUST NOT require ownership of the upstream reasoning provider.

### ALP-I002 — Transport-semantic independence
Governed job semantics MUST NOT depend on transport-specific names, paths,
provider IDs or APIs except where a profile explicitly declares such metadata
as integrity evidence.

### ALP-I003 — Authority before consequence
A consequential operation MUST NOT begin unless Lane has independently
validated authority covering the target, operation class, scope and freshness
identity.

### ALP-I004 — Execution is not verification
An executor's success claim MUST NOT by itself establish successful final state.

### ALP-I005 — Settlement evidence
Every settled consequential attempt MUST produce a receipt. An attempt whose
prior external consequence cannot be proven MUST instead remain explicitly
ambiguous or verification-required; it MUST NOT be represented as settled PASS.

### ALP-I006 — Ambiguity fails closed
If prior ownership or consequence cannot be proven, Lane MUST stop automatic
dependent/new consequence where replay could be unsafe.

### ALP-I007 — Duplicate-consequence control
Repeated delivery of the same governed job MUST NOT cause uncontrolled
duplicate consequences. The implementation MUST use idempotency, effect
verification, explicit ambiguity, or another profile-defined safe mechanism.

### ALP-I008 — Dependency safety
A checkpoint or descendant result MUST NOT remain current/valid when a required
ancestor is failed, rolled back or invalidated.

### ALP-I009 — Liveness is not readiness
Process liveness or heartbeat freshness MUST NOT alone establish execution
readiness.

### ALP-I010 — Evidence before attention
A user-visible success/attention signal SHOULD be emitted only after the
profile's evidence threshold is satisfied. Infrastructure-only changes SHOULD
remain silent unless operator action is required.

### ALP-I011 — Provider intent is not authority
A model/tool-call/provider request MUST NOT itself grant execution authority.

### ALP-I012 — Receipt is not reality
A PASS receipt MUST NOT override contradictory independently observed final
state. Production profiles MUST define how effect evidence is reconciled.

## 4. Canonical governed job

A Core-Conformant job MUST identify:

- protocol/schema identity;
- job identity;
- project/target identity;
- authority reference;
- operation class;
- inputs;
- preconditions;
- execution contract;
- verification contract;
- dependency/checkpoint rules when applicable;
- rollback policy;
- output contract;
- idempotency identity or explicit non-idempotent recovery class.

The semantic job identity MUST be canonical-hashable.

Transport/provider metadata MUST remain outside semantic identity unless the
applicable profile explicitly says otherwise.

## 5. Authority

Authority MUST be scoped, freshness-bounded and independently checkable before
consequence.

Authority MUST NOT be inferred solely from transport possession, filename,
directory location, process liveness, package possession, provider intent or a
prior successful job.

An authority mechanism SHOULD use an epoch, nonce, signed grant, brokered
capability or equivalent anti-stale identity.

## 6. Core lifecycle

Primary path:

```text
RECEIVED
→ VALIDATING
→ AUTHORIZED
→ CLAIMING
→ CLAIMED
→ EXECUTING
→ VERIFYING
→ PUBLISHED
```

Core terminal/invalidating states:

- `PUBLISHED`
- `FAILED`
- `ROLLED_BACK`
- `INVALIDATED`

Core recovery/blocking states:

- `BLOCKED_AMBIGUOUS`
- `HELD_DEPENDENCY`
- `RETRYABLE`
- `VERIFY_REQUIRED`

An implementation MAY expose additional internal states, but normalized
conformance output MUST map them to the registered ALP meanings.

A worker or verifier crash MUST NOT leave a result represented as healthy PASS
without subsequent settlement evidence.

## 7. Readiness

A Core-Conformant implementation SHOULD expose independent readiness dimensions:

1. `process_liveness`
2. `transport_readiness`
3. `transaction_readiness`
4. `execution_readiness`

Top-level `READY` MUST require all readiness conditions declared by the
implementation profile, including absence of blocking unresolved ambiguity.

A UI MUST NOT infer top-level READY solely from a PID, service state or fresh
heartbeat.

## 8. Verification

Verification MUST be separately attributable from execution, even if both roles
run on the same host.

A normalized verification result MUST identify:

- verifier identity/version;
- verified input/artifact identity;
- assertion(s);
- observed result;
- one of `PASS`, `FAIL`, `NOT_ASSERTABLE`.

Free-form intent MUST NOT receive verified PASS unless the verifier can
independently assert the relevant property.

## 9. Receipts

A settlement receipt MUST bind at minimum:

- job identity;
- attempt identity;
- target/project;
- authority identity/freshness;
- operation class;
- settlement status;
- verifier identity/result when verification is required;
- relevant dependency identities;
- relevant artifact/effect identity;
- protocol/profile version;
- settlement time or ordering identity.

Receipts SHOULD be content-hashed.

If receipt chaining is used, a conforming implementation MUST ship or identify
a chain verifier.

## 10. Failure, retry and rollback

`FAILED` MUST be distinguishable from worker crash, verifier crash, dependency
hold, authority rejection, transport failure and ambiguity.

A failed attempt MAY retry only through an explicit retry transition.

When an ancestor fails or is rolled back:

- unpublished descendants MUST become `HELD_DEPENDENCY` or equivalent;
- already-published dependent descendants MUST become `INVALIDATED` or
  equivalent;
- invalid descendants MUST NOT remain represented as current/green.

## 11. Consequence-aware restart

Profiles supporting durable continuation MUST classify unresolved consequential
operations into at least one of:

- safely replayable/idempotent;
- externally verifiable before settlement;
- manually ambiguous.

Automatic restart MUST NOT cross a manually ambiguous consequence boundary.

## 12. Transport contract

A Transport-Conformant adapter MUST provide semantic equivalents of:

```text
send(channel, payload)
watch(channel)
receive(channel, delivery_id)
acknowledge(channel, delivery_id)
```

The adapter MUST preserve payload integrity or provide sufficient integrity
metadata to detect corruption.

Unacknowledged durable deliveries MUST remain re-observable according to the
adapter's declared durability class.

Transport possession MUST NOT imply authority.

Transport-specific metadata MUST NOT alter normalized governed semantics.

## 13. Capability negotiation

Implementations MUST declare supported capabilities.

Core 1.0 capability IDs are defined in `CAPABILITY_REGISTRY_1.0_CANDIDATE.md`.

A required capability that is absent or version-incompatible MUST cause
negotiation rejection.

A previously established security/capability floor MUST NOT be silently
downgraded.

Unsupported capabilities MUST NOT be implied by user interface or receipt.

## 14. Provider normalization

Provider-specific interaction envelopes MAY be normalized into governed intent.

Normalization MUST reject ambiguous multiple consequential directives and
unknown schemas rather than guessing.

Provider metadata that is declared non-semantic MUST NOT alter the canonical
governed intent identity.

## 15. Evidence

Evidence claims MUST distinguish:

- reference/test evidence;
- remote-provider observation;
- actual local runtime capture;
- production conformance;
- signed/authenticated evidence;
- independently witnessed evidence.

A stronger evidence status MUST NOT be inferred from a weaker status.

## 16. Extensions

Features outside the Core 1.0 conformance class MAY remain separately versioned
experimental extensions.

Core 1.0 stability MUST NOT be interpreted as stability of an extension whose
own document remains `0.x` or `alpha`.

Experimental extensions in the reference repository include Live Spec
Reconciliation, benchmark profiles, witness federation, production bridge and
other separately versioned profiles.

## 17. Conformance

Conformance classes and their exact requirements are normative in
`CONFORMANCE_CLASSES_1.0_CANDIDATE.md`.

Passing the reference unit tests is evidence for the reference implementation;
it does not automatically certify a live deployment.

## 18. Compatibility and migration

Compatibility, downgrade and migration behavior are normative in
`VERSIONING_AND_COMPATIBILITY_1.0_CANDIDATE.md`.

Implementations MUST NOT silently coerce unsupported protocol versions into
compatibility.

## 19. Stability gate

This document is a 1.0 normative candidate, not a stable release, until every
mandatory item in `STABILITY_GATE_AUDIT.md` is PASS.

Changing or deleting an unmet gate solely to obtain a stable label is a claims
failure.
