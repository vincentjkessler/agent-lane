# Architecture

Agent Lane is organized around the human testing handoff rather than around a particular model vendor or IDE.

## Functional path

1. **Receive** — accept a task from the upstream AI workflow.
2. **Resolve** — identify product, repository, task identity, and intended test target.
3. **Isolate** — create or select a safe working copy for the task.
4. **Execute** — apply the task through the configured worker/toolchain.
5. **Verify** — run machine checks and retain evidence.
6. **Route** — open or reuse the correct product-specific browser surface.
7. **Present** — show the human the isolated task and the controls necessary to test it.
8. **Tweak** — permit bounded changes without destroying the test context.
9. **Settle** — persist approve/reject/needs-tweak state and verification receipts.
10. **Continue** — allow later work to proceed while the human is testing earlier work.

## Design rule

The Test Center is the primary human surface. Additional Lane UI should earn its existence by making the test loop faster, safer, or easier to recover.

## Safety boundary

The test copy and live product must have an explicit boundary. A failure in task execution, browser rendering, optional visual assets, or a tweak must not silently mutate production state.

## Hard dependency

The architecture only matters if a new user can complete the loop without author coaching. That user test outranks feature count.
