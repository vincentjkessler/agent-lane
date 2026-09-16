import hashlib, json, sys
from pathlib import Path

root = Path(__file__).resolve().parent
cfg = json.loads((root / 'input.json').read_text())
actual = json.loads((root / 'result.json').read_text())

value = cfg['seed']
marks = []
for step in range(cfg['iterations']):
    i = step + 1
    addend = i * i + 43 * i + 211
    value = ((value * cfg['multiplier']) + addend) % cfg['modulus']
    if (i // cfg['checkpoint_interval']) * cfg['checkpoint_interval'] == i:
        marks.append(str(value))
expected = {
    'schema': 'ecs-006b-result/v1',
    'final_x': value,
    'checkpoint_count': len(marks),
    'checkpoint_sha256': hashlib.sha256(','.join(marks).encode('utf-8')).hexdigest(),
}
if actual != expected:
    print('ECS006B_VERIFY=FAIL')
    print(json.dumps({'expected': expected, 'actual': actual}, sort_keys=True))
    sys.exit(1)
print('ECS006B_VERIFY=PASS')
