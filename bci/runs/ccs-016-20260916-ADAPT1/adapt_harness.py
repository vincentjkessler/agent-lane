import difflib, hashlib, json, subprocess
from pathlib import Path

ROOT = Path('bci/runs/ccs-016-20260916-ADAPT1')
FREEZE = '593face0b0a4081935285b5a4a46a4c68cf05d65'
EXPECTED = json.loads((ROOT/'expected-adapted.json').read_text())

expected_rows = [{'id':x['id'],'decision':x['decision']} for x in EXPECTED['expected']]
expected = {
    'schema':'ccs-016-report/v1',
    'policy':'adapted-v2',
    'items':expected_rows,
    'counts':EXPECTED['counts'],
}
raw=json.dumps(expected,sort_keys=True,separators=(',',':'))
expected['digest']=hashlib.sha256(raw.encode()).hexdigest()

results={}
for lane in ('conventional','compositional'):
    report=json.loads((ROOT/lane/'output/report.json').read_text())
    if report != expected:
        raise SystemExit(f'{lane} adapted output mismatch')
    results[lane]={'correct':True,'report_digest':report['digest']}

if results['conventional']['report_digest'] != results['compositional']['report_digest']:
    raise SystemExit('lane digests differ')

def frozen_text(path):
    return subprocess.check_output(['git','show',f'{FREEZE}:{path}'],text=True)

def diff_counts(old,new):
    adds=dels=0
    for line in difflib.unified_diff(old.splitlines(),new.splitlines(),lineterm=''):
        if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
            continue
        if line.startswith('+'): adds+=1
        elif line.startswith('-'): dels+=1
    return adds,dels

lane_paths={
  'conventional':['bci/runs/ccs-016-20260916-ADAPT1/conventional/baseline.py'],
  'compositional':['bci/runs/ccs-016-20260916-ADAPT1/compositional/engine.py','bci/runs/ccs-016-20260916-ADAPT1/compositional/policy.json'],
}
for lane,paths in lane_paths.items():
    touched=[]; adds=dels=0
    for p in paths:
        old=frozen_text(p); new=Path(p).read_text()
        if old!=new:
            touched.append(p)
            a,d=diff_counts(old,new); adds+=a; dels+=d
    results[lane].update({'implementation_files_touched':len(touched),'files_touched':touched,'lines_added':adds,'lines_deleted':dels})

# Separate code/config changes by lane.
results['conventional']['code_files_touched']=1 if results['conventional']['implementation_files_touched'] else 0
results['conventional']['config_files_touched']=0
results['conventional']['prompt_files_touched']=0
results['compositional']['code_files_touched']=1 if 'bci/runs/ccs-016-20260916-ADAPT1/compositional/engine.py' in results['compositional']['files_touched'] else 0
results['compositional']['config_files_touched']=1 if 'bci/runs/ccs-016-20260916-ADAPT1/compositional/policy.json' in results['compositional']['files_touched'] else 0
results['compositional']['prompt_files_touched']=0

out={
  'schema':'ccs-016-adapt-measurement/v1',
  'experiment_id':'CCS-016-20260916-ADAPT1',
  'correctness':'PASS',
  'expected_fixture':'expected-adapted.json',
  'expected_fixture_attribution':EXPECTED['checker'],
  'independence_claimed':False,
  'shared_evaluation_work':['disruption.json','expected-adapted.json','pre-adaptation-manifest.json','provenance-correction.json','adapt_harness.py','.github/workflows/ccs-016-adapt.yml'],
  'lane_specific':results,
  'human_messages_after_freeze':2,
  'human_message_breakdown':{'challenge':1,'provenance_correction':1,'lane_specific_instructions':0},
  'active_human_effort_observable':{'messages':2,'direct_code_or_config_edits':0,'minutes':'not directly observable'},
  'model_usage':{
    'challenge_authoring_assistance':'Astra 6',
    'implementation_assistance_both_lanes':'GPT-5.6 Sol',
    'runtime_llm_calls_conventional':0,
    'runtime_llm_calls_compositional':0,
    'planned_external_evaluator':'Opus 4.6'
  },
  'adaptation_attempts_before_workflow':{
    'conventional_connector_write_attempts':1,
    'compositional_connector_write_attempts':1,
    'failed_connector_write_attempts':0
  }
}
(ROOT/'measurement.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('CCS016_ADAPTED_VERIFY=PASS')
print('CCS016_DIGEST='+expected['digest'])
print('CCS016_MEASUREMENT='+json.dumps(results,sort_keys=True,separators=(',',':')))
