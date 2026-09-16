import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
challenge = json.loads((ROOT / "challenge.json").read_text(encoding="utf-8"))
actual = json.loads((ROOT / "result.json").read_text(encoding="utf-8"))

seed = challenge["seed"]
modulus = challenge["modulus"]
multiplier = challenge["multiplier"]
iterations = challenge["iterations"]
checkpoint_interval = challenge["checkpoint_interval"]

x = seed
checkpoints = []
for i in range(1, iterations + 1):
    additive = i * i + 17 * i + 23
    x = (multiplier * x + additive) % modulus
    if i % checkpoint_interval == 0:
        checkpoints.append(x)

joined = ",".join(map(str, checkpoints))
expected = {
    "final_x": x,
    "checkpoint_count": len(checkpoints),
    "checkpoints_sha256": hashlib.sha256(joined.encode("utf-8")).hexdigest(),
    "schema": "ecs-008-result/v1",
}

if actual != expected:
    print("verification mismatch", file=sys.stderr)
    print("expected=" + json.dumps(expected, sort_keys=True, separators=(",", ":")), file=sys.stderr)
    print("actual=" + json.dumps(actual, sort_keys=True, separators=(",", ":")), file=sys.stderr)
    sys.exit(1)
