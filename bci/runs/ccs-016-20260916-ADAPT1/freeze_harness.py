import hashlib, json, os
from pathlib import Path

root = Path('bci/runs/ccs-016-20260916-ADAPT1')
if (root / 'disruption.md').exists() or (root / 'disruption.json').exists():
    raise SystemExit('disruption exists before freeze')
items = json.loads((root / 'input/releases.json').read_text())['items']

rows=[]
for item in items:
    ok = item['tests_passed'] is True and item['security_review']=='pass' and item['rollback_ready'] is True
    rows.append({'id':item['id'],'decision':'APPROVE' if ok else 'HOLD'})
rank={'APPROVE':0,'HOLD':1}
rows.sort(key=lambda x:(rank[x['decision']],x['id']))
expected={'schema':'ccs-016-report/v1','policy':'initial-v1','items':rows,'counts':{'APPROVE':sum(x['decision']=='APPROVE' for x in rows),'HOLD':sum(x['decision']=='HOLD' for x in rows)}}
raw=json.dumps(expected,sort_keys=True,separators=(',',':'))
expected['digest']=hashlib.sha256(raw.encode()).hexdigest()

conv=json.loads((root/'conventional/output/report.json').read_text())
comp=json.loads((root/'compositional/output/report.json').read_text())
if conv != expected: raise SystemExit('conventional initial output mismatch')
if comp != expected: raise SystemExit('compositional initial output mismatch')
if conv != comp: raise SystemExit('initial outputs differ')

lane_files={
  'conventional':['conventional/baseline.py'],
  'compositional':['compositional/engine.py','compositional/policy.json']
}
def sha(path): return hashlib.sha256((root/path).read_bytes()).hexdigest()
def loc(path):
    if not path.endswith('.py'): return sum(1 for line in (root/path).read_text().splitlines() if line.strip())
    return sum(1 for line in (root/path).read_text().splitlines() if line.strip() and not line.lstrip().startswith('#'))
freeze={
 'schema':'ccs-016-freeze/v1',
 'experiment_id':'CCS-016-20260916-ADAPT1',
 'status':'FROZEN_AWAITING_HUMAN_DISRUPTION',
 'freeze_source_commit':os.environ.get('GITHUB_SHA'),
 'initial_report_digest':expected['digest'],
 'initial_outputs_semantically_identical':True,
 'disruption_present_at_freeze':False,
 'lanes':{}
}
for lane, paths in lane_files.items():
    freeze['lanes'][lane]={
      'files':paths,
      'file_sha256':{p:sha(p) for p in paths},
      'implementation_files':len(paths),
      'implementation_loc':sum(loc(p) for p in paths)
    }
(root/'freeze.json').write_text(json.dumps(freeze,indent=2,sort_keys=True)+'\n')
print('CCS016_FREEZE=' + json.dumps({'digest':expected['digest'],'status':freeze['status'],'conventional_loc':freeze['lanes']['conventional']['implementation_loc'],'compositional_loc':freeze['lanes']['compositional']['implementation_loc']},sort_keys=True,separators=(',',':')))
print('CCS016_VERIFY_INITIAL=PASS')
