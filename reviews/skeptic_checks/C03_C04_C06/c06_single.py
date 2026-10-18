"""Run own anchored-model enumeration for one law at given sizes (driver around c06_checks.models).
Usage: python3 c06_single.py "<law>" N1 N2 ...   -> prints counts, affinity, timing;
writes out/c06_single_<tag>.json"""
import json
import sys
import time

from c06_checks import OUT, law, models

s = sys.argv[1]
res = {}
for N in map(int, sys.argv[2:]):
    t0 = time.time()
    ms, complete = models(N, [law(s)])
    a = sorted(((T[0][1] - 1) % N) for T in ms)
    aff = all(all(T[x][y] == (x + 1 + ((T[0][1] - 1) % N) * y) % N for x in range(N) for y in range(N)) for T in ms)
    roots = sorted(r for r in range(N) if (r * r + r - 1) % N == 0)
    res[N] = {"models": len(ms), "complete": complete, "all_affine": aff, "a": a, "golden_roots": roots,
              "sec": round(time.time() - t0, 1)}
    print(s, N, res[N], flush=True)
tag = s.replace("(", "").replace(")", "").replace("=", "_") + "_" + "_".join(sys.argv[2:])
(OUT / f"c06_single_{tag}.json").write_text(json.dumps(res, indent=1))
