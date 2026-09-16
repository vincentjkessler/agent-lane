import json, hashlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
cfg = json.loads((ROOT / 'trigger.json').read_text())
actual = json.loads((ROOT / 'result.json').read_text())
x = int(cfg['seed'])
mod = int(cfg['modulus'])
mul = int(cfg['multiplier'])
iters = int(cfg['iterations'])
interval = int(cfg['checkpoint_interval'])
checkpoints = []
for i in range(1, iters + 1):
    term = i*i + 53*i + 211
    x = (mul * x + term) % mod
    if i % interval == 0:
        checkpoints.append(x)
digest = hashlib.sha256(','.join(map(str, checkpoints)).encode('utf-8')).hexdigest()
expected = {
    'schema': 'ecs-006a-result/v1',
    'final_x': x,
    'checkpoint_count': len(checkpoints),
    'checkpoints_sha256': digest,
}
if actual != expected:
    print('ECS006A_VERIFY=FAIL')
    print('expected=' + json.dumps(expected, sort_keys=True))
    print('actual=' + json.dumps(actual, sort_keys=True))
    sys.exit(1)
print('ECS006A_VERIFY=PASS')
