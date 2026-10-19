"""Count distinct infinite affine spectra (N <= 200) over both atlas families (textbook: 45, of which 29 not in
the OEIS); how many of them are ℕ itself; per family."""
import sys, os
from collections import defaultdict
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c13_lib import laws_up_to_iso, affine_system_of
from c13_atlas import direct_spectrum, topoly
inf_specs = defaultdict(set); fin_specs = defaultdict(set)
for fam, (vs, ml) in {"3var": (("x", "y", "z"), 4), "2var": (("x", "y"), 5)}.items():
    systems = set(affine_system_of(s, t) for s, t in laws_up_to_iso(vs, ml).values())
    for sysm in systems:
        spec = tuple(direct_spectrum(sysm))
        if not sysm:
            inf_specs[spec].add(fam); continue
        polys = [topoly(p) for p in sysm]
        g = polys[0]
        for q in polys[1:]:
            g = sp.gcd(g, q)
        (inf_specs if g.degree() >= 1 else fin_specs)[spec].add(fam)
alln = tuple(range(1, 201))
print("distinct infinite spectra (union of families):", len(inf_specs), " of which all N:", alln in inf_specs)
print("per family: 3var", sum(1 for v in inf_specs.values() if "3var" in v), " 2var", sum(1 for v in inf_specs.values() if "2var" in v))
print("distinct finite spectra (union):", len(fin_specs), "; total distinct spectra union:", len(set(inf_specs) | set(fin_specs)))
print("infinite spectra with < 8 terms <= 200:", [s for s in inf_specs if len(s) < 8])
