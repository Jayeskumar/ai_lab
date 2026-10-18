"""Skeptic check C13-B: soundness of offset congruence closure (Theorem 6, CLM-C13-06).

Stage 1 (own code only): own closure on the 17 laws of CLM-C06-10 and on all 18,581 laws of the 3-variable
         family; exhaustive enumeration of ALL anchored tables of sizes 2 and 3 for every law.
Stage 2 (deliberate comparison): the procedure under test, systems.anchored.offset_closure_bound, is run with
         the parameters of EXP-C13-08 on the same laws; its bounds are compared with the exhaustive truth for
         N = 2, 3 and with my own closure.
Stage 3 (own SAT encoding): for laws with a bound g (either closure), sizes N = 4..7 not dividing g are checked
         UNSAT (all bounded laws at N = 4, a random sample at N = 5, 6, 7).

usage: python3 c13_closure.py stage1|stage2|stage3
"""
import json
import os
import random
import sys
import time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from c13_lib import (affine_system_of, all_anchored_tables, laws_up_to_iso, law_holds_all_tables,  # noqa
                     own_closure_bound, read_law, roots_mod, sat_model)

OUT = os.path.join(HERE, "out")

C06_13 = ["x(yz)=((zx)x)y", "x(yz)=((zx)y)x", "x(yz)=((zy)x)x", "(xy)z=y((zx)y)", "(xy)z=y((zy)x)",
          "(xy)z=z((yx)z)", "(xy)z=z((yz)x)"]
C06_12 = ["x(yz)=y((yx)z)", "x(yz)=((xx)y)z", "x(yz)=((xx)z)y", "x(yz)=((xy)x)z", "x(yz)=((xy)y)z",
          "x(yz)=((xy)z)x", "x(yz)=((xy)z)y", "x(yz)=((xz)x)y", "x(yz)=((xz)y)x", "x(yz)=((xz)y)y"]


def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def exact_div(law, g):
    sysm = affine_system_of(*law)
    return g > 0 and all((roots_mod(sysm, d) if sysm else True) for d in divs(g))


def stage1():
    t0 = time.time()
    res = {"c06": []}
    for name in C06_13 + C06_12:
        law = read_law(name)
        g = own_closure_bound([law], values=(0, 1, 2, 3, 4, -1, -2), rounds=8, node_values=10)
        res["c06"].append({"law": name, "own_bound": g, "exact": exact_div(law, g)})
        print("C06-10 law", name, "own bound", g, "exact Div(g):", exact_div(law, g), flush=True)
    fam = laws_up_to_iso(("x", "y", "z"), 4)
    keys = sorted(fam)
    print("family size", len(keys), flush=True)
    own = {}
    for i, k in enumerate(keys):
        own[k] = own_closure_bound([fam[k]], values=(0, 1, 2, 3, -1), rounds=4)
    cnt = Counter(own.values())
    ex = Counter(g for k, g in own.items() if g > 0 and exact_div(fam[k], g))
    print("own closure bounds:", dict(sorted(cnt.items())), "exact Div(g):", dict(sorted(ex.items())),
          "total exact", sum(ex.values()), flush=True)
    # exhaustive truth for N = 2, 3
    truth = {}
    T2, T3 = all_anchored_tables(2), all_anchored_tables(3)
    for i, k in enumerate(keys):
        s, t = fam[k]
        truth[k] = (bool(law_holds_all_tables(T2, s, t).any()), bool(law_holds_all_tables(T3, s, t).any()))
    viol = []
    for k in keys:
        g = own[k]
        if g > 0:
            for N, has in zip((2, 3), truth[k]):
                if has and g % N:
                    viol.append((k, N, g))
    print("own closure vs exhaustive N=2,3: violations", len(viol), viol[:5], flush=True)
    res.update({"family_size": len(keys), "own_bounds": {str(a): b for a, b in sorted(cnt.items())},
                "own_exact": {str(a): b for a, b in sorted(ex.items())}, "own_exact_total": sum(ex.values()),
                "own_viol_N23": viol, "n_models_N2": sum(v[0] for v in truth.values()),
                "n_models_N3": sum(v[1] for v in truth.values()), "elapsed_s": round(time.time() - t0, 1)})
    json.dump(res, open(os.path.join(OUT, "c13_closure_stage1.json"), "w"), indent=1)
    json.dump({"|".join(k): [own[k], truth[k][0], truth[k][1]] for k in keys},
              open(os.path.join(OUT, "c13_closure_perlaw_own.json"), "w"))


