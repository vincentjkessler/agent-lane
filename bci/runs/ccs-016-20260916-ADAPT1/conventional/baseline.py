import hashlib, json
from pathlib import Path

ROOT = Path('bci/runs/ccs-016-20260916-ADAPT1')
DATA = json.loads((ROOT/'input/releases.json').read_text())['items']
OUT = ROOT/'conventional/output'
OUT.mkdir(parents=True, exist_ok=True)

rows=[]
recognized_impact={'none','minor','major'}
for item in DATA:
    impact=item.get('customer_impact')
    original_ok = item['tests_passed'] is True and item['security_review']=='pass' and item['rollback_ready'] is True
    docs_ok = item.get('docs_ready') is True
    impact_ok = impact in recognized_impact
    owner_ok = impact == 'none' or item.get('owner_ack') is True
    approve = original_ok and docs_ok and impact_ok and owner_ok
    rows.append({'id':item['id'],'decision':'APPROVE' if approve else 'HOLD'})
order={'APPROVE':0,'HOLD':1}
rows.sort(key=lambda x:(order[x['decision']],x['id']))
report={'schema':'ccs-016-report/v1','policy':'adapted-v2','items':rows,'counts':{'APPROVE':sum(r['decision']=='APPROVE' for r in rows),'HOLD':sum(r['decision']=='HOLD' for r in rows)}}
raw=json.dumps(report,sort_keys=True,separators=(',',':'))
report['digest']=hashlib.sha256(raw.encode()).hexdigest()
(OUT/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
lines=['# Release Readiness','',f"APPROVE: {report['counts']['APPROVE']}",f"HOLD: {report['counts']['HOLD']}",'']+[f"- {r['id']}: {r['decision']}" for r in rows]+['',f"Digest: `{report['digest']}`",'']
(OUT/'report.md').write_text('\n'.join(lines))
