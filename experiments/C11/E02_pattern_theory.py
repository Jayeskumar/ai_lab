"""EXP-C11-02: growth rates of pattern-terminated codes; which terminator is best, and where."""

import itertools

from lab import oeis
from systems.codes import EliasDelta, EliasGamma, EliasOmega, FibonacciC1, Levenshtein, PatternCode, autocorrelation, growth_rate

META = {
    "id": "EXP-C11-02",
    "cycle": "C11",
    "title": "Pattern-terminated codes: growth rates, the all-ones maximum, and the best terminator per range",
    "agent": "Mathematical Explorer",
    "question": "How does the terminator pattern p control the code T_p? Is 1^k best among patterns of length k?",
    "hypothesis": "H-C11-1: among binary patterns of length k, exactly 1^k and 0^k maximise the growth rate "
                  "lambda_p (hence the asymptotic efficiency 1/log2 lambda_p). H-C11-2 (bold, inventor): for every "
                  "n beyond a small threshold, the best length-k terminator is 1^k. H-C11-3: unbordered patterns of "
                  "length k have lambda equal to the (k-1)-bonacci constant.",
    "assumptions": ["all binary patterns of length 2..10 (2044 patterns)", "codeword counts by exact dynamic "
                    "programming (big integers), growth rates from the denominator x^k + (1-2x) c_p(x)",
                    "range analysis for n <= 2^64"],
    "methodology": "Compute lambda_p two ways (polynomial root; count ratio at length 400); rank patterns; compare "
                   "cumulative codeword counts of 1^k with unbordered patterns; compute, for every n <= 2^64, the "
                   "pattern of length <= 8 giving the shortest codeword (envelope) and crossover points against "
                   "Elias gamma/delta/omega/Levenshtein; OEIS checks of count sequences.",
    "falsification": "A length-k pattern other than 0^k, 1^k with lambda >= lambda_(1^k); a range of large n where a "
                     "pattern beats 1^k of the same length (refutes H-C11-2).",
}


def bonacci(k):
    import numpy as np
    r = np.roots([1] + [-1] * k)
    return max(x.real for x in r if abs(x.imag) < 1e-9)


