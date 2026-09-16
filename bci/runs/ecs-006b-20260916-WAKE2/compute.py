import hashlib, json
from pathlib import Path

root = Path(__file__).resolve().parent
config = json.loads((root / 'input.json').read_text())
x = config['seed']
checkpoints = []
for i in range(1, config['iterations'] + 1):
    x = (config['multiplier'] * x + (i*i + 43*i + 211)) % config['modulus']
    if i % config['checkpoint_interval'] == 0:
        checkpoints.append(x)
text = ','.join(str(v) for v in checkpoints)
result = {
    'schema': 'ecs-006b-result/v1',
    'final_x': x,
    'checkpoint_count': len(checkpoints),
    'checkpoint_sha256': hashlib.sha256(text.encode()).hexdigest(),
}
serialized = json.dumps(result, sort_keys=True, separators=(',', ':'))
(root / 'result.json').write_text(serialized + '\n')
print('ECS006B_RESULT=' + serialized)
