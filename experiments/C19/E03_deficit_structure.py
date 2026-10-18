"""EXP-C19-03: the deficit D(n) = B(n) - L(n): Fibonacci inputs, two summands, failed additive models, a recursion."""

import time
from collections import defaultdict
from fractions import Fraction

from systems.zeckendorf_game import (FIB, cusenza_bound, deficit_rec, greedy_length_fast, lazy_digits, rho,
                                     zeckendorf_digits)

META = {
    "id": "EXP-C19-03",
    "cycle": "C19",
    "title": "Structure of the deficit D(n) = B(n) - L(n) of the longest Zeckendorf game",
    "agent": "Mathematical Inventor",
    "question": "How does D(n) = B(n) - L(n) (B = sum_i a_i delta_i, Cusenza et al.) depend on the Zeckendorf "
                "digits of n?",
    "hypothesis": "H-C19-F: D(F at level j) = floor(j^2/4). H-C19-1 (bold): D is additive over Zeckendorf summands "
                  "up to a correction for consecutive pairs only. H-C19-2: the effect of the top summand depends "
                  "only on the two highest levels. H-C19-3 (bold): D is additive over the runs of the lazy "
                  "representation. H-C19-R: D(F_j + m) = floor(j^2/4) + D(m) - rho_(j mod 2)(m) with the explicit "
                  "rho of systems/zeckendorf_game.py (inferred from n < 30000; out-of-sample tests in EXP-C19-04).",
    "assumptions": ["L(n) computed by the split-first greedy strategy, which is optimal by Cusenza et al. "
                    "(2022, Thm 1.2) and was confirmed independently for n <= 150 (EXP-C19-01)",
                    "levels j: F = 1, 2, 3, 5, ... (level j carries FIB[j])"],
    "methodology": "Greedy lengths for all n < 30000 and for Fibonacci inputs up to level 33; two-summand values "
                   "for j <= 24; exact rational rank test for the lazy-run model on n < 160; comparison of the "
                   "recursion with the greedy on n < 30000.",
    "falsification": "Any n contradicting H-C19-F or H-C19-R; the additive models are refuted by explicit "
                     "counterexamples or inconsistent linear systems.",
}

N = 30000


def levels(n):
    d = zeckendorf_digits(n)
    return [k for k in range(len(d) - 1, -1, -1) if d[k]]


def h(k):
    return k * k // 4


def R2(j, i):
    if i == 0:
        return 1
    return (i + 1) ** 2 // 4 + 1 if (j - i) % 2 else i * i // 4 + 2


def lazy_runs(n):
    d, out, k = lazy_digits(n), [], 0
    while k < len(d):
        if d[k]:
            s = k
            while k < len(d) and d[k]:
                k += 1
            out.append((s, k - s))
        else:
            k += 1
    return out


