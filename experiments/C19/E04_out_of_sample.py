"""EXP-C19-04: out-of-sample tests of the deficit recursion, an O(log^2 n) algorithm, OEIS, asymptotics."""

import math
import random
import time

from lab import oeis
from systems.zeckendorf_game import (FIB, cusenza_bound, deficit_rec, greedy_length_fast, longest_rec, rho)

META = {
    "id": "EXP-C19-04",
    "cycle": "C19",
    "title": "Out-of-sample tests of the conjectured recursion for the longest Zeckendorf game",
    "agent": "Mathematical Skeptic",
    "question": "Does the recursion D(F_j + m) = floor(j^2/4) + D(m) - rho_(j mod 2)(m), inferred from n < 30000, "
                "predict the longest game for n it was not fitted on? How fast is it, and what do L and D look "
                "like asymptotically?",
    "hypothesis": "H-C19-R (out of sample): longest_rec(n) = greedy length for every tested n >= 30000.",
    "assumptions": ["greedy lengths are optimal (Cusenza et al. 2022, Thm 1.2; independently confirmed for n <= 150 "
                    "in EXP-C19-01)", "random samples drawn with a fixed seed"],
    "methodology": "Compare longest_rec(n) with the fast greedy simulation for all n in [30000, 36000), 200 random "
                   "n in [4e4, 1e6), 12 random n in [1e6, 2e7) and 60 numbers F_j + m (j in [20, 30], m < 40); time "
                   "both methods; OEIS novelty checks of L, D, L(F_j), rho_0, rho_1; tabulate "
                   "(phi^2 n - L(n)) / (log_phi n)^2.",
    "falsification": "Any tested n with longest_rec(n) != greedy length.",
    "seed": 1919,
}

PHI = (1 + 5 ** 0.5) / 2


def run():
    rng = random.Random(META["seed"])
    tests = list(range(30000, 36000))
    tests += [rng.randrange(40000, 1_000_000) for _ in range(200)]
    tests += [rng.randrange(1_000_000, 20_000_000) for _ in range(12)]
    fam = []
    for _ in range(60):
        j = rng.randint(20, 30)
        fam.append(FIB[j] + rng.randrange(0, 40))
    tests += fam
    t0 = time.perf_counter()
    mism = []
    greedy_time = 0.0
    for n in tests:
        a = time.perf_counter()
        g = greedy_length_fast(n)
        greedy_time += time.perf_counter() - a
        if longest_rec(n) != g:
            mism.append(n)
    t_tests = time.perf_counter() - t0
    # speed
    bench, bench_times = [], {}
    for n in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
        a = time.perf_counter()
        g = greedy_length_fast(n)
        tg = time.perf_counter() - a
        a = time.perf_counter()
        r = longest_rec(n)
        tr = time.perf_counter() - a
        # wall-clock times go under "timings" (not hashed); before batch 1.1 they were stored here, so no re-run
        # could reproduce the result hash
        bench.append({"n": n, "L": g, "agree": g == r})
        bench_times[f"{n}/greedy_s"] = round(tg, 4)
        bench_times[f"{n}/recursion_s"] = round(tr, 6)
    huge = {str(10 ** e): longest_rec(10 ** e) for e in (12, 18, 30)}
    # OEIS
    Ls = [longest_rec(n) for n in range(1, 41)]
    Ds = [cusenza_bound(n) - longest_rec(n) for n in range(1, 41)]
    LF = [longest_rec(FIB[j]) for j in range(0, 25)]
    seqs = {"L(n), n>=1": Ls, "D(n), n>=1": Ds, "L(F_j), j>=0": LF,
            "rho_0(m), m>=1": [rho(0, m) for m in range(1, 41)], "rho_1(m), m>=1": [rho(1, m) for m in range(1, 41)]}
    look = {}
    for k, s in seqs.items():
        r = oeis.novelty_check(s)
        look[k] = {"status": r["status"], "hits": [h["anumber"] + " " + h["name"][:90] for h in r.get("hits", [])[:3]],
                   "terms": s[:20]}
    # asymptotics
    asym = []
    for e in (3, 4, 5, 6, 7, 9, 12, 18):
        n = 10 ** e
        L = longest_rec(n)
        asym.append({"n": f"1e{e}", "L/n": round(L / n, 9),
                     "(phi^2 n - L)/(log_phi n)^2": round((PHI ** 2 * n - L) / (math.log(n, PHI) ** 2), 4)})
    return {
        "n_tested": len(tests),
        "mismatches": mism[:20],
        "n_mismatches": len(mism),
        "ranges": {"all": [30000, 35999], "random_mid": [40000, 999999], "random_large": [1000000, 19999999],
                   "fibonacci_plus_small": len(fam)},
        "benchmark": bench,
        "L_huge_conjectural": huge,
        "oeis": look,
        "asymptotics": asym,
        "timings": {"tests_s": round(t_tests, 1), "greedy_total_s": round(greedy_time, 1), **bench_times},
        "summary": [
            f"recursion vs greedy on {len(tests)} out-of-sample n (all of [30000, 36000), 200 random < 1e6, "
            f"12 random < 2e7, 60 of the form F_j + m): {len(mism)} mismatches",
            "benchmark n = 1e4..1e7: recursion and greedy simulation agree: " + str(all(b["agree"] for b in bench)) +
            " (wall-clock times under 'timings')",
            "OEIS: " + "; ".join(f"{k}: {v['status']}" for k, v in look.items()),
            f"(phi^2 n - L(n)) / (log_phi n)^2 at n = 1e3..1e18: {[a['(phi^2 n - L)/(log_phi n)^2'] for a in asym]}",
        ],
    }
