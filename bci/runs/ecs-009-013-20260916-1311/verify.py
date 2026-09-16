import hashlib
import json
import sys


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def expected_lexicographic_order(nodes, edges):
    remaining = set(nodes)
    done = []
    done_set = set()
    prereq = {n: set() for n in nodes}
    for a, b in edges:
        prereq[b].add(a)
    while remaining:
        eligible = sorted(n for n in remaining if prereq[n].issubset(done_set))
        if not eligible:
            raise AssertionError("cycle detected")
        chosen = eligible[0]
        remaining.remove(chosen)
        done.append(chosen)
        done_set.add(chosen)
    return done


def expected_max_path(nodes, edges, order):
    parents = {n: [] for n in nodes}
    for a, b in edges:
        parents[b].append(a)
    score = {}
    for n in order:
        score[n] = nodes[n] + max([score[p] for p in parents[n]] or [0])
    return max(score.values())


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify.py CHALLENGE RESULT")
    challenge = load(sys.argv[1])
    result = load(sys.argv[2])
    order = expected_lexicographic_order(challenge["nodes"], challenge["edges"])
    max_sum = expected_max_path(challenge["nodes"], challenge["edges"], order)
    material = "|".join(order) + ":" + str(max_sum) + ":" + challenge["salt"]
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    expected = {
        "schema": "ecs-compute-result/v1",
        "order": order,
        "maximum_weighted_path_sum": max_sum,
        "fingerprint_sha256": digest
    }
    if result != expected:
        print("ECS_VERDICT=FAIL")
        print("EXPECTED=" + json.dumps(expected, sort_keys=True))
        print("OBSERVED=" + json.dumps(result, sort_keys=True))
        raise SystemExit(1)
    print("ECS_VERDICT=PASS")
    print("VERIFIED_RESULT=" + json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
