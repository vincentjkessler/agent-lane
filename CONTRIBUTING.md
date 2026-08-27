# Contributing

Agent Lane is in alpha. Contributions that improve the core handoff loop are preferred over broad feature expansion.

## Before opening a PR

1. State the human testing friction being removed.
2. Describe the failure mode if the change is wrong.
3. Include a reproducible verification path.
4. Preserve the isolated-copy/live-state boundary.
5. Avoid introducing a model-vendor dependency unless the feature is explicitly adapter-scoped.

For behavior changes, include before/after evidence when practical.
