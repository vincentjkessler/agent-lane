import hashlib
import json
from pathlib import Path

root = Path('bci/runs/ccs-016-20260916-ADAPT1')
items = json.loads((root / 'input/releases.json').read_text())['items']
policy = json.loads((root / 'compositional/policy.json').read_text())
out = root / 'compositional/output'
out.mkdir(parents=True, exist_ok=True)

def matches(test, item):
    if 'all' in test:
        return all(matches(x, item) for x in test['all'])
    if 'any' in test:
        return any(matches(x, item) for x in test['any'])
    field = test['field']
    actual = item.get(field)
    op = test['op']
    expected = test.get('value')
    if op == 'eq':
        return actual == expected
    if op == 'in':
        return actual in expected
    raise ValueError(op)

rows = []
for item in items:
    decision = policy['default_decision']
    for rule in policy['rules']:
        if matches(rule['when'], item):
            decision = rule['decision']
            break
    rows.append({'id': item['id'], 'decision': decision})

rank = {name: i for i, name in enumerate(policy['decision_order'])}
rows.sort(key=lambda row: (rank[row['decision']], row['id']))
counts = {name: sum(row['decision'] == name for row in rows) for name in policy['decision_order']}
report = {'schema':'ccs-016-report/v1','policy':policy['policy_id'],'items':rows,'counts':counts}
canonical = json.dumps(report, sort_keys=True, separators=(',', ':'))
report['digest'] = hashlib.sha256(canonical.encode()).hexdigest()
(out / 'report.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
md = ['# Release Readiness', '', f"APPROVE: {counts.get('APPROVE', 0)}", f"HOLD: {counts.get('HOLD', 0)}", '']
md += [f"- {row['id']}: {row['decision']}" for row in rows]
md += ['', f"Digest: `{report['digest']}`", '']
(out / 'report.md').write_text('\n'.join(md))
