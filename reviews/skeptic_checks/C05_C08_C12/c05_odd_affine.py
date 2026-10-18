"""Idempotent affine models x*y = (1-b)x + by of law 677 (and x*y = a x + (1-a) y of law 1313) over Z_p:
check that they exist exactly when p = 1 mod 10 (b a primitive 10th root of unity), p < 200.  -> out/c05_odd_affine.json"""
import json
from pathlib import Path
res = {}
for p in [q for q in range(3, 200) if all(q % d for d in range(2, int(q ** 0.5) + 1))]:
    found677 = [b for b in range(p) if all((lambda op: op(y, op(x, op(op(y, x), y))) == x)(lambda u, v: ((1 - b) * u + b * v) % p) for x in range(p) for y in range(p))]
    found1313 = [a for a in range(p) if all((lambda op: op(y, op(op(op(y, x), x), y)) == x)(lambda u, v: (a * u + (1 - a) * v) % p) for x in range(p) for y in range(p))]
    res[p] = {"p mod 10": p % 10, "677_b": found677, "1313_a": found1313}
ok = all((bool(v["677_b"]) == (p % 10 == 1)) and (bool(v["1313_a"]) == (p % 10 == 1)) for p, v in res.items())
(Path(__file__).resolve().parent / "out/c05_odd_affine.json").write_text(json.dumps({"exists_iff_p_1_mod_10": ok, "rows": res}, indent=1))
print("exists iff p = 1 mod 10 (p < 200):", ok, {p: v for p, v in res.items() if v["677_b"]})