def rank(rows, ncols):
    """Exact rank over Q (Gaussian elimination with Fractions)."""
    M = [[Fraction(x) for x in r] for r in rows]
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def run():
    t0 = time.perf_counter()
    L = [greedy_length_fast(n) for n in range(N)]
    D = [cusenza_bound(n) - L[n] for n in range(N)]
    t_greedy = time.perf_counter() - t0
    # Fibonacci inputs
    fib_bad = [j for j in range(34) if cusenza_bound(FIB[j]) - greedy_length_fast(FIB[j]) != h(j)]
    # two summands
    two_bad, two_checked = [], 0
    for j in range(2, 25):
        for i in range(0, j - 1):
            n = FIB[j] + FIB[i]
            two_checked += 1
            if cusenza_bound(n) - greedy_length_fast(n) != h(j) + h(i) - R2(j, i):
                two_bad.append((j, i))
    # H-C19-1: consecutive-pair model
    pair_bad = []
    for n in range(1, N):
        lv = levels(n)
        pred = sum(h(j) for j in lv) - sum(R2(a, b) for a, b in zip(lv, lv[1:]))
        if pred != D[n]:
            pair_bad.append(n)
    # H-C19-2: top-summand effect depends on (top, next)
    tab = defaultdict(set)
    for n in range(1, N):
        lv = levels(n)
        if len(lv) >= 2:
            tab[(lv[0], lv[1])].add(D[n] - D[n - FIB[lv[0]]])
    amb = {str(k): sorted(v) for k, v in tab.items() if len(v) > 1}
    first_amb = min(((k, v) for k, v in tab.items() if len(v) > 1), key=lambda kv: kv[0][0])
    # H-C19-3: lazy-run additivity, exact rank test on n < 160
    data = [(lazy_runs(n), D[n]) for n in range(1, 160)]
    runs = sorted({r for rs, _ in data for r in rs})
    idx = {r: c for c, r in enumerate(runs)}
    A = [[sum(1 for r in rs if idx[r] == c) for c in range(len(runs))] for rs, _ in data]
    Ab = [row + [dv] for row, (_, dv) in zip(A, data)]
    rA, rAb = rank(A, len(runs)), rank(Ab, len(runs) + 1)
    # H-C19-R: the recursion, in-sample
    rec_bad = [n for n in range(N) if deficit_rec(n) != D[n]]
    # side facts
    def top(n):
        return max(k for k in range(len(FIB)) if FIB[k] <= n)
    bound_top_bad = [n for n in range(1, N) if D[n] > h(top(n))]
    mono_bad = [n for n in range(1, N - 1) if L[n + 1] <= L[n]]
    return {
        "fibonacci_inputs_violations_j_le_33": fib_bad,
        "two_summand_law_checked": two_checked,
        "two_summand_violations": two_bad,
        "consecutive_pair_model_mismatches": len(pair_bad),
        "consecutive_pair_first_counterexample": {"n": pair_bad[0], "levels": levels(pair_bad[0]),
                                                  "D": D[pair_bad[0]]} if pair_bad else None,
        "top_next_ambiguous_keys": len(amb),
        "top_next_first_ambiguity": {"top_next": list(first_amb[0]), "values": sorted(first_amb[1])},
        "lazy_run_model": {"n_range": [1, 159], "distinct_runs": len(runs), "rank_A": rA, "rank_A_b": rAb,
                           "consistent": rA == rAb},
        "recursion_in_sample_mismatches": len(rec_bad),
        "rho_even_first": [rho(0, m) for m in range(40)],
        "rho_odd_first": [rho(1, m) for m in range(40)],
        "D_le_floor_top2_over4_violations": len(bound_top_bad),
        "L_strictly_increasing_violations_1_le_n": mono_bad[:10],
        "L_first": L[:41],
        "D_first": D[:41],
        "timings": {"greedy_all_n_s": round(t_greedy, 1), "total_s": round(time.perf_counter() - t0, 1)},
        "summary": [
            f"D(F) = floor(j^2/4) for the Fibonacci input at level j, j <= 33: violations {fib_bad}",
            f"two-summand law D(F_j + F_i) = h(j) + h(i) - R(j,i): {two_checked} pairs (j <= 24), violations "
            f"{len(two_bad)}",
            f"H-C19-1 (consecutive-pair additivity) refuted: {len(pair_bad)} mismatches for n < {N}, first n = "
            f"{pair_bad[0] if pair_bad else None}",
            f"H-C19-2 refuted: {len(amb)} (top, next) keys with several values, e.g. {first_amb[0]} -> "
            f"{sorted(first_amb[1])}",
            f"H-C19-3 (lazy-run additivity) on n < 160: rank {rA} vs augmented {rAb} -> "
            f"{'consistent' if rA == rAb else 'inconsistent (refuted)'}",
            f"recursion H-C19-R reproduces D for all n < {N} (in-sample): mismatches {len(rec_bad)}",
            f"D(n) <= floor(j^2/4) (j top level): violations {len(bound_top_bad)}; L strictly increasing for "
            f"n >= 1: violations {len(mono_bad)}",
        ],
    }
