import json, os
from pathlib import Path

ROOT = Path('bci/runs/ccs-015-20260916-BASE1')
REPO = Path('.')
REFERENCE = Path('bci/runs/ecs-012-20260916-APP1/release.json')


def impl_loc(path):
    count = 0
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        count += 1
    return count

baseline = json.loads((ROOT / 'baseline_release.json').read_text())
reference = json.loads(REFERENCE.read_text())
exact_semantic_match = baseline == reference

ccs_files = [
    'bci/runs/ecs-012-20260916-APP1/collect.py',
    'bci/runs/ecs-012-20260916-APP1/render.py',
    'bci/runs/ecs-012-20260916-APP1/verify.py',
    '.github/workflows/ecs-012-applicationless.yml',
]
baseline_files = [
    'bci/runs/ccs-015-20260916-BASE1/baseline.py',
    '.github/workflows/ccs-015-conventional-baseline.yml',
]

metrics = {
    'schema': 'ccs-015-comparison/v1',
    'experiment_id': 'CCS-015-20260916-BASE1',
    'task': 'Reproduce the CCS-012 FRONTIER release from the same historical source map',
    'output_exact_semantic_match': exact_semantic_match,
    'reference_release_sha256': reference.get('release_sha256'),
    'baseline_release_sha256': baseline.get('release_sha256'),
    'compositional': {
        'implementation_files': len(ccs_files),
        'implementation_loc': sum(impl_loc(x) for x in ccs_files),
        'files': ccs_files,
        'required_successful_workflow_stages': 2,
        'observed_workflow_attempts': 3,
        'policy_decision_events_required': 1,
        'explicit_durable_human_interrupt': True,
        'independent_runtime_verifier': True,
        'observed_adapter_fault_rejected': True,
    },
    'conventional_baseline': {
        'implementation_files': len(baseline_files),
        'implementation_loc': sum(impl_loc(x) for x in baseline_files),
        'files': baseline_files,
        'required_successful_workflow_stages': 1,
        'observed_workflow_attempts': 1,
        'policy_decision_events_required': 1,
        'explicit_durable_human_interrupt': False,
        'independent_runtime_verifier': False,
        'lab_comparator_verifies_final_output': True,
        'workflow_run_id': os.environ.get('GITHUB_RUN_ID'),
    },
}

b = metrics['conventional_baseline']
c = metrics['compositional']
if not exact_semantic_match:
    verdict = 'BASELINE_FAILED_TO_REPRODUCE_OUTPUT'
elif b['implementation_files'] < c['implementation_files'] and b['implementation_loc'] < c['implementation_loc'] and b['required_successful_workflow_stages'] < c['required_successful_workflow_stages']:
    verdict = 'CONVENTIONAL_AUTOMATION_SIMPLER_FOR_THIS_DETERMINISTIC_TASK'
else:
    verdict = 'NO_CLEAR_SIMPLICITY_WINNER'
metrics['verdict'] = verdict
(ROOT / 'comparison.json').write_text(json.dumps(metrics, indent=2, sort_keys=True) + '\n')

lines = [
    '# CCS-015 Comparative Baseline Result',
    '',
    f'Verdict: **{verdict}**',
    '',
    f'- Exact semantic output match: `{str(exact_semantic_match).lower()}`',
    f'- Compositional implementation: {c["implementation_files"]} files, {c["implementation_loc"]} nonblank/noncomment LOC, {c["required_successful_workflow_stages"]} required workflow stages, {c["observed_workflow_attempts"]} observed attempts.',
    f'- Conventional baseline: {b["implementation_files"]} files, {b["implementation_loc"]} nonblank/noncomment LOC, {b["required_successful_workflow_stages"]} required workflow stage, {b["observed_workflow_attempts"]} observed attempt.',
    '- Both require one human policy decision conceptually.',
    '- The compositional version uniquely provides an explicit durable human interrupt/resume point and an independent runtime verifier.',
    '- For this deterministic transformation, those extra properties are not required to obtain the final release output and therefore are treated as added machinery, not automatic practical advantage.',
    '',
    '## Interpretation',
    '',
    'This experiment is a calibration result. If the conventional baseline is simpler while reproducing the same output, the lab should not use deterministic release transformation as evidence that composition is superior. Future comparative tests should target tasks where semantic adaptation, cold continuation, changing requirements, or recovery are actually needed.',
    '',
]
(ROOT / 'CONCLUSION.md').write_text('\n'.join(lines))
print('CCS015_COMPARE=' + json.dumps({'verdict': verdict, 'exact_match': exact_semantic_match}, sort_keys=True))
if not exact_semantic_match:
    raise SystemExit(1)
