"""Spot-check the C union-find counter against an independent pure-Python BFS at larger n."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c01_validate_tools import bfs_classes
from c01_border_search import run_c, formula
rng = random.Random(2026)
cases = [(2, 7, 14), (2, 8, 15), (2, 9, 15), (2, 6, 15), (3, 4, 9), (3, 5, 9), (4, 3, 7)]
bad = tot = 0
for q, k, n in cases:
    al = "0123456789"[:q]
    for _ in range(6):
        u = "".join(rng.choice(al) for _ in range(k)); v = u
        while v == u:
            v = "".join(rng.choice(al) for _ in range(k))
        c = run_c([(u, v)], q, n)[(u, v)]
        b = [bfs_classes(u, v, al, m) for m in range(1, n + 1)]
        tot += 1; bad += c != b
print(f"C counter vs Python BFS: {tot} random relations (n up to 15): mismatches {bad}")
