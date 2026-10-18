"""How far is an infinite affine spectrum from the root set of the Q-gcd of its system?  (CLM-C13-11 wording)"""
import sys, os
from collections import defaultdict, Counter
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c13_lib import laws_up_to_iso, affine_system_of
from c13_atlas import direct_spectrum, topoly, A
diffs = Counter(); examples = {}
nsys = 0
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
        if g.degree() < 1:
            continue
        nsys += 1
        G = g.primitive()[1]
        gp = tuple(int(c) for c in reversed(G.all_coeffs()))
        s1, s2 = set(direct_spectrum(sysm)), set(direct_spectrum([gp]))
        if s1 != s2:
            ps = sorted({p for N in s1 ^ s2 for p in sp.factorint(N)})
            diffs[tuple(ps)] += 1
            examples.setdefault(tuple(ps), (ks[0], [list(p) for p in sysm], str(G.as_expr()),
                                            sorted(s1 - s2)[:6], sorted(s2 - s1)[:6]))
print("infinite systems:", nsys, " systems whose spectrum differs from the root set of the gcd (N<=200):",
      sum(diffs.values()))
for ps, c in diffs.most_common():
    print("  primes", ps, "systems", c, "example", examples[ps])