def stage2():
    """Deliberate comparison: run the procedure under test (systems/anchored.py) on the same laws."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
    from systems.anchored import offset_closure_bound, enumerate_laws, law_from_key  # procedure under test
    from systems.magma import parse
    t0 = time.time()
    per = json.load(open(os.path.join(OUT, "c13_closure_perlaw_own.json")))
    # map their canonical keys to mine via my canonicalisation of their parsed laws
    from c13_lib import law_orbit_key
    theirs = {}
    fam_keys = enumerate_laws(("x", "y", "z"), 4)
    for key in fam_keys:
        law = law_from_key(key)
        g = offset_closure_bound([law], values=(0, 1, 2, 3, -1), rounds=4)
        mine = law_orbit_key(law[0], law[1], ("x", "y", "z"))
        theirs["|".join(mine)] = g
    print("their family size", len(fam_keys), "mapped", len(theirs), "own keys", len(per), flush=True)
    missing = set(per) ^ set(theirs)
    cnt = Counter(theirs.values())
    viol = []
    stronger_theirs = stronger_own = diff = 0
    for k, (g_own, m2, m3) in per.items():
        g = theirs.get(k)
        if g is None:
            continue
        if g > 0:
            for N, has in ((2, m2), (3, m3)):
                if has and g % N:
                    viol.append((k, N, g))
        if g != g_own:
            diff += 1
            if g_own == 0 or (g > 0 and g_own % g == 0 and g != g_own):
                stronger_theirs += 1
            elif g == 0 or (g_own > 0 and g % g_own == 0):
                stronger_own += 1
    # C06 laws with their C06 parameters
    c06 = []
    for name in C06_13 + C06_12:
        a, b = name.split("=")
        law = (parse(a), parse(b))
        g = offset_closure_bound([law], values=(0, 1, 2, 3, 4, -1, -2), rounds=8, max_symbols=20000,
                                 symbol_values=10)
        c06.append((name, g))
    print("their bounds:", dict(sorted(cnt.items())), flush=True)
    print("their closure vs exhaustive N=2,3: violations", len(viol), viol[:5], flush=True)
    print("bounds differing own/theirs:", diff, "theirs strictly finer:", stronger_theirs,
          "own strictly finer:", stronger_own, "key mismatch", len(missing), flush=True)
    print("their C06 bounds:", c06, flush=True)
    res = {"their_bounds": {str(a): b for a, b in sorted(cnt.items())}, "viol_N23": viol, "n_diff": diff,
           "theirs_finer": stronger_theirs, "own_finer": stronger_own, "key_mismatch": sorted(missing)[:20],
           "their_c06": c06, "elapsed_s": round(time.time() - t0, 1)}
    json.dump(res, open(os.path.join(OUT, "c13_closure_stage2.json"), "w"), indent=1)
    json.dump(theirs, open(os.path.join(OUT, "c13_closure_perlaw_theirs.json"), "w"))


def stage3(sample=400, seed=13):
    t0 = time.time()
    per = json.load(open(os.path.join(OUT, "c13_closure_perlaw_own.json")))
    theirs = json.load(open(os.path.join(OUT, "c13_closure_perlaw_theirs.json")))
    bounded = sorted(k for k in per if per[k][0] > 0 or theirs.get(k, 0) > 0)
    rng = random.Random(seed)
    samp = rng.sample(bounded, min(sample, len(bounded)))
    checks = Counter()
    viol = []
    unknown = []
    plan = [(k, 4) for k in bounded] + [(k, N) for k in samp for N in (5, 6, 7)]
    for k, N in plan:
        g_own, g_th = per[k][0], theirs.get(k, 0)
        if (g_own == 0 or g_own % N) or (g_th == 0 or g_th % N):
            # at least one closure claims N cannot be a size
            need = [w for w, g in (("own", g_own), ("theirs", g_th)) if g > 0 and g % N]
            if not need:
                continue
            law = read_law(k.replace("|", "="))
            st, T = sat_model(N, [law], budget=2_000_000)
            checks[(N, st)] += 1
            if st == "SAT":
                viol.append((k, N, g_own, g_th))
            elif st == "UNKNOWN":
                unknown.append((k, N))
    print("stage3 checks (N, status):", dict(checks), "violations", viol[:5], "unknown", len(unknown), flush=True)
    res = {"n_bounded": len(bounded), "sample": len(samp), "checks": {f"{a}:{b}": c for (a, b), c in checks.items()},
           "violations": viol, "unknown": unknown[:50], "elapsed_s": round(time.time() - t0, 1)}
    json.dump(res, open(os.path.join(OUT, "c13_closure_stage3.json"), "w"), indent=1)


if __name__ == "__main__":
    {"stage1": stage1, "stage2": stage2, "stage3": stage3}[sys.argv[1]]()
