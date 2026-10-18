"""EXP-C13-06: H-C13-1 - is every anchored spectrum closed under divisors? (falsification search)"""

import random
import time

from systems.anchored import (affine_roots, affine_system, anchored_status, divisors, enumerate_laws, law_from_key,
                              law_str, system_of_laws, zero_modulus)

META = {
    "id": "EXP-C13-06",
    "cycle": "C13",
    "title": "Divisor-closure of anchored spectra: all 2-variable laws with <= 4 leaves per side, N <= 10",
    "agent": "Mathematical Skeptic",
    "question": "Is there a law with an anchored model of some size N <= 10 but none of some size d | N?",
    "hypothesis": "H-C13-1 (bold): every anchored spectrum is closed under divisors.",
    "assumptions": ["laws over {x,y} with at most 4 leaves per side, up to renaming and exchange of sides",
                    "sizes 2, 3, 5 always decided; a composite N in {4, 6, 8, 9, 10} is decided only when one of "
                    "its proper divisors is UNSAT (otherwise no violation is possible at N)",
                    "affine models decide SAT without a solver; conflict budget 2,000,000; UNKNOWN recorded"],
    "methodology": "For each law: zero-substitution filter (N | m); affine roots; otherwise MagmaSAT with the anchor. "
                   "Report every pair (N, d) with N SAT and d | N UNSAT.",
    "falsification": "Any such pair.",
}

ORDER = [2, 3, 5, 4, 6, 8, 9, 10]


def decide(law, sysm, n, m):
    if m is not None and m != 0 and m % n != 0:
        return "UNSAT", "zero"
    if affine_roots(sysm, n):
        return "SAT", "affine"
    st, _ = anchored_status([law], n)
    return st, "sat"


def run():
    t0 = time.perf_counter()
    keys = enumerate_laws(("x", "y"), 4)
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
            "unknown": unknown, "calls": calls, "rows": rows, "runtime_s": round(time.perf_counter() - t0, 1),
            "summary": [f"{len(keys)} laws; {len(rows)} have a model of some size 2..10",
                        f"divisor-closure violations: {len(violations)} {[v['law'] for v in violations[:5]]}",
                        f"UNKNOWN: {len(unknown)}; decisions {calls}"]}
