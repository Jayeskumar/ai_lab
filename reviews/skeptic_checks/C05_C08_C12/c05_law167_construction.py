"""Sufficiency half of CLM-C05-04 (spectrum of law 167, x = (yx)(xy), is exactly {n = 0, 1 mod 4}):
build the textbook construction (pair the 2-subsets {a,b} <-> {c,d}; ab = c, ba = d, cd = b, dc = a; xx = x)
from an arbitrary perfect matching of the 2-subsets and check the law by brute force.  -> out/c05_law167_construction.json"""
import itertools, json, random
from pathlib import Path
rng = random.Random(167)
res = {}
for n in range(1, 30):
    if n % 4 not in (0, 1):
        continue
    pairs = list(itertools.combinations(range(n), 2))
    ok_all = True
    for trial in range(5):
        rng.shuffle(pairs)
        T = [[None] * n for _ in range(n)]
        for i in range(n):
            T[i][i] = i
        for k in range(0, len(pairs), 2):
            (a, b), (c, d) = pairs[k], pairs[k + 1]
            if rng.random() < 0.5:
                a, b = b, a
            if rng.random() < 0.5:
                c, d = d, c
            T[a][b], T[b][a], T[c][d], T[d][c] = c, d, b, a
        ok = all(T[T[y][x]][T[x][y]] == x for x in range(n) for y in range(n))
        ok_all &= ok
    res[n] = ok_all
(Path(__file__).resolve().parent / "out/c05_law167_construction.json").write_text(json.dumps(res))
print(res)
