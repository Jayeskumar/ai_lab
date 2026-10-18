"""Count finite affine systems in the atlas without a constant polynomial and without a coprime pair
(so that every pairwise resultant is 0): relevant to the wording 'L divides a resultant of the system'."""
import sys, os
from collections import defaultdict
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c13_lib import laws_up_to_iso, affine_system_of
from c13_atlas import topoly, A
cnt = 0; total_fin = 0; ex = []
for vs, ml in ((("x", "y", "z"), 4), (("x", "y"), 5)):
    systems = defaultdict(list)
    for k, (s, t) in laws_up_to_iso(vs, ml).items():
        systems[affine_system_of(s, t)].append(k)
    for sysm, ks in systems.items():
        if not sysm:
            continue
        polys = [topoly(p) for p in sysm]
        g = polys[0]
        for q in polys[1:]:
            g = sp.gcd(g, q)
        if g.degree() >= 1:
            continue
        total_fin += 1
        if any(q.degree() == 0 for q in polys):
            continue
        if any(sp.gcd(polys[i], polys[j]).degree() == 0 for i in range(len(polys)) for j in range(i + 1, len(polys))):
            continue
        cnt += 1
        if len(ex) < 3:
            ex.append((ks[0], [str(q.as_expr()) for q in polys]))
print("finite systems:", total_fin, " without constant and without coprime pair:", cnt, ex)
