import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

with (ROOT / "input.json").open("r", encoding="utf-8") as f:
    cfg = json.load(f)

x = cfg["seed"]
checkpoints = []
for i in range(1, cfg["iterations"] + 1):
    x = (cfg["multiplier"] * x + (i * i + 31 * i + 101 * cfg["epoch"])) % cfg["modulus"]
    if i % cfg["checkpoint_interval"] == 0:
        checkpoints.append(x)

checkpoint_text = ",".join(str(v) for v in checkpoints)
result = {
    "schema": "ecs-014-result/v1",
    "epoch": cfg["epoch"],
    "final_x": x,
    "checkpoint_count": len(checkpoints),
    "checkpoint_sha256": hashlib.sha256(checkpoint_text.encode("utf-8")).hexdigest(),
}

compact = json.dumps(result, sort_keys=True, separators=(",", ":"))
(ROOT / "result.json").write_text(compact + "\n", encoding="utf-8")
print(f"ECS014_RESULT={compact}")
