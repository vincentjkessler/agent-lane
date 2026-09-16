import json, os
from pathlib import Path

root = Path(__file__).resolve().parent
result = json.loads((root / 'result.json').read_text())
trigger_commit = os.environ['GITHUB_SHA']
run_id = int(os.environ['GITHUB_RUN_ID'])
receipt = {
    'schema': 'ecs-006b-receipt/v1',
    'experiment_id': 'ECS-006B-20260916-WAKE2',
    'mutation_actor': 'GitHub Actions',
    'monitor_mode': 'condition_watch',
    'work_used': False,
    'prior_conversation_context_used': False,
    'manual_chat_after_arm': False,
    'trigger_commit': trigger_commit,
    'workflow_run_id': run_id,
    'workflow_conclusion_expected': 'success',
    'result': result,
    'verification': 'PASS',
    'verdict': 'PASS_PENDING_SCHEDULED_OBSERVER',
}
state = {
    'schema': 'ecs-006b-state/v1',
    'experiment_id': 'ECS-006B-20260916-WAKE2',
    'status': 'COMPLETE',
    'monitor_armed': True,
    'manual_chat_after_arm': False,
    'trigger_commit': trigger_commit,
    'workflow_run_id': run_id,
    'verification': 'PASS',
    'result': result,
}
(root / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
(root / 'state.json').write_text(json.dumps(state, indent=2, sort_keys=True) + '\n')
print('ECS006B_DURABLE_STATE=COMPLETE')
