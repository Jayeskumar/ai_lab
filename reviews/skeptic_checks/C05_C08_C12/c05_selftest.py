"""Self-test of the own C05 encoder: SAT model counts (no extra constraints) = brute-force counts
for every one of the 115 identities at n = 2 and n = 3.  -> out/c05_selftest.json"""
import itertools, json, time
from pathlib import Path
import numpy as np
from pysat.solvers import Solver
import c05_checks as C

t0 = time.time()
ids = C.nontrivial_identities()
tabs = {n: [np.array(v).reshape(n, n) for v in itertools.product(range(n), repeat=n * n)] for n in (2, 3)}
bad = []
for t in ids:
    for n in (2, 3):
        bf = sum(C.satisfies_np(T, t) for T in tabs[n])
        E, m = C.encode(t, n, latin_rows=False, latin_cols=False, symbreak=False)
        cnt = 0
        with Solver(name="cadical195", bootstrap_with=E.cl) as S:
            while S.solve():
                mod = set(l for l in S.get_model() if l > 0)
                T = [[next(c for c in range(n) if m[a][b][c] in mod) for b in range(n)] for a in range(n)]
                assert C.satisfies(T, t)
                cnt += 1
                S.add_clause([-m[a][b][T[a][b]] for a in range(n) for b in range(n)])
        if cnt != bf:
            bad.append([C.show(t), n, cnt, int(bf)])
res = {"identities": len(ids), "mismatches": bad, "seconds": round(time.time() - t0, 1)}
(Path(__file__).resolve().parent / "out/c05_selftest.json").write_text(json.dumps(res, indent=1))
print(res)
