"""EXP-C13-08: computer-assisted proofs of finite anchored spectra by offset congruence closure."""

import itertools
import random
import time
from collections import Counter

from systems.anchored import (affine_roots, affine_spectrum, affine_system, anchored_status, divisors,
                              enumerate_laws, law_from_key, law_str, offset_closure_bound)
from systems.magma import fill, parse, shapes, to_str

META = {
    "id": "EXP-C13-08",
    "cycle": "C13",
    "title": "Finite spectra proved by offset congruence closure (and a soundness test against SAT)",
    "agent": "Formal Verifier",
    "question": "Can the sound closure procedure of systems/anchored.py (law instances at small elements, the anchor, "
                "functionality of the table, union-find with integer offsets) prove N | g for the finite-spectrum "
                "laws of CLM-C06-10 and for the laws of the 3-variable family? Is it ever contradicted by SAT data?",
    "hypothesis": "H-C13-6: for 16 of the 17 laws of CLM-C06-10 the closure proves N | 3 resp. N | 2 (with the affine "
                  "models this gives the exact spectra {1,3}, {1,2}); a sizeable part of the 18,581-law family gets "
                  "an exact finite spectrum Div(g); no bound is ever contradicted by a SAT model.",
    "assumptions": ["C06 laws: values 0..4, -1, -2, 8 rounds, instances also at the first 10 table entries",
                    "family: values 0..3, -1, 4 rounds, constants only (cheap setting)",
                    "soundness test: all 253 one-variable laws with <= 5 leaves (SAT, N <= 12), 150 random "
                    "2-variable laws (seed 8, SAT, N <= 7) and 200 random 3-variable laws with a bound (SAT, N <= 6): "
                    "every N with a model must divide the bound"],
    "methodology": "offset_closure_bound(); a law whose bound g > 0 has affine models for every divisor of g has "
                   "spectrum exactly Div(g) (upper bound from the closure, lower bound from the affine tables).",
    "falsification": "A SAT model of size N with N not dividing the derived bound (an unsound closure step).",
    "seed": 8,
}

C06_13 = ["x(yz)=((zx)x)y", "x(yz)=((zx)y)x", "x(yz)=((zy)x)x", "(xy)z=y((zx)y)", "(xy)z=y((zy)x)",
          "(xy)z=z((yx)z)", "(xy)z=z((yz)x)"]
C06_12 = ["x(yz)=y((yx)z)", "x(yz)=((xx)y)z", "x(yz)=((xx)z)y", "x(yz)=((xy)x)z", "x(yz)=((xy)y)z",
          "x(yz)=((xy)z)x", "x(yz)=((xy)z)y", "x(yz)=((xz)x)y", "x(yz)=((xz)y)x", "x(yz)=((xz)y)y"]


def _law(s):
    a, b = s.split("=")
    return parse(a), parse(b)


def exact_divisor_spectrum(law, g):
    """True if every divisor of g > 0 admits an affine model (so the spectrum is exactly Div(g))."""
    sysm = affine_system(law)
    return g > 0 and all((affine_roots(sysm, d) if sysm else True) for d in divisors(g))


def run():
    t0 = time.perf_counter()
    rng = random.Random(META["seed"])
    # (a) the conjecture CLM-C06-10
    c06 = []
    for conj, laws in (("{1,3}", C06_13), ("{1,2}", C06_12)):
        for L in laws:
            law = _law(L)
            g = offset_closure_bound([law], values=(0, 1, 2, 3, 4, -1, -2), rounds=8, max_symbols=20000,
                                     symbol_values=10)
            c06.append({"law": L, "conjectured": conj, "bound": g, "exact": exact_divisor_spectrum(law, g)})
    proved = [r["law"] for r in c06 if r["exact"] and str(set(divisors(r["bound"]))).replace(" ", "") ==
              r["conjectured"]]
    # (b) the whole 3-variable family
    fam = enumerate_laws(("x", "y", "z"), 4)
    bounds = Counter()
    exact = Counter()
    bounded = []
    for k in fam:
        law = law_from_key(k)
        g = offset_closure_bound([law], values=(0, 1, 2, 3, -1), rounds=4)
        bounds[g] += 1
        if g > 0:
            bounded.append((k, g))
        if g > 0 and exact_divisor_spectrum(law, g):
            exact[g] += 1
    # (c) soundness test against SAT
    viol = []
    tested = 0
    one = []
    for k in range(0, 5):
        for sh in shapes(k):
            one.append(fill(sh, ["x"] * (k + 1)))
    laws_soundness = [(f"{to_str(a)} = {to_str(b)}", (a, b), 12) for a, b in itertools.combinations(one, 2)]
    two = rng.sample(enumerate_laws(("x", "y"), 4), 150)
    laws_soundness += [(law_str(k), law_from_key(k), 7) for k in two]
    fam_sample = rng.sample(bounded, 200)
    laws_soundness += [(law_str(k), law_from_key(k), 6) for k, _ in fam_sample]
    nontrivial_bounds = 0
    for name, law, nmax in laws_soundness:
        g = offset_closure_bound([law], values=(0, 1, 2, 3, 4, -1, -2), rounds=6, symbol_values=4)
        if g == 0:
            continue
        nontrivial_bounds += 1
        sysm = affine_system(law)
        for n in range(2, nmax + 1):
            if g % n == 0:
                continue
            tested += 1
            if (affine_roots(sysm, n) if sysm else True):
                viol.append({"law": name, "N": n, "bound": g, "how": "affine"})
                continue
            st, _ = anchored_status([law], n, budget=300_000)
            if st == "SAT":
                viol.append({"law": name, "N": n, "bound": g, "how": "sat"})
    return {"c06_laws": c06, "c06_proved_exactly": proved,
            "family_bounds": {str(k): v for k, v in sorted(bounds.items())},
            "family_exact_divisor_spectra": {str(k): v for k, v in sorted(exact.items())},
            "family_size": len(fam),
            "soundness": {"laws": len(laws_soundness), "with_bound": nontrivial_bounds, "checks": tested,
                          "violations": viol},
            "timings": {"total_s": round(time.perf_counter() - t0, 1)},
            "summary": [f"CLM-C06-10: exact spectrum proved for {len(proved)} of 17 laws; not proved: "
                        f"{[r['law'] for r in c06 if r['law'] not in proved]}",
                        f"3-variable family ({len(fam)} laws): bound found for {sum(v for k, v in bounds.items() if k)} "
                        f"(g=1: {bounds.get(1, 0)}); exact spectrum Div(g) proved for {sum(exact.values())} "
                        f"{dict(sorted(exact.items())[:8])}",
                        f"soundness: {len(laws_soundness)} laws, {nontrivial_bounds} with a bound, {tested} sizes N "
                        f"not dividing the bound checked by SAT/affine; violations {len(viol)}"]}
