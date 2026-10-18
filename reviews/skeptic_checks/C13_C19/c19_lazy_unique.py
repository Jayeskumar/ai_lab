"""Skeptic check: uniqueness of lazy Fibonacci representations and the interval claim used in the proof of
Theorem 2 (CLM-C19-02); Corollary 3 (CLM-C19-04): lazy(n) = Zeckendorf(n) iff n = F_k - 1.  Own code."""
from collections import Counter, defaultdict
import c19_checks as C

LEV = 21
FIB = C.FIB
count = Counter()
tops = defaultdict(lambda: [10**18, -1])
for mask in range(1, 1 << LEV):
    t = mask.bit_length() - 1
    ok = all(not (((mask >> k) & 1) == 0 and ((mask >> (k + 1)) & 1) == 0) for k in range(t))
    if not ok:
        continue
    v = sum(FIB[k] for k in range(t + 1) if (mask >> k) & 1)
    count[v] += 1
    lo, hi = tops[t]
    tops[t] = [min(lo, v), max(hi, v)]
limit = FIB[LEV] - 1          # every n below this has its lazy top level < LEV... (top t needs F_{t+2}-1 <= n)
bad_unique = [n for n in range(1, FIB[LEV - 1] - 1) if count[n] != 1]
bad_interval = [t for t in range(LEV) if tops[t] != [FIB[t + 1] - 1, FIB[t + 2] - 2]]
print("lazy strings over", LEV, "levels: values with multiplicity != 1 below", FIB[LEV - 1] - 1, ":", bad_unique[:5])
print("top-level intervals [F_{t+2}-1, F_{t+3}-2] wrong for t in", bad_interval)
fk1 = {f - 1 for f in FIB}
bad_cor = []
for n in range(1, 100000):
    z = [0] * (C.top_level(n) + 1)
    for k in C.zeck(n):
        z[k] = 1
    if (C.lazy(n) == z) != (n in fk1):
        bad_cor.append(n)
print("Corollary 3 (lazy == Zeckendorf iff n = F_k - 1), n < 100000: violations", bad_cor[:5])
