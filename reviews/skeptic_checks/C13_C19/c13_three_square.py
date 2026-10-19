"""Systems with Q-gcd a^2 + 2a - 2 ('3 is a square'): cofactor ideal, exceptional primes, comparison at
prime powers p^e (p | R', e <= 8)."""
import sys, os
from collections import defaultdict
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c13_lib import laws_up_to_iso, affine_system_of, show, roots_mod
A = sp.Symbol("a")
G = sp.Poly(A**2 + 2*A - 2, A)
systems = defaultdict(list)
for vs, ml in ((("x", "y", "z"), 4), (("x", "y"), 5)):
    for k, (s, t) in laws_up_to_iso(vs, ml).items():
        systems[affine_system_of(s, t)].append(f"{show(s)} = {show(t)}")
for sysm, laws in systems.items():
    if not sysm:
        continue
    polys = [sp.Poly(list(reversed(p)), A) for p in sysm]
    g = polys[0]
    for q in polys[1:]:
        g = sp.gcd(g, q)
    if g.degree() < 1 or g.primitive()[1] != G and g.primitive()[1] != -G:
        continue
    cof = [sp.div(q, G)[0] for q in polys]
    R = 0
    for c in cof:
        if c.degree() == 0:
            R = sp.gcd(R, int(c.as_expr()))
    for i in range(len(cof)):
        for j in range(i + 1, len(cof)):
            if cof[i].degree() >= 1 and cof[j].degree() >= 1:
                R = sp.gcd(R, int(sp.resultant(cof[i].as_expr(), cof[j].as_expr(), A)))
    ps = sorted(sp.factorint(abs(int(R))).keys()) if R else "R=0"
    bad = []
    if R:
        for p in ps:
            for e in range(1, 9):
                q = p ** e
                if bool(roots_mod(sysm, q)) != bool(roots_mod([(-2, 2, 1)], q)):
                    bad.append(q)
    print(len(laws), "laws, e.g.", laws[0], "| system", [str(q.as_expr()) for q in polys], "| cofactor R'", R,
          "primes", ps, "| prime powers where Aff differs from roots of G:", bad)
