"""Targeted random search for counterexamples to CLM-C01-08 among LONG 'hard' relations that share
at least one common border (the regime where the conjectured formula differs from 1/(1-qx+x^k)).

Construction: pick a common border b, put u = b + x + b', v = b + y + b'' where the middle parts are
random and the result is forced to start and end with b; keep pairs with
Borders(u) & Borders(v) != {} and neither border set containing the other.
Counts by the C union-find (classcount.c), compared with the formula for n = 1..nmax.

Usage: python c01_targeted_search.py q kmin kmax nmax samples seed
"""
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c01_border_search import borders, canonical, formula, run_c  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def sample(q, k, rng):
    al = "0123456789"[:q]
    while True:
        L = rng.randint(1, k // 2)
        b = "".join(rng.choice(al) for _ in range(L))
        def make():
            mid = "".join(rng.choice(al) for _ in range(k - 2 * L)) if k >= 2 * L else None
            if mid is None:
                return None
            return b + mid + b
        u, v = make(), make()
        if u is None or v is None or u == v:
            continue
        bu, bv = borders(u), borders(v)
        if not (bu & bv) or bu <= bv or bv <= bu:
            continue
        return canonical(u, v)


def main():
    q, kmin, kmax, nmax, samples, seed = (int(a) for a in sys.argv[1:7])
    rng = random.Random(seed)
    t0 = time.time()
    pairs = set()
    tries = 0
    while len(pairs) < samples and tries < 50 * samples:
        tries += 1
        pairs.add(sample(q, rng.randint(kmin, kmax), rng))
    pairs = sorted(pairs)
    fails, ncb = [], {}
    by_k = {}
    for u, v in pairs:
        by_k.setdefault(len(u), []).append((u, v))
    for k, ps in sorted(by_k.items()):
        res = run_c(ps, q, nmax)
        for (u, v), counts in res.items():
            common = borders(u) & borders(v)
            ncb[len(common)] = ncb.get(len(common), 0) + 1
            pred = formula(u, v, q, nmax)
            if counts != pred:
                fails.append({"u": u, "v": v, "counts": counts, "predicted": pred})
    out = {"q": q, "k_range": [kmin, kmax], "nmax": nmax, "relations": len(pairs),
           "by_number_of_common_borders": ncb, "failures": fails, "seconds": round(time.time() - t0, 1)}
    name = f"targeted_q{q}_k{kmin}-{kmax}_n{nmax}_s{seed}.json"
    json.dump(out, open(os.path.join(OUT, name), "w"), indent=1)
    print(f"targeted q={q} k={kmin}..{kmax} n<={nmax}: {len(pairs)} hard relations with common borders "
          f"(#common borders: {dict(sorted(ncb.items()))}); failures {len(fails)} [{out['seconds']} s]")


if __name__ == "__main__":
    main()
