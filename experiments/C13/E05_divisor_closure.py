"""EXP-C13-05: H-C13-1 - is every anchored spectrum closed under divisors? (falsification search)"""

import random
import time

from systems.anchored import (affine_roots, affine_system, anchored_status, divisors, enumerate_laws, law_from_key,
                              law_str, system_of_laws, zero_modulus)

META = {
    "id": "EXP-C13-05",
    "cycle": "C13",
    "title": "Divisor-closure of anchored spectra: 300 random 2-variable laws with <= 4 leaves per side, N <= 9",
    "agent": "Mathematical Skeptic",
    "question": "Is there a law with an anchored model of some size N <= 9 but none of some size d | N?",
    "hypothesis": "H-C13-1 (bold): every anchored spectrum is closed under divisors.",
    "assumptions": ["300 laws sampled (seed 5) from the 2601 laws over {x,y} with at most 4 leaves per side (up to "
                    "renaming and exchange of sides); a run with 600 laws, N <= 10 and budget 2,000,000 was stopped "
                    "after 22 CPU-minutes (hard UNSAT instances at N = 9, 10)",
                    "sizes 2, 3, 5 always decided; a composite N in {4, 6, 8, 9} is decided only when one of "
                    "its proper divisors is UNSAT (otherwise no violation is possible at N)",
                    "affine models decide SAT without a solver; conflict budget 200,000; UNKNOWN recorded"],
    "methodology": "For each law: zero-substitution filter (N | m); affine roots; otherwise MagmaSAT with the anchor. "
                   "Report every pair (N, d) with N SAT and d | N UNSAT.",
    "falsification": "Any such pair.",
    "seed": 5,
}

ORDER = [2, 3, 5, 4, 6, 8, 9]


def decide(law, sysm, n, m):
    if m is not None and m != 0 and m % n != 0:
        return "UNSAT", "zero"
    if affine_roots(sysm, n):
        return "SAT", "affine"
    st, _ = anchored_status([law], n, budget=200_000)
    return st, "sat"


def run():
    t0 = time.perf_counter()
    keys = random.Random(META["seed"]).sample(enumerate_laws(("x", "y"), 4), 300)
    rows, violations, unknown = [], [], []
    calls = {"zero": 0, "affine": 0, "sat": 0, "skipped": 0}
    for k in keys:
        law = law_from_key(k)
        m = zero_modulus(law)
        if m == 1:
            calls["zero"] += 1
            continue
        sysm = affine_system(law)
        st = {1: "SAT"}
        for n in ORDER:
            props = [d for d in divisors(n)[1:-1]]
            if props and all(st.get(d) == "SAT" for d in props):
                st[n] = "not needed"
                calls["skipped"] += 1
                continue
            st[n], how = decide(law, sysm, n, m)
            calls[how] += 1
        v = [(n, d) for n in ORDER if st.get(n) == "SAT" for d in divisors(n)[1:-1] if st.get(d) == "UNSAT"]
        if v:
            violations.append({"law": law_str(k), "pairs": v, "status": st})
        if any(x == "UNKNOWN" for x in st.values()):
            unknown.append(law_str(k))
        if any(st.get(n) == "SAT" for n in ORDER):
            rows.append({"law": law_str(k), "status": st})
    return {"n_laws": len(keys), "n_with_nontrivial_models": len(rows), "violations": violations,
            "unknown": unknown, "calls": calls, "rows": rows, "timings": {"total_s": round(time.perf_counter() - t0, 1)},
            "summary": [f"{len(keys)} sampled laws; {len(rows)} have a model of some size 2..9",
                        f"divisor-closure violations: {len(violations)} {[v['law'] for v in violations[:5]]}",
                        f"UNKNOWN: {len(unknown)}; decisions {calls}"]}
