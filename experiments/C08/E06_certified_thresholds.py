"""EXP-C08-06: re-test the associativity atlas with a stronger, certificate-producing search.

Method (after the Historian's check, reviews/historian_checks/c08_thresholds.py).  For a recurrence
G_k = a_1 G_{k-1} + ... + a_d G_{k-d}, the map nu(n) = sum_i d_i x^i in Z[x]/(x^d - a_1 x^(d-1) - ... - a_d)
is injective on greedy expansions (x^i -> G_i recovers n).  If nu(a o_s b) = x^s nu(a) nu(b) held for ALL
a, b, then o_s would be associative.  Pairs violating the identity are candidates; an explicit triple with
(a o b) o c != a o (b o c) certifies non-associativity.  "No failure found" is only computational support.
"""

import random

from systems.circle import BaseSequence, two_term

META = {
    "id": "EXP-C08-06",
    "cycle": "C08",
    "title": "Certified non-associativity: re-testing the circle-product thresholds and the 90 quadratic rows",
    "agent": "Mathematical Skeptic",
    "question": "Which associativity claims of EXP-C08-02..04 survive a stronger search (embedding identity on all "
                "pairs a <= b < 200, 2000 random pairs below 10^6, the literature example of Ambroz-Frougny-"
                "Masakova-Pelantova for tribonacci), with explicit counterexamples for every failure?",
    "hypothesis": "The Historian's audit (reviews/historian_C03_C10.md) predicts failures at tribonacci s = 3, "
                  "G(k+1) = G(k) + G(k-2) at s = 10, (2,2;1,2) at s = 4, 4-bonacci at s = 6, (3,3;1,5) at s = 9, "
                  "(4,3;1,5) at s = 4 and (3,3;1,2) at s = 7, all listed as associative before.",
    "assumptions": ["pairs a <= b < 300, plus 4000 seeded random pairs in [1, 10^6), plus the literature example and "
                    "the three pairs reported by the Historian",
                    "for each failing pair, c is searched in [1, 300)", "shifts 0..12"],
    "methodology": "For every sequence and shift: test the embedding identity on the pair set; on the first failing "
                   "pair search an explicit triple; record a certified counterexample or 'no failure found'.",
    "falsification": "A shift listed as associative in EXP-C08-02..04 with a certified counterexample (refutes the "
                     "earlier measurement), or a certified counterexample for Fibonacci with s >= 2 (would "
                     "contradict the Lean theorem of CLM-C08-01).",
    "seed": 806,
}

AFMP_TRIBONACCI = [(10016, 10016)]     # the word 110100100101101 of Ambroz-Frougny-Masakova-Pelantova (2003)
HISTORIAN_PAIRS = [(78, 248), (50, 96), (41, 280)]   # counterexamples reported in reviews/historian_C03_C10.md


def checker(S: BaseSequence):
    coeffs = S.coeffs
    d = len(coeffs)

    def mul(u, v):
        p = [0] * (2 * d - 1)
        for i, x in enumerate(u):
            if x:
                for j, y in enumerate(v):
                    p[i + j] += x * y
        for k in range(2 * d - 2, d - 1, -1):
            c = p[k]
            p[k] = 0
            if c:
                for t, a in enumerate(coeffs, start=1):
                    p[k - t] += a * c
        return tuple(p[:d])

    X = tuple([0, 1] + [0] * (d - 2)) if d > 1 else (coeffs[0],)
    pw = [tuple([1] + [0] * (d - 1))]
    for _ in range(200):
        pw.append(mul(pw[-1], X))
    cache = {}

    def nu(n):
        if n not in cache:
            u = [0] * d
            for i, dg in S.greedy(n).items():
                for t in range(d):
                    u[t] += dg * pw[i][t]
            cache[n] = tuple(u)
        return cache[n]

    def test(s, pairs):
        for a, b in pairs:
            if nu(S.circle(a, b, s)) != mul(pw[s], mul(nu(a), nu(b))):
                for c in range(1, 300):
                    L = S.circle(S.circle(a, b, s), c, s)
                    R = S.circle(a, S.circle(b, c, s), s)
                    if L != R:
                        return {"status": "NOT ASSOCIATIVE", "triple": [a, b, c], "lhs": L, "rhs": R}
                return {"status": "embedding fails, no c < 300 found", "pair": [a, b]}
        return {"status": "no failure found"}

    return test


