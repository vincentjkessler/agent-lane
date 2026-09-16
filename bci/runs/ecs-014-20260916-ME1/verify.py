import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

with (ROOT / "input.json").open("r", encoding="utf-8") as f:
    cfg = json.load(f)
with (ROOT / "result.json").open("r", encoding="utf-8") as f:
    actual = json.load(f)

x = cfg["seed"]
checkpoints = []
for i in range(1, cfg["iterations"] + 1):
    term = i * i + 31 * i + 101 * cfg["epoch"]
    x = (cfg["multiplier"] * x + term) % cfg["modulus"]
    if i % cfg["checkpoint_interval"] == 0:
        checkpoints.append(x)

checkpoint_text = ",".join(map(str, checkpoints))
expected = {
    "schema": "ecs-014-result/v1",
    "epoch": cfg["epoch"],
    "final_x": x,
    "checkpoint_count": len(checkpoints),
    "checkpoint_sha256": hashlib.sha256(checkpoint_text.encode("utf-8")).hexdigest(),
}

if actual != expected:
    print("ECS014_VERIFY=FAIL")
    print("expected=" + json.dumps(expected, sort_keys=True, separators=(",", ":")))
    print("actual=" + json.dumps(actual, sort_keys=True, separators=(",", ":")))
    sys.exit(1)

print("ECS014_VERIFY=PASS")
