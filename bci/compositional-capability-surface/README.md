# Compositional Capability Surface (CCS)

## Lab

**Capability Composition Laboratory (CCL)**

## Thesis

Ordinary consumer ChatGPT exposes a larger compositional systems surface than its individual product features suggest. By combining reasoning, persistent state, connected systems, hosted execution, verification, scheduling, and human control, it can participate in higher-order application-like workflows without requiring a custom agent runtime around every workflow.

This is a systems-engineering claim, not a claim of a newly emergent model capability.

## Research question

Given a fixed set of documented primitives, what higher-order operational behaviors become reachable through composition, what measurable value do those compositions add over simpler alternatives, and where are the product/safety/reliability boundaries?

## Rename from ECS

The earlier name **Emergent Capability Surface (ECS)** is retired because it can imply model-level emergence. Historical evidence remains under `bci/emergent-capability-surface/` and experiment paths using `ecs-*`; those artifacts are immutable historical records.

From this point forward:

- Surface: **Compositional Capability Surface (CCS)**
- Lab: **Capability Composition Laboratory (CCL)**
- New experiment IDs use `CCS-*`.
- Historical `ECS-*` identifiers are preserved as aliases in the canonical CCS map.

## Promotion standard

A capability is promoted only after a controlled, reproducible test with durable evidence and explicit boundaries. A composition is not considered interesting merely because it can be built; comparative value against a simpler baseline is now a first-class requirement.

## Comparative dimensions

New experiments should measure, where applicable:

1. task success and output correctness;
2. human interventions and manual transfer steps;
3. custom orchestration code/configuration required;
4. recovery behavior after faults or interruptions;
5. persistence/cold-resume burden;
6. time-to-useful-result;
7. generalization across task or substrate changes;
8. permission and safety boundaries.

The lab is specifically trying to identify where composition provides real leverage versus where a conventional script, workflow engine, or ordinary single ChatGPT conversation is simpler and better.
