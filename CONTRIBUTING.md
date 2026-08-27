# Contributing

Agent Lane is in alpha. Contributions that improve the public protocol, reference surface, evidence quality, and core handoff semantics are preferred over broad feature expansion.

## Repository scope

This repository is the public protocol/community/reference surface. It is **not** the default destination for the complete production Agent Lane implementation.

Do not submit production Receiver/runtime source, Test Center/workbench internals, operational recovery machinery, deployment/configuration internals, security-sensitive integration details, or other proprietary production implementation material unless that component has first been deliberately approved for public release.

See [`docs/PUBLICATION-BOUNDARY.md`](docs/PUBLICATION-BOUNDARY.md).

## Before opening a PR

1. State the human testing friction or protocol ambiguity being addressed.
2. Describe the failure mode if the change is wrong.
3. Include a reproducible verification path.
4. Preserve the isolated-copy/live-state boundary.
5. Avoid introducing a model-vendor dependency unless the feature is explicitly adapter-scoped.
6. Confirm that the material belongs inside the declared public publication boundary.

For behavior changes, include before/after evidence when practical.
