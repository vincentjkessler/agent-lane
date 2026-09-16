import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
challenge = json.loads((ROOT / "challenge.json").read_text(encoding="utf-8"))

x = challenge["seed"]
modulus = challenge["modulus"]
multiplier = challenge["multiplier"]
iterations = challenge["iterations"]
checkpoint_interval = challenge["checkpoint_interval"]
checkpoints = []

for i in range(1, iterations + 1):
    x = (multiplier * x + (i * i + 17 * i + 23)) % modulus
    if i % checkpoint_interval == 0:
        checkpoints.append(x)

checkpoint_bytes = ",".join(str(v) for v in checkpoints).encode("utf-8")
result = {
    "final_x": x,
    "checkpoint_count": len(checkpoints),
    "checkpoints_sha256": hashlib.sha256(checkpoint_bytes).hexdigest(),
    "schema": "ecs-008-result/v1",
}

serialized = json.dumps(result, sort_keys=True, separators=(",", ":"))
(ROOT / "result.json").write_text(serialized + "\n", encoding="utf-8")
