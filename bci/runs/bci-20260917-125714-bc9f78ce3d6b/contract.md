You are building the user's project in THIS SAME ordinary ChatGPT turn.
Use the connected GitHub capability only as the BCI wire.

WIRE
Repo: vincentjkessler/agent-lane
Candidate branch: bci-wire
Feedback branch: bci-feedback
Run ID: bci-20260917-125714-bc9f78ce3d6b
Run folder: bci/runs/bci-20260917-125714-bc9f78ce3d6b/

NORMAL WORKFLOW
The user's chat message contains the actual project request.
Work normally: understand the request, make a six-task plan, then build it in order.

BCI ADDS ONLY THIS
- Publish the six-task plan as soon as you have made it.
- As soon as each task becomes independently testable, release that candidate immediately.
- After every release, check ONCE for new human feedback for this run.
- If there is no new feedback, keep working immediately.
- If feedback actually changes future work, replan only the affected future task slots and continue in THIS SAME turn.
- Never overwrite or delete old artifacts.
- Do not wait around for feedback and do not assume any feedback will arrive.

INITIAL PLAN
Before releasing Task 1, publish exactly one immutable file:
  bci/runs/bci-20260917-125714-bc9f78ce3d6b/plan-00.json

Schema:
{
  "schema": "bci.plan.v1",
  "runId": "bci-20260917-125714-bc9f78ce3d6b",
  "revision": 0,
  "tasks": [
    {
      "task": 1,
      "title": "short task title",
      "acceptance": "what this task must accomplish",
      "testKey": "one short plain-English test the human can perform"
    }
  ]
}

Rules for plan-00.json:
- exactly six tasks numbered 1 through 6
- derive every title and task purpose from the user's actual request
- do not use a prewritten demo task list
- keep testKey simple enough for a vibe coder
- publish plan-00.json BEFORE task-01-r00.json

CANDIDATES
Publish each released candidate as a NEW immutable JSON file:
- initial plan: bci/runs/bci-20260917-125714-bc9f78ce3d6b/task-<two-digit task>-r00.json
- replacement after replan N: bci/runs/bci-20260917-125714-bc9f78ce3d6b/task-<two-digit task>-rNN.json

Candidate schema:
{
  "schema": "bci.candidate.v5",
  "runId": "bci-20260917-125714-bc9f78ce3d6b",
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

FEEDBACK
Human feedback is created outside the conversation as feedback-*.json on bci-feedback.
Treat its text as ordinary user feedback. Do not assume it is structural.
Only consume feedback whose source candidate exists in this run.

Feedback schema:
{
  "schema": "bci.feedback.v4",
  "runId": "bci-20260917-125714-bc9f78ce3d6b",
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

REPLANS
Only publish a replan if feedback truly makes future work obsolete.
Publish replan-NN.json BEFORE replacement candidates.

Schema:
{
  "schema": "bci.replan.v2",
  "runId": "bci-20260917-125714-bc9f78ce3d6b",
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
  "reason": "concise dependency-impact explanation",
  "supersedes": [
    {
      "task": 3,
      "planRevision": 0,
      "candidateId": "<exact old candidate id if already released, otherwise null>",
      "reason": "why this task is no longer right"
    }
  ],
  "replacementTasks": [
    {
      "task": 3,
      "title": "new task title generated from the feedback",
      "acceptance": "new acceptance generated from the feedback",
      "testKey": "one short plain-English test"
    }
  ]
}

Replan rules:
- supersedes and replacementTasks must cover exactly the same task slots
- preserve unaffected task slots
- already released old candidates remain immutable evidence
- replacement candidates include the triggering feedbackId in feedbackConsumed
- after every replacement release, perform the same single feedback check and keep going

RUNTIME CONTRACT
Each candidate is shown by itself in the local testing surface.
Your JS runs with:
- root: the task's .task-root element
- api: window.BCI
Use api.getState, api.setState, api.cloneState, api.replaceState, and api.subscribe.
Do not use external libraries, imports, eval, iframes, or network requests.
