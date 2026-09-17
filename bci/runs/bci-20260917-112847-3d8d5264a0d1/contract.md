We are building one integrated project-management application in THIS SAME ordinary ChatGPT turn.
Use the connected GitHub capability as the wire.

WIRE
Repo: vincentjkessler/agent-lane
Candidate branch: bci-wire
Feedback branch: bci-feedback
Run ID: bci-20260917-112847-3d8d5264a0d1
Run folder: bci/runs/bci-20260917-112847-3d8d5264a0d1/

WHAT TO DO
Build the six tasks below in order.
As soon as one task is good enough to test by itself:
1. release it immediately as a new candidate JSON on the candidate branch
2. check ONCE for any new feedback-*.json for this run on the feedback branch
3. if there is no new feedback, continue immediately
4. if feedback changes future work, publish the next replan-NN.json first, replace only the affected future task slots, and keep going in this SAME turn

IMPORTANT
- Do NOT wait around for feedback.
- Do NOT assume feedback will arrive.
- Do NOT overwrite old candidate files.
- Old candidates remain immutable evidence.
- Human test copy must be plain English for a vibe coder.

CANDIDATE FILE
Publish a NEW JSON file for each released task:
- initial plan: bci/runs/bci-20260917-112847-3d8d5264a0d1/task-<two-digit task>-r00.json
- replacement after replan N: bci/runs/bci-20260917-112847-3d8d5264a0d1/task-<two-digit task>-rNN.json

Candidate schema:
{
  "schema": "bci.candidate.v5",
  "runId": "bci-20260917-112847-3d8d5264a0d1",
  "task": 1,
  "planRevision": 0,
  "candidateId": "t1-r0-<short unique suffix>",
  "title": "short title",
  "html": "<HTML fragment for that task only>",
  "css": "<CSS for that task only>",
  "js": "<JavaScript body for that task only>",
  "feedbackConsumed": []
}
Do not wrap JSON in markdown fences.

FEEDBACK FILES
Human feedback is created outside this conversation as feedback-*.json files on bci-feedback.
Validate runId, feedbackId, sourceTask, sourceCandidateId, sourcePlanRevision, text, createdAt, and nonce.
Treat the feedback text as ordinary human direction.
Do not assume it is structural.

Feedback schema:
{
  "schema": "bci.feedback.v4",
  "runId": "bci-20260917-112847-3d8d5264a0d1",
  "feedbackId": "fb-001-<unique>",
  "sequence": 1,
  "sourceTask": 2,
  "sourceCandidateId": "<exact candidate>",
  "sourcePlanRevision": 0,
  "kind": "CHANGE_REQUEST",
  "text": "the human's actual requested change",
  "createdAt": "<ISO>",
  "nonce": "<unique>"
}

REPLAN FILES
Only publish a replan file if feedback really changes future work.
Publish it BEFORE any replacement candidates.
Use:
- bci/runs/bci-20260917-112847-3d8d5264a0d1/replan-01.json
- bci/runs/bci-20260917-112847-3d8d5264a0d1/replan-02.json
- ...

Replan schema:
{
  "schema": "bci.replan.v2",
  "runId": "bci-20260917-112847-3d8d5264a0d1",
  "revision": 1,
  "parentRevision": 0,
  "triggeredBy": {
    "feedbackId": "<exact feedbackId>",
    "sequence": 1,
    "sourceTask": 2,
    "sourceCandidateId": "<exact sourceCandidateId>",
    "sourcePlanRevision": 0,
    "text": "<exact feedback text>",
    "createdAt": "<copy>",
    "nonce": "<copy>"
  },
  "reason": "why the old downstream work is no longer correct",
  "supersedes": [
    {
      "task": 3,
      "planRevision": 0,
      "candidateId": "<exact old candidate id or null>",
      "reason": "why this task is obsolete"
    }
  ],
  "replacementTasks": [
    {
      "task": 3,
      "title": "new task title",
      "acceptance": "new acceptance generated from the feedback",
      "testKey": "one short plain-English test"
    }
  ]
}
replacementTasks must cover exactly the same task slots as supersedes.
Each replacement candidate must include the triggering feedbackId in feedbackConsumed.

RUNTIME CONTRACT
Each candidate is shown by itself in the local testing surface.
Your JS runs with:
- root: the task's .task-root element
- api: window.BCI
Use api.getState, api.setState, api.cloneState, api.replaceState, and api.subscribe.
Do not use external libraries, imports, eval, iframes, or network requests.

SIX-TASK PLAN
1. PROJECT FOUNDATION
Build the shared project-management foundation.
Need: exactly three project cards, visible project status badges, visible project/open-task metrics, and a working active-project selection.
Test: Click RoomForge, then Ravenhurst. If the highlight follows your clicks, it works.

2. PROJECT WORKSPACE
Build the active-project workspace.
Need: active project name, Overview/Tasks/Notes navigation, working section switching, live shared tasks, live notes.
Test: Switch between Overview, Tasks, and Notes. If each view changes and the project name stays clear, it works.

3. SEARCH AND FILTER WORK
Build the shared task work queue.
Need: live text search, status filter, owner filter, title/due sorting, result count, Clear Filters, shared-state updates.
Test: Search, change one filter, then clear it. If the list reacts each time, it works.

4. TASK EDITING
Build a working task editor.
Need: create and edit title, owner, status, due date; reject blank title visibly; keep the visible list current.
Test: Edit one task, change its status, and save it. If the row updates right away, it works.

5. SAVE AND RESTORE
Build snapshot persistence.
Need: Save Snapshot, Restore Snapshot, Clear Saved State, Undo Last Change.
Test: Save, change something, then Restore. If the saved version comes back, it works.

6. INTEGRATION CHECK
Build a self-contained diagnostics panel.
Need: at least eight real checks over the shared state and current project/task data.
Test: Look over the checks. If they are green and the counts look right, it works.
