import hashlib, json
from pathlib import Path

ROOT = Path('bci/runs/ccs-015-20260916-BASE1')
SOURCE = ROOT / 'source-map.json'
POLICY = 'FRONTIER'


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

raw = SOURCE.read_bytes()
capmap = json.loads(raw)
confirmed = []
for item in capmap.get('confirmed', []):
    entry = {'id': item['id'], 'name': item['name'], 'status': item['status']}
    for key in ('evidence', 'evidence_note', 'boundary'):
        if key in item:
            entry[key] = item[key]
    confirmed.append(entry)
candidates = [{'id': x['id'], 'name': x['name'], 'status': x['status']} for x in capmap.get('candidates', [])]
analysis = {
    'schema': 'ecs-012-analysis/v1',
    'experiment_id': 'ECS-012-20260916-APP1',
    'source_map_updated_at': capmap.get('updated_at'),
    'source_map_sha256': hashlib.sha256(raw).hexdigest(),
    'confirmed_count': len(confirmed),
    'candidate_count': len(candidates),
    'confirmed': confirmed,
    'candidates': candidates,
    'confirmed_ids': [x['id'] for x in confirmed],
    'candidate_ids': [x['id'] for x in candidates],
    'boundaries': [{'id': x['id'], 'boundary': x['boundary']} for x in confirmed if 'boundary' in x],
    'legacy_without_evidence_field': [x['id'] for x in confirmed if 'evidence' not in x and 'evidence_note' in x],
}
analysis['analysis_sha256'] = hashlib.sha256(canonical(analysis).encode()).hexdigest()
release = {
    'schema': 'ecs-012-release/v1',
    'experiment_id': 'ECS-012-20260916-APP1',
    'selected_policy': POLICY,
    'generated_from_analysis_sha256': analysis['analysis_sha256'],
    'source_map_sha256': analysis['source_map_sha256'],
    'confirmed_count': analysis['confirmed_count'],
    'confirmed': analysis['confirmed'],
    'boundaries': analysis['boundaries'],
    'candidates_included': True,
    'candidate_count': analysis['candidate_count'],
    'candidates': analysis['candidates'],
}
release['release_sha256'] = hashlib.sha256(canonical(release).encode()).hexdigest()
(ROOT / 'baseline_release.json').write_text(json.dumps(release, indent=2, sort_keys=True) + '\n')
print('CCS015_BASELINE=' + canonical({'release_sha256': release['release_sha256'], 'policy': POLICY}))
