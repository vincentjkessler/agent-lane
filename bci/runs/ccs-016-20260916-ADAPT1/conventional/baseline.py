import hashlib, json
from pathlib import Path

ROOT = Path('bci/runs/ccs-016-20260916-ADAPT1')
DATA = json.loads((ROOT/'input/releases.json').read_text())['items']
OUT = ROOT/'conventional/output'
OUT.mkdir(parents=True, exist_ok=True)

rows=[]
for item in DATA:
    approve = item['tests_passed'] is True and item['security_review']=='pass' and item['rollback_ready'] is True
    rows.append({'id':item['id'],'decision':'APPROVE' if approve else 'HOLD'})
order={'APPROVE':0,'HOLD':1}
rows.sort(key=lambda x:(order[x['decision']],x['id']))
report={'schema':'ccs-016-report/v1','policy':'initial-v1','items':rows,'counts':{'APPROVE':sum(r['decision']=='APPROVE' for r in rows),'HOLD':sum(r['decision']=='HOLD' for r in rows)}}
raw=json.dumps(report,sort_keys=True,separators=(',',':'))
report['digest']=hashlib.sha256(raw.encode()).hexdigest()
(OUT/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
lines=['# Release Readiness','',f"APPROVE: {report['counts']['APPROVE']}",f"HOLD: {report['counts']['HOLD']}",'']+[f"- {r['id']}: {r['decision']}" for r in rows]+['',f"Digest: `{report['digest']}`",'']
(OUT/'report.md').write_text('\n'.join(lines))
