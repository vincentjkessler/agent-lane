import hashlib
import heapq
import json
import sys


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def lexicographic_toposort(nodes, edges):
    indegree = {n: 0 for n in nodes}
    outgoing = {n: [] for n in nodes}
    for a, b in edges:
        outgoing[a].append(b)
        indegree[b] += 1
    ready = [n for n, d in indegree.items() if d == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        n = heapq.heappop(ready)
        order.append(n)
        for nxt in outgoing[n]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(ready, nxt)
    if len(order) != len(nodes):
        raise ValueError("graph is cyclic")
    return order


def maximum_weighted_path_sum(nodes, edges, topo_order):
    incoming = {n: [] for n in nodes}
    for a, b in edges:
        incoming[b].append(a)
    best = {}
    for n in topo_order:
        parent_best = max((best[p] for p in incoming[n]), default=0)
        best[n] = parent_best + nodes[n]
    return max(best.values())


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: solve.py CHALLENGE RESULT")
    challenge = load(sys.argv[1])
    nodes = challenge["nodes"]
    edges = challenge["edges"]
    order = lexicographic_toposort(nodes, edges)
    max_sum = maximum_weighted_path_sum(nodes, edges, order)
    material = "|".join(order) + ":" + str(max_sum) + ":" + challenge["salt"]
    fingerprint = hashlib.sha256(material.encode("utf-8")).hexdigest()
    result = {
        "schema": "ecs-compute-result/v1",
        "order": order,
        "maximum_weighted_path_sum": max_sum,
        "fingerprint_sha256": fingerprint
    }
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print("ECS_RESULT=" + json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
