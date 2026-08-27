# Agent Lane Publication Boundary

## Purpose

Agent Lane uses a split public/private development model during alpha.

The public `agent-lane` repository exists to make the protocol, semantics, evidence claims, external review path, and deliberately chosen reference material inspectable. It is not a standing authorization to publish the entire production implementation.

## Public by default

The following material belongs in the public repository unless a specific reason requires otherwise:

- ALP specification and normative schemas
- SG-06 external-review materials
- protocol conformance semantics
- architecture and conceptual documentation
- alpha acceptance criteria
- measurement methodology
- public evidence/status summaries
- issue and review workflows
- deliberately selected examples
- deliberately selected reference implementations, adapters, SDKs, or test fixtures

## Private by default

The following material stays outside this repository unless explicitly reviewed and approved for public release:

- production Windows Receiver/runtime source
- production workbench and Test Center internals
- production transport implementation details beyond what is required by the public protocol
- operational recovery machinery
- deployment, release, environment, and configuration internals
- credentials, secrets, private endpoints, private paths, machine-specific configuration, or security-sensitive material
- proprietary integration knowledge
- internal product orchestration that is not required to independently implement or review ALP
- implementation details under active IP/open-source-boundary review

## Release rule

Publishing a production component is a deliberate release decision, not a by-product of normal development.

Before moving a private-by-default component into the public repository, establish:

1. **Reason to publish** — interoperability, independent review, reference value, adoption, or another explicit purpose.
2. **IP decision** — confirm that public disclosure is intentional and consistent with the chosen IP strategy.
3. **Security review** — remove secrets, sensitive configuration, exploitable operational assumptions, and unnecessary internal topology.
4. **License decision** — state which license applies to the released component.
5. **Scope reduction** — publish only what is necessary for the stated purpose.
6. **Verification** — confirm that the public artifact reproduces the claimed behavior without relying on undisclosed accidental dependencies.

## Licensing boundary

The repository's MIT license applies to material actually released under that license in this repository. It does not create an obligation to publish unreleased Agent Lane production components.

## Architectural intent

The intended split is:

```text
agent-lane                  PUBLIC
├── protocol
├── schemas
├── architecture/docs
├── public evidence
├── external review
└── selected reference material

production implementation  PRIVATE BY DEFAULT
├── Receiver/runtime
├── workbench/Test Center
├── operational recovery
├── deployment/configuration
├── sensitive integrations
└── proprietary implementation knowledge
```

The boundary can move later. It should move only by deliberate decision.
