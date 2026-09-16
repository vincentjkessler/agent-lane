import json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parent
cfg = json.loads((ROOT / 'trigger.json').read_text())
x = int(cfg['seed'])
mod = int(cfg['modulus'])
mul = int(cfg['multiplier'])
iters = int(cfg['iterations'])
interval = int(cfg['checkpoint_interval'])
checkpoints = []
for i in range(1, iters + 1):
    x = (mul * x + i*i + 53*i + 211) % mod
    if i % interval == 0:
        checkpoints.append(x)
text = ','.join(str(v) for v in checkpoints)
result = {
    'schema': 'ecs-006a-result/v1',
    'final_x': x,
    'checkpoint_count': len(checkpoints),
    'checkpoints_sha256': hashlib.sha256(text.encode()).hexdigest(),
}
(ROOT / 'result.json').write_text(json.dumps(result, sort_keys=True, separators=(',', ':')))
print('ECS006A_RESULT=' + json.dumps(result, sort_keys=True, separators=(',', ':')))
