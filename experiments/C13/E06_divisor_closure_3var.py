"""EXP-C13-06: H-C13-1 continued - divisor-closure for a sample of 3-variable laws and for pairs of laws."""

import random
import time

from systems.anchored import (affine_roots, affine_spectrum, affine_system, anchored_status, divisors,
                              enumerate_laws, law_from_key, law_str, system_of_laws, zero_modulus)

META = {
    "id": "EXP-C13-06",
    "cycle": "C13",
    "title": "Divisor-closure of anchored spectra: 150 random 3-variable laws and 80 random pairs of 2-variable laws",
    "agent": "Mathematical Skeptic",
    "question": "Does any 3-variable law (<= 4 leaves per side) or any conjunction of two 2-variable laws have an "
                "anchored model of a size N but not of some divisor d of N?",
    "hypothesis": "H-C13-1 (bold): every anchored spectrum is closed under divisors.",
    "assumptions": ["150 laws sampled (seed 13) among the 3-variable laws whose affine spectrum is not all N and "
                    "which survive the zero filter; sizes 2, 3, 5 always decided, composite 4, 6, 8 only when a "
                    "proper divisor is UNSAT", "80 pairs of 2-variable laws (<= 4 leaves per side, seed 13); sizes "
                    "2..8 with the same pruning", "conflict budget 100,000; UNKNOWN recorded"],
    "methodology": "As EXP-C13-05: zero filter, affine roots, SAT; violations are pairs (N, d), N SAT, d | N UNSAT.",
    "falsification": "Any such pair.",
    "seed": 13,
}


def decide(laws, sysm, n, m):
    if m is not None and m % n != 0:
        return "UNSAT", "zero"
    if affine_roots(sysm, n) if sysm else True:
        return "SAT", "affine"
    st, _ = anchored_status(laws, n, budget=100_000)
    return st, "sat"


def profile(laws, order, m):
    sysm = system_of_laws(laws)
    st = {1: "SAT"}
    calls = {"zero": 0, "affine": 0, "sat": 0, "skipped": 0}
    for n in order:
        props = divisors(n)[1:-1]
        if props and all(st.get(d) == "SAT" for d in props):
            st[n] = "not needed"
            calls["skipped"] += 1
            continue
        st[n], how = decide(laws, sysm, n, m)
        calls[how] += 1
    viol = [(n, d) for n in order if st.get(n) == "SAT" for d in divisors(n)[1:-1] if st.get(d) == "UNSAT"]
    return st, viol, calls


def _zero_of_laws(laws):
    ms = [zero_modulus(l) for l in laws]
    if any(m == 1 for m in ms):
        return 1
    from math import gcd
    g = None
    for m in ms:
        if m is not None:
            g = m if g is None else gcd(g, m)
    return g


def run():
    rng = random.Random(META["seed"])
    t0 = time.perf_counter()
    pool = []
    for k in enumerate_laws(("x", "y", "z"), 4):
        law = law_from_key(k)
        if zero_modulus(law) == 1:
            continue
        if len(affine_spectrum(affine_system(law), 12)) == 12:
            continue
        pool.append(k)
    sample = rng.sample(pool, 150)
    res3, viol3, unk3 = [], [], []
    tot = {"zero": 0, "affine": 0, "sat": 0, "skipped": 0}
    for k in sample:
        law = law_from_key(k)
        st, v, calls = profile([law], [2, 3, 5, 4, 6, 8], zero_modulus(law))
        for c in calls:
            tot[c] += calls[c]
        if v:
            viol3.append({"law": law_str(k), "pairs": v, "status": st})
        if "UNKNOWN" in st.values():
            unk3.append(law_str(k))
        if any(st.get(n) == "SAT" for n in (2, 3, 4, 5, 6, 8)):
            res3.append({"law": law_str(k), "status": st})
    two = [k for k in enumerate_laws(("x", "y"), 4) if zero_modulus(law_from_key(k)) != 1]
    pairs = [tuple(rng.sample(two, 2)) for _ in range(80)]
    resp, violp, unkp = [], [], []
    for k1, k2 in pairs:
        laws = [law_from_key(k1), law_from_key(k2)]
        m = _zero_of_laws(laws)
        if m == 1:
            continue
        st, v, calls = profile(laws, [2, 3, 5, 4, 6, 8], m)
        for c in calls:
            tot[c] += calls[c]
        name = f"{law_str(k1)} & {law_str(k2)}"
        if v:
            violp.append({"laws": name, "pairs": v, "status": st})
        if "UNKNOWN" in st.values():
            unkp.append(name)
        if any(st.get(n) == "SAT" for n in (2, 3, 4, 5, 6, 8)):
            resp.append({"laws": name, "status": st})
    return {"pool_size": len(pool), "sample": [law_str(k) for k in sample], "violations_3var": viol3,
            "violations_pairs": violp, "unknown_3var": unk3, "unknown_pairs": unkp, "with_models_3var": res3,
            "with_models_pairs": resp, "calls": tot, "runtime_s": round(time.perf_counter() - t0, 1),
            "summary": [f"3-var: {len(sample)} of {len(pool)} candidate laws; {len(res3)} with a model of size 2..8; "
                        f"violations {len(viol3)} {[v['law'] for v in viol3[:4]]}; UNKNOWN {len(unk3)}",
                        f"pairs: 80; {len(resp)} with a model of size 2..8; violations {len(violp)} "
                        f"{[v['laws'] for v in violp[:3]]}; UNKNOWN {len(unkp)}", f"decisions {tot}"]}
