import hashlib, json, os
from pathlib import Path

ROOT = Path('bci/runs/ecs-012-20260916-APP1')


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

analysis = json.loads((ROOT / 'analysis.json').read_text())
state = json.loads((ROOT / 'state.json').read_text())
steer = json.loads((ROOT / 'steer.json').read_text())
choice = steer.get('choice')

if state.get('status') != 'AWAITING_HUMAN_STEER':
    raise SystemExit('state is not awaiting human steer')
if choice not in ('CONSERVATIVE', 'FRONTIER'):
    raise SystemExit('invalid steer')

release = {
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
    release['candidate_count'] = analysis['candidate_count']
    release['candidates'] = analysis['candidates']

release['release_sha256'] = hashlib.sha256(canonical(release).encode()).hexdigest()
(ROOT / 'release.json').write_text(json.dumps(release, indent=2, sort_keys=True) + '\n')

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
(ROOT / 'ECL_STATUS.md').write_text('\n'.join(lines))

state.update({
    'status': 'COMPLETE',
    'stage': 2,
    'human_interrupt_applied': True,
    'selected_steer': choice,
    'release_sha256': release['release_sha256'],
    'stage2_workflow_run_id': os.environ.get('GITHUB_RUN_ID'),
})
(ROOT / 'state.json').write_text(json.dumps(state, indent=2, sort_keys=True) + '\n')
print('ECS012_RELEASE=' + canonical({'selected_policy': choice, 'release_sha256': release['release_sha256'], 'status': 'COMPLETE'}))
