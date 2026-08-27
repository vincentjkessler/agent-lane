# Agent Lane Protocol 1.0 Candidate — Evidence Status

## Current stability state

| Gate | Status | Evidence |
|---|---:|---|
| `SG-03` Live Drive Adapter 001 | **PASS** | Real Windows Receiver + Google Drive activation + authorized effect + independent verifier + immutable receipt |
| `SG-04` Second materially different real adapter | **PASS** | Local Folder Adapter 002 and live Google Drive sync-folder adapter: 7/7 normalized semantic equivalence |
| `SG-06` Outside implementation/review | **BLOCKED** | No attributable outside technical review has yet been preserved |

Therefore:

`ALP 1.0 Stable = NOT YET`

## SG-03 summary

Live probe ID:
`alp-sg03-drive-live-20260826T135708Z-953f9f5f`

Observed live path:

```text
Google Drive object/activation
→ Windows Receiver windows-agent-lane-01
→ authorized workspace-write
→ actual project verifier
→ immutable provider-side receipt
```

Key identities:

- artifact SHA-256: `b19ffefd7c6de93542dbfe627c65250d06e606893da44797b007b080b033d3d7`
- pre-authored marker SHA-256: `f98d9605d3016a9fb83ab56da01ed8fa2885e90fbf8f7f3d61940b922b4f0978`
- receipt final effect SHA-256: `f98d9605d3016a9fb83ab56da01ed8fa2885e90fbf8f7f3d61940b922b4f0978`
- independent verifier: `agent-lane-core-conformance`
- verifier result: `85/85 PASS`
- SG-03 evidence bundle SHA-256: `e7302401718fc752f2bba4e44a6f8397bef3b31460b19df3bea57166e3fcb2f1`

## SG-04 summary

Real adapters:

1. `local-folder-reference-002` — `LOCAL_DURABLE`
2. `google-drive-sync-folder` — `REMOTE_DURABLE`, Windows Receiver + Google Drive for Desktop synchronized root

Normalized vectors:

- TA-V001 happy publication — equivalent
- TA-V002 verifier failure/rollback — equivalent
- TA-V003 stale authority — equivalent
- TA-V004 worker exception — equivalent
- TA-V005 duplicate delivery/idempotency — equivalent
- TA-V006 restart/re-instantiation persistence — equivalent
- TA-V007 transport integrity/tamper — equivalent

Result: **7/7 semantic equivalence**.

Latest live core verifier during SG-04: `88/88 PASS`.

SG-04 evidence bundle SHA-256:
`2c3fd6e8240b299f37bc0e2274b1d7c4679088c4ff607bbbdb44ce7a49a8e8f9`

Important boundary: the live Drive adapter uses Google Drive for Desktop's synchronized filesystem semantics. It is a real remote-backed transport, but it is not represented as a direct Drive REST implementation.

## Internal candidate evidence

- internal unit tests: `368/368 PASS`
- normative candidate audit: `18/18 PASS`
- adversarial RC: `ADVERSARIAL_RC_PASS`
- v0.18 engineering RC freeze SHA-256: `ab29be6c5de8ef8147e1cc7327fae105e80ed6f8a8a4667fb1b11f1321a8e55d`
- v1 candidate freeze SHA-256: `cd0119c4cd4cb24035bb9e7b375747961ba36f1be93e8da40757559190c6c8dd`
- normative document set SHA-256: `b46365ee97c1797f8872a2cbee51b15e604cb680183db41afec205fc8525ce0c`
- candidate schema set SHA-256: `ea5e435e5e237155e897b7285623d97e4db85b00825b19c04aa956466251407b`

## Evidence boundaries

The candidate does **not** claim:

- live multi-provider API conformance;
- outside third-party implementation adoption yet;
- HSM-grade or Windows CNG custody;
- globally trusted signing/witness infrastructure;
- universal exactly-once side effects;
- distributed consensus;
- novelty, patentability or freedom to operate;
- ALP 1.0 stable status before SG-06 is satisfied and the frozen audit is rerun.
