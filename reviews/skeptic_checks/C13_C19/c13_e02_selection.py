"""Re-create the selection of EXP-C13-02 with own code: per family, the affine classes (spectrum up to 120) that
pass the filter 'not all N and max element >= 60', split by the true kind (Q-gcd constant or not); also the
infinite non-trivial classes that the filter misses."""
import sys, os
from collections import defaultdict
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c13_lib import laws_up_to_iso, affine_system_of, roots_mod
from c13_atlas import topoly
for fam, (vs, ml) in {"3var_le4": (("x", "y", "z"), 4), "2var_le5": (("x", "y"), 5)}.items():
    laws = laws_up_to_iso(vs, ml)
    bysys = defaultdict(list)
    for k, (s, t) in laws.items():
        bysys[affine_system_of(s, t)].append(k)
    classes = defaultdict(lambda: {"laws": 0, "kinds": set()})
    for sysm, ks in bysys.items():
        spec = tuple(N for N in range(1, 121) if (roots_mod(sysm, N) if sysm else True))
        if sysm:
            polys = [topoly(p) for p in sysm]
            g = polys[0]
            for q in polys[1:]:
                g = sp.gcd(g, q)
            kind = "inf" if g.degree() >= 1 else "fin"
        else:
            kind = "all"
        classes[spec]["laws"] += len(ks)
        classes[spec]["kinds"].add(kind)
    sel = {s: c for s, c in classes.items() if not (len(s) == 120 or s[-1] < 60)}
    sel_fin = [s for s, c in sel.items() if c["kinds"] == {"fin"}]
    sel_inf = [s for s, c in sel.items() if "inf" in c["kinds"]]
    inf_all = [s for s, c in classes.items() if "inf" in c["kinds"] and len(s) < 120]
    missed = [s for s in inf_all if s not in sel]
    tested = sum(min(3, classes[s]["laws"]) for s in sel)
    print(fam, "classes passing the filter:", len(sel), "(finite", len(sel_fin), ", infinite", len(sel_inf), ")",
          "laws tested (3 per class):", tested, "of which finite-class:", sum(min(3, classes[s]["laws"]) for s in sel_fin),
          "| infinite non-trivial classes missed by the filter:", len(missed), [s[:8] for s in missed])
