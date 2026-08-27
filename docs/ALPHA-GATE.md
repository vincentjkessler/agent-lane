# Agent Lane Alpha Gate

The alpha gate is intentionally narrower than the long-term Lane roadmap.

## Hard dependency

A person who did not build Lane must be able to send one task and, without coaching from the author, reach the correct Test Center, understand what changed, test it, make a tweak, and finish the task.

If this fails, the alpha fails regardless of website polish, payments, or additional UI.

## Required

- [ ] Task arrives automatically.
- [ ] Product identity is resolved correctly.
- [ ] Work happens against an isolated copy; live state is not mutated by the test task.
- [ ] A new product opens the correct test browser.
- [ ] An already-open product receives the new task in that browser with visible notification.
- [ ] The Test Center exposes the current task prominently and suppresses unrelated task noise.
- [ ] Critical controls needed to exercise the change are present.
- [ ] The user can make a tweak and preview it against the isolated copy.
- [ ] Approve / reject / needs-tweak state persists.
- [ ] A verification receipt is attached to settlement.
- [ ] Failure states show a concrete recovery action.

## Explicitly not required for alpha

- complete final Lane UI
- support for every project type
- elaborate analytics dashboards
- full commercial account system
- every future governance feature
- every proof product integrated

## Alpha decision

Launch only when the required list passes end-to-end from a clean-user perspective.
