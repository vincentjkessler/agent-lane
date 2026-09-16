# ECS-003 / ECS-004 Phase 3 — Cold-start instruction

Use only this pointer as the operational starting point:

`vincentjkessler/agent-lane@bci-wire:bci/runs/ecs-20260916-0634/state.json`

Treat the external state referenced by that pointer as authoritative. Do not rely on prior conversation history or remembered task details. Resume the experiment's next action, minimize retrieval to only what the external state says is necessary, and write a Phase 3 receipt back under the experiment root if the available GitHub connection permits it.

Report the selected continuation operation, the files actually retrieved, and whether ECS-003 and ECS-004 satisfy their acceptance criteria. Do not mark either capability confirmed if the external state is insufficient or if hidden prior context is required.