def run():
    lam, check_ratio = {}, {}
    for k in range(2, 11):
        for bits in itertools.product("01", repeat=k):
            p = "".join(bits)
            lam[p] = growth_rate(p)
    # numerical cross-check of the root formula against count ratios for k <= 6
    for k in range(2, 7):
        for bits in itertools.product("01", repeat=k):
            p = "".join(bits)
            c = PatternCode(p, max_len=400).count
            if lam[p] > 1.05:
                check_ratio[p] = abs(c[400] / c[399] - lam[p])
    h1_viol = []
    best_by_k = {}
    for k in range(2, 11):
        ps = [p for p in lam if len(p) == k]
        top = max(lam[p] for p in ps)
        best = sorted(p for p in ps if lam[p] > top - 1e-12)
        best_by_k[k] = {"best": best, "lambda": round(top, 9), "lambda_1^k": round(lam["1" * k], 9)}
        if set(best) != {"0" * k, "1" * k}:
            h1_viol.append((k, best))
    # unbordered patterns: lambda equals the (k-1)-bonacci constant
    h3_viol = []
    for p, l in lam.items():
        if sum(autocorrelation(p)) == 1 and abs(l - bonacci(len(p) - 1)) > 1e-9:
            h3_viol.append(p)
    # envelope over patterns of length <= 8 for n <= 2^64
    NMAX = 2 ** 64
    pats = sorted({p for p in lam if len(p) <= 8 and p[0] == "1"})   # complement symmetry: p and its complement are equivalent
    codes = {p: PatternCode(p, max_len=400) for p in pats if lam[p] > 1.2}
    import bisect
    # sample n at all powers and half-powers of two plus all small n
    samples = sorted(set(list(range(1, 2049)) + [int(2 ** (e / 4)) for e in range(4, 257)]))
    env = []
    for n in samples:
        lens = {p: c.length(n) for p, c in codes.items()}
        m = min(lens.values())
        env.append((n, m, sorted(p for p, L in lens.items() if L == m)[:4]))
    # H-C11-2: for large n, is 1^k optimal among length-k patterns?
    h2_counter = {}
    for k in (3, 4, 5, 6):
        ones = codes.get("1" * k)
        rivals = [p for p in codes if len(p) == k and p != "1" * k]
        wins = []
        for n in samples:
            if n < 10 ** 3:
                continue
            Lo = ones.length(n)
            better = [p for p in rivals if codes[p].length(n) < Lo]
            if better:
                wins.append((n, better[:3], Lo - min(codes[p].length(n) for p in better)))
        h2_counter[k] = {"n_samples_where_some_rival_beats_1^k": len(wins), "examples": wins[:3],
                         "largest_n_with_rival_win": wins[-1][0] if wins else None}
    # crossover against Elias codes for fixed patterns
    fixed = ["11", "111", "1111", "11111", "011", "0111", "00111", "101", "1011"]
    base = {"gamma": EliasGamma(), "delta": EliasDelta(), "omega": EliasOmega(), "Levenshtein": Levenshtein()}
    cross = {}
    for p in fixed:
        c = codes[p] if p in codes else PatternCode(p, max_len=400)
        row = {}
        for bname, b in base.items():
            shorter = [n for n in samples if c.length(n) < b.length(n)]
            longer = [n for n in samples if c.length(n) > b.length(n)]
            row[bname] = {"pattern_shorter_on_fraction_of_samples": round(len(shorter) / len(samples), 3),
                          "max_sample_where_pattern_shorter": shorter[-1] if shorter else None,
                          "min_sample_where_pattern_longer": longer[0] if longer else None}
        cross[p] = row
    # cumulative counts: unbordered length k vs 1^(k-1) (same lambda)
    ratio_unb = {}
    for k, u in ((3, "011"), (4, "0111"), (5, "01111")):
        a = PatternCode(u, max_len=300).cum[300]
        b = PatternCode("1" * (k - 1), max_len=300).cum[300]
        ratio_unb[f"cum_{u}/cum_{'1' * (k - 1)} at L=300"] = round(a / b, 9)
    # OEIS checks of codeword counts
    oe = {}
    for p in ("011", "101", "0101", "0111", "1011", "0110"):
        seq = [x for x in PatternCode(p).count if x][:30]
        r = oeis.novelty_check(seq)
        oe[p] = {"counts": seq[:16], "status": r["status"], "hits": [h["anumber"] + " " + h["name"][:60] for h in r.get("hits", [])[:2]]}
    ranking = {k: sorted({(round(lam[p], 6)) for p in lam if len(p) == k}, reverse=True)[:6] for k in range(2, 8)}
    return {
        "lambda_examples": {p: round(lam[p], 9) for p in ("11", "111", "011", "101", "1111", "0111", "0101", "1011", "0110", "11111")},
        "max_ratio_check_error": max(check_ratio.values()),
        "best_by_k": best_by_k,
        "h1_violations": h1_viol,
        "h3_violations": h3_viol,
        "distinct_lambda_values_by_k": ranking,
        "envelope_samples": [e for e in env if e[0] in (1, 2, 3, 5, 10, 30, 100, 1000, 2048) or e[0] in [int(2 ** (e2 / 4)) for e2 in (40, 80, 120, 160, 200, 256)]],
        "h2_rival_wins": h2_counter,
        "crossovers_vs_elias": cross,
        "unbordered_vs_ones_cum_ratio": ratio_unb,
        "oeis": oe,
        "summary": [
            f"H-C11-1 (1^k, 0^k uniquely maximise lambda, k=2..10): violations {h1_viol}",
            f"H-C11-3 (unbordered => (k-1)-bonacci lambda): violations {len(h3_viol)}",
            f"root-vs-count-ratio max error {max(check_ratio.values()):.2e}",
            f"H-C11-2 rival wins over 1^k for n >= 1000: " + str({k: v['n_samples_where_some_rival_beats_1^k'] for k, v in h2_counter.items()}),
            f"cumulative-count ratios unbordered/1^(k-1): {ratio_unb}",
            "OEIS: " + str({p: v['status'] for p, v in oe.items()}),
        ],
    }