def run():
    rng = random.Random(META["seed"])
    base_pairs = [(a, b) for a in range(1, 300) for b in range(a, 300)]
    rand_pairs = [(rng.randrange(1, 10 ** 6), rng.randrange(1, 10 ** 6)) for _ in range(4000)]
    pairs = HISTORIAN_PAIRS + base_pairs + rand_pairs
    named = [
        ("Fibonacci 1,2", BaseSequence("Fibonacci", [1, 2], (1, 1)), range(0, 8), []),
        ("Pell 1,2,5", BaseSequence("Pell", [1, 2], (2, 1)), range(0, 6), []),
        ("(2,2) 1,2", BaseSequence("(2,2)", [1, 2], (2, 2)), range(2, 9), []),
        ("tribonacci 1,2,4", BaseSequence("trib", [1, 2, 4], (1, 1, 1)), range(2, 10), AFMP_TRIBONACCI),
        ("4-bonacci 1,2,4,8", BaseSequence("tetra", [1, 2, 4, 8], (1, 1, 1, 1)), range(4, 11), []),
        ("G(k+1)=G(k)+G(k-2) 1,2,3", BaseSequence("narayana", [1, 2, 3], (1, 0, 1)), range(8, 13), []),
        ("(3,3) 1,5", BaseSequence("(3,3)15", [1, 5], (3, 3)), range(8, 13), []),
    ]
    thresholds = {}
    for name, S, shifts, extra in named:
        test = checker(S)
        res = {s: test(s, extra + pairs) for s in shifts}
        fails = [s for s, r in res.items() if r["status"] == "NOT ASSOCIATIVE"]
        ok = [s for s, r in res.items() if r["status"] == "no failure found"]
        thresholds[name] = {"by_shift": {str(s): r for s, r in res.items()},
                            "largest_certified_failure": max(fails) if fails else None,
                            "smallest_shift_without_failure_above_all_failures":
                                min([s for s in ok if all(s > f for f in fails)], default=None)}
    quad = []
    import numpy as np
    for p in range(1, 6):
        for q in (-3, -2, -1, 1, 2, 3):          # the same 90 rows as EXP-C08-04
            r = np.roots([1, -p, -q])
            if np.iscomplexobj(r) and np.max(np.abs(np.imag(r))) > 1e-12:
                continue
            r = sorted(np.real(r), key=abs)
            beta, alpha = float(r[0]), float(r[1])
            if not (alpha > 1 and abs(beta) < 1 - 1e-9) or abs(beta) < 1e-12:
                continue
            for g1 in range(2, 7):
                try:
                    S = BaseSequence(f"G(k+1)={p}G(k)+({q})G(k-1); 1,{g1}", [1, g1], (p, q))
                    S.extend(60)
                except (ValueError, AssertionError):
                    continue
                if any(S.G[i] * S.G[i] == S.G[i - 1] * S.G[i + 1] for i in range(1, 6)):
                    continue
                test = checker(S)
                res = {s: test(s, pairs[:12000]) for s in range(0, 11)}
                fails = [s for s, r_ in res.items() if r_["status"] == "NOT ASSOCIATIVE"]
                ok = [s for s, r_ in res.items() if r_["status"] == "no failure found"]
                upward = all(not (s1 < s2 and s1 in ok and s2 in fails) for s1 in range(11) for s2 in range(11))
                quad.append({"p": p, "q": q, "g1": g1, "beta": round(beta, 6), "no_failure_shifts": ok,
                             "certified_failures": fails, "upward_closed_on_0_10": upward,
                             "canonical": g1 in (p, p + 1),
                             "examples": {str(s): res[s].get("triple") for s in fails[-2:]}})
    old = {}
    import json
    from pathlib import Path
    prev = json.loads(Path("results/EXP-C08-04.json").read_text())["results"]["rows"]
    for row in prev:
        old[row["G"]] = row["associative_shifts"]
    contradicted = []
    for r in quad:
        key = f"G(k+1)={r['p']}G(k)+({r['q']})G(k-1); 1,{r['g1']}"
        if key in old:
            bad = sorted(set(old[key]) & set(r["certified_failures"]))
            if bad:
                contradicted.append({"G": key, "listed_associative_but_certified_failing": bad})
    non_monotone = [r for r in quad if not r["upward_closed_on_0_10"]]
    return {
        "thresholds": thresholds,
        "quadratic_rows": quad,
        "earlier_rows_contradicted": contradicted,
        "non_monotone_rows": [{"p": r["p"], "q": r["q"], "g1": r["g1"], "beta": r["beta"],
                               "canonical": r["canonical"], "no_failure_shifts": r["no_failure_shifts"]}
                              for r in non_monotone],
        "positive_beta_rows": sum(1 for r in quad if r["beta"] > 0),
        "positive_beta_non_monotone": sum(1 for r in non_monotone if r["beta"] > 0),
        "summary": [
            "thresholds (largest certified failing shift / smallest later shift without failure): " +
            "; ".join(f"{k}: {v['largest_certified_failure']}/{v['smallest_shift_without_failure_above_all_failures']}"
                      for k, v in thresholds.items()),
            f"quadratic rows re-tested (the 90 of EXP-C08-04): {len(quad)}; rows whose earlier 'associative' shifts "
            f"are now certified to fail: {len(contradicted)}; still non-monotone on 0..10: {len(non_monotone)} "
            f"(canonical: {sum(r['canonical'] for r in non_monotone)}, positive beta: "
            f"{sum(1 for r in non_monotone if r['beta'] > 0)} of {sum(1 for r in quad if r['beta'] > 0)} rows)",
        ],
    }
