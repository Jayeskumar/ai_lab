"""Counterexample search for CLM-C05-09 (conjectured spectra {1} + odd n >= 5 for ETP laws 677 and 1313).

Idea (derived in the review): for an affine operation x*y = a x + b y over a field, law 677
x = y(x((yx)y)) holds iff  a b (1 + b^2) = 1  and  a + a^2 b^2 + b^3 = 0,  and law 1313
x = y(((yx)x)y) holds iff  a b^2 (a + 1) = 1  and  a + a^3 b + b^2 = 0.  With a + b = 1 (idempotent) in
characteristic 2 both reduce to "the relevant coefficient is a primitive 5th root of unity", which exists
in GF(16).  This script builds the 16-element tables and checks the laws by brute force over all (x, y)
with its own evaluator; it also lists every affine (a, b) over GF(16), GF(8), GF(4), and every scalar
affine x*y = a x + b y + c over Z_n, n = 8, 10, 16, that satisfies either law.  -> out/c05_gf16.json"""
import itertools
import json
from pathlib import Path

def gf_mul_factory(deg, poly):
    def mul(u, v):
        r = 0
        while v:
            if v & 1:
                r ^= u
            v >>= 1
            u <<= 1
            if u >> deg & 1:
                u ^= poly
        return r
    return mul

FIELDS = {16: (4, 0b10011), 8: (3, 0b1011), 4: (2, 0b111)}
LAWS = {677: lambda op, x, y: op(y, op(x, op(op(y, x), y))),
        1313: lambda op, x, y: op(y, op(op(op(y, x), x), y))}

def check(table, law):
    n = len(table)
    op = lambda u, v: table[u][v]
    return all(LAWS[law](op, x, y) == x for x in range(n) for y in range(n))

out = {"field_affine": {}, "Zn_affine": {}, "example_tables": {}}
for q, (deg, poly) in FIELDS.items():
    mul = gf_mul_factory(deg, poly)
    for law in LAWS:
        sols = []
        for a in range(q):
            for b in range(q):
                T = [[mul(a, x) ^ mul(b, y) for y in range(q)] for x in range(q)]
                if check(T, law):
                    sols.append((a, b))
                    if q == 16 and f"{law}@16" not in out["example_tables"]:
                        out["example_tables"][f"{law}@16"] = {"a": a, "b": b, "field": "GF(2)[t]/(t^4+t+1), elements as bit masks",
                                                              "table": T,
                                                              "quasigroup": all(len(set(r)) == q for r in T) and all(len(set(c)) == q for c in zip(*T)),
                                                              "idempotent": all(T[i][i] == i for i in range(q))}
        out["field_affine"][f"{law}@GF({q})"] = sols
for n in (8, 10, 16):
    for law in LAWS:
        sols = []
        for a, b, c in itertools.product(range(n), repeat=3):
            T = [[(a * x + b * y + c) % n for y in range(n)] for x in range(n)]
            if check(T, law):
                sols.append((a, b, c))
        out["Zn_affine"][f"{law}@Z{n}"] = sols
(Path(__file__).resolve().parent / "out/c05_gf16.json").write_text(json.dumps(out, indent=1))
for k, v in out["field_affine"].items():
    print(k, len(v), v[:6])
for k, v in out["Zn_affine"].items():
    print(k, len(v))
for k, v in out["example_tables"].items():
    print(k, "a =", v["a"], "b =", v["b"], "quasigroup", v["quasigroup"], "idempotent", v["idempotent"])
