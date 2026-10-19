"""For each polynomial of CLM-C13-11: is there a law (atlas families) whose affine system is exactly {G}
(so that Aff = root set of G for every N, with no exceptional primes)?  Also: laws whose system is G times
a constant, or {G, multiples of G with unit cofactors}."""
import sys, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c13_lib import laws_up_to_iso, affine_system_of, show
want = {(1, 2): "2a+1", (1, 3): "3a+1", (1, 0, 1): "a^2+1", (-1, -2, 1): "a^2-2a-1", (-2, 2, 1): "a^2+2a-2",
        (1, 1, 1): "a^2+a+1", (-1, -1, 1): "a^2-a-1", (1, 2, 2): "2a^2+2a+1", (-1, 0, 2): "2a^2-1",
        (1, 0, 0, 0, 1): "a^4+1", (1, 0, -1, 0, 1): "a^4-a^2+1"}
# also allow a -> -a images (same root sets up to sign of a)
def neg(p):
    q = [c * (-1) ** i for i, c in enumerate(p)]
    return tuple(q) if q[-1] > 0 else tuple(-c for c in q)
found = defaultdict(list)
for vs, ml in ((("x", "y", "z"), 4), (("x", "y"), 5)):
    for k, (s, t) in laws_up_to_iso(vs, ml).items():
        sysm = affine_system_of(s, t)
        if len(sysm) == 1:
            p = next(iter(sysm))
            for w, name in want.items():
                if p == w or p == neg(w):
                    found[name].append(f"{show(s)} = {show(t)}" + ("" if p == w else "  [a -> -a]"))
for name in want.values():
    print(f"{name:12s}", len(found[name]), "laws with system exactly {G};", found[name][:2])
