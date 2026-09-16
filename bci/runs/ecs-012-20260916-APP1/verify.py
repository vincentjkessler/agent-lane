import hashlib, json, sys
from pathlib import Path

ROOT = Path('bci/runs/ecs-012-20260916-APP1')
MAP = Path('bci/emergent-capability-surface/map.json')


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def sha_obj_without(obj, key):
    tmp = dict(obj)
    tmp.pop(key, None)
    return hashlib.sha256(canonical(tmp).encode()).hexdigest()


def expected_analysis():
    raw = MAP.read_bytes()
    capmap = json.loads(raw)
    confirmed = []
    for item in capmap.get('confirmed', []):
        entry = {'id': item['id'], 'name': item['name'], 'status': item['status']}
        for k in ('evidence', 'evidence_note', 'boundary'):
            if k in item:
                entry[k] = item[k]
        confirmed.append(entry)
    candidates = [
        {'id': x['id'], 'name': x['name'], 'status': x['status']}
        for x in capmap.get('candidates', [])
    ]
    obj = {
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
    obj['analysis_sha256'] = hashlib.sha256(canonical(obj).encode()).hexdigest()
    return obj

stage = sys.argv[1] if len(sys.argv) > 1 else ''
analysis = json.loads((ROOT / 'analysis.json').read_text())
exp = expected_analysis()
if analysis != exp:
    raise SystemExit('analysis mismatch')
if analysis['analysis_sha256'] != sha_obj_without(analysis, 'analysis_sha256'):
    raise SystemExit('analysis digest mismatch')
state = json.loads((ROOT / 'state.json').read_text())

if stage == 'stage1':
    if state.get('status') != 'AWAITING_HUMAN_STEER' or state.get('stage') != 1:
        raise SystemExit('stage1 state mismatch')
    if state.get('analysis_sha256') != analysis['analysis_sha256']:
        raise SystemExit('state analysis digest mismatch')
    if state.get('human_interrupt_applied') is not False:
        raise SystemExit('human interrupt was applied too early')
    if (ROOT / 'release.json').exists() or (ROOT / 'ECL_STATUS.md').exists():
        raise SystemExit('stage2 artifacts exist before human steer')
    print('ECS012_VERIFY_STAGE1=PASS')
    raise SystemExit(0)

if stage != 'stage2':
    raise SystemExit('expected stage1 or stage2')

steer = json.loads((ROOT / 'steer.json').read_text())
choice = steer.get('choice')
if choice not in ('CONSERVATIVE', 'FRONTIER'):
    raise SystemExit('invalid steer')
release = json.loads((ROOT / 'release.json').read_text())
expected_release = {
    'schema': 'ecs-012-release/v1',
    'experiment_id': 'ECS-012-20260916-APP1',
    'selected_policy': choice,
    'generated_from_analysis_sha256': analysis['analysis_sha256'],
    'source_map_sha256': analysis['source_map_sha256'],
    'confirmed_count': analysis['confirmed_count'],
    'confirmed': analysis['confirmed'],
    'boundaries': analysis['boundaries'],
    'candidates_included': choice == 'FRONTIER',
}
if choice == 'FRONTIER':
    expected_release['candidate_count'] = analysis['candidate_count']
    expected_release['candidates'] = analysis['candidates']
expected_release['release_sha256'] = hashlib.sha256(canonical(expected_release).encode()).hexdigest()
if release != expected_release:
    raise SystemExit('release mismatch')
if release['release_sha256'] != sha_obj_without(release, 'release_sha256'):
    raise SystemExit('release digest mismatch')

lines = [
    '# Emergent Capability Laboratory — Verified Status',
    '',
    f'Policy: **{choice}**',
    f'Confirmed capabilities: **{analysis["confirmed_count"]}**',
    '',
    '## Confirmed',
    '',
]
for item in analysis['confirmed']:
    lines.append(f'- **{item["id"]} — {item["name"]}**: {item["status"]}')
    if item.get('boundary'):
        lines.append(f'  - Boundary: {item["boundary"]}')
if choice == 'FRONTIER':
    lines += ['', '## Candidate frontier', '']
    for item in analysis['candidates']:
        lines.append(f'- **{item["id"]} — {item["name"]}**: {item["status"]}')
else:
    lines += ['', 'Candidate details omitted by CONSERVATIVE publication policy.']
lines += [
    '',
    '## Verification',
    '',
    f'- Analysis SHA-256: `{analysis["analysis_sha256"]}`',
    f'- Release SHA-256: `{release["release_sha256"]}`',
    '- Human interrupt applied: `true`',
    '',
]
expected_md = '\n'.join(lines)
if (ROOT / 'ECL_STATUS.md').read_text() != expected_md:
    raise SystemExit('status markdown mismatch')
if state.get('status') != 'COMPLETE' or state.get('stage') != 2:
    raise SystemExit('final state mismatch')
if state.get('human_interrupt_applied') is not True:
    raise SystemExit('human interrupt not recorded')
if state.get('selected_steer') != choice:
    raise SystemExit('selected steer mismatch')
if state.get('release_sha256') != release['release_sha256']:
    raise SystemExit('state release digest mismatch')
print('ECS012_VERIFY_STAGE2=PASS')
