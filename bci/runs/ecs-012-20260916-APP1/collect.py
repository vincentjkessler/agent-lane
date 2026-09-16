import hashlib, json, os
from pathlib import Path

ROOT = Path('bci/runs/ecs-012-20260916-APP1')
MAP = Path('bci/emergent-capability-surface/map.json')


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest_bytes(data: bytes):
    return hashlib.sha256(data).hexdigest()

raw = MAP.read_bytes()
capmap = json.loads(raw)
confirmed = capmap.get('confirmed', [])
candidates = capmap.get('candidates', [])

confirmed_view = []
for item in confirmed:
    entry = {'id': item['id'], 'name': item['name'], 'status': item['status']}
    if 'evidence' in item:
        entry['evidence'] = item['evidence']
    if 'evidence_note' in item:
        entry['evidence_note'] = item['evidence_note']
    if 'boundary' in item:
        entry['boundary'] = item['boundary']
    confirmed_view.append(entry)

candidate_view = [
    {'id': x['id'], 'name': x['name'], 'status': x['status']}
    for x in candidates
]

payload = {
    'schema': 'ecs-012-analysis/v1',
    'experiment_id': 'ECS-012-20260916-APP1',
    'source_map_updated_at': capmap.get('updated_at'),
    'source_map_sha256': digest_bytes(raw),
    'confirmed_count': len(confirmed_view),
    'candidate_count': len(candidate_view),
    'confirmed': confirmed_view,
    'candidates': candidate_view,
    'confirmed_ids': [x['id'] for x in confirmed_view],
    'candidate_ids': [x['id'] for x in candidate_view],
    'boundaries': [
        {'id': x['id'], 'boundary': x['boundary']}
        for x in confirmed_view if 'boundary' in x
    ],
    'legacy_without_evidence_field': [
        x['id'] for x in confirmed_view
        if 'evidence' not in x and 'evidence_note' in x
    ],
}
payload['analysis_sha256'] = hashlib.sha256(canonical(payload).encode()).hexdigest()
(ROOT / 'analysis.json').write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')

state = json.loads((ROOT / 'state.json').read_text())
if state.get('status') != 'WAITING_FOR_STAGE1_TRIGGER':
    raise SystemExit('state is not waiting for stage 1')
state.update({
    'status': 'AWAITING_HUMAN_STEER',
    'stage': 1,
    'analysis_sha256': payload['analysis_sha256'],
    'source_map_sha256': payload['source_map_sha256'],
    'allowed_steers': ['CONSERVATIVE', 'FRONTIER'],
    'stage1_workflow_run_id': os.environ.get('GITHUB_RUN_ID'),
})
(ROOT / 'state.json').write_text(json.dumps(state, indent=2, sort_keys=True) + '\n')
print('ECS012_STAGE1=' + canonical({'confirmed_count': len(confirmed_view), 'candidate_count': len(candidate_view), 'analysis_sha256': payload['analysis_sha256'], 'status': state['status']}))
