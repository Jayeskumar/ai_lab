"""EXP-C11-09: the Fraenkel-Klein code C3 (1996) as a baseline for T_011 and the Fibonacci code C1."""

import random

import numpy as np

from systems.code_bench import expected_length
from systems.codes import FibonacciC1, FraenkelKleinC3, PatternCode

from experiments.C11.E03_synthetic_benchmarks import sources
from experiments.C11.E04_data_benchmarks import datasets

META = {
    "id": "EXP-C11-09",
    "cycle": "C11",
    "title": "Fraenkel-Klein C3 as a baseline: counts, exact length comparison with T_011 and C1, benchmarks",
    "agent": "Mathematical Skeptic",
    "question": "Fraenkel and Klein (1996) already improved the Fibonacci code C1 with C3, a uniquely decipherable "
                "but non-prefix code that is also decoded by searching for the pattern 011. Does T_011 still improve "
                "on the strongest code of that family?",
    "hypothesis": "H-C11-5: C3 has 2F_L - 2 codewords of length <= L (Fraenkel-Klein Prop. 5), so T_011 "
                  "(F_(L+2) - L - 1) is never longer than C3 except for a few small n, cum_011/cum_C3 -> phi^2/2, "
                  "and T_011 has the smaller expected length on the heavy-tailed sources.",
    "assumptions": ["C3 implemented from the paper's construction; its decoder reads one bit past each codeword "
                    "(input virtually followed by '1'), so C3 is compared as a uniquely decipherable code",
                    "exact length comparison for n <= 2e6 and count inequalities for L <= 300 (big integers)",
                    "sources and data sets exactly as in EXP-C11-03 and EXP-C11-04"],
    "methodology": "Check the first 12 codewords against the list printed in the paper, the length counts against "
                   "2F_(r-2) and the construction, round trips of concatenated streams, length(n) == len(encode(n)); "
                   "compare length functions exactly; expected lengths on 12 sources and 4 data sets.",
    "falsification": "C3 shorter than T_011 for some n > 8; a round-trip failure; C3 better than T_011 on Zipf 1.1, "
                     "log-uniform or the bursty posting list.",
    "seed": 9,
}

PAPER_LIST = ["101", "111", "1001", "1101", "10001", "10101", "11001", "11101", "100001", "101001", "100101",
              "110001"]


def _lengths(cum, ns):
    return np.searchsorted(np.asarray(cum, dtype=np.float64), ns, side="left")


def _avg_length(cum, N):
    """Exact average codeword length over n = 1..N from cumulative counts (big integers)."""
    total, prev = 0, 0
    for L, c in enumerate(cum):
        c = min(c, N)
        total += L * (c - prev)
        prev = c
        if c == N:
            return total / N
    raise ValueError("cumulative table too short")


def run():
    rng = random.Random(META["seed"])
    c1, c3, t011 = FibonacciC1(), FraenkelKleinC3(), PatternCode("011", max_len=400)
    problems = []
    # 1. the construction
    first = [c3.encode(n) for n in range(1, 13)]
    if first != PAPER_LIST:
        problems.append(("paper list", first))
    F = c3.Fs
    by_len = {}
    for n in range(1, c3.cum[20] + 1):
        w = c3.encode(n)
        if len(w) != c3.length(n):
            problems.append(("length", n))
        by_len.setdefault(len(w), []).append(w)
    for r in range(3, 21):
        block = [c1.encode(j)[:-1] for j in range(F[r - 1], F[r])]
        if by_len[r] != ["10" + z for z in block] + ["11" + z for z in block] or len(by_len[r]) != 2 * F[r - 2]:
            problems.append(("block", r))
    words = [w for r in sorted(by_len) for w in by_len[r]]
    prefix_pairs = sum(1 for a in words[:200] for b in words[:2000] if a != b and b.startswith(a))
    Fk = [0, 1]
    while len(Fk) < 1500:
        Fk.append(Fk[-1] + Fk[-2])
    kraft = sum(2 * Fk[r - 2] / 2 ** r for r in range(3, 1501))
    # 2. round trips (dense small values exercise the special codeword 111)
    vals = list(range(1, 3001)) + [rng.randrange(1, 2 ** 60) for _ in range(2000)] + \
        [rng.choice((1, 2, 3, 4)) for _ in range(5000)]
    rng.shuffle(vals)
    if c3.decode_seq(c3.encode_seq(vals), len(vals)) != vals:
        problems.append(("roundtrip", None))
    for n in [rng.randrange(1, 2 ** 60) for _ in range(2000)]:
        if c3.decode(c3.encode(n))[0] != n:
            problems.append(("single", n))
    # 3. exact length comparison
    ns = np.arange(1, 2_000_001, dtype=np.float64)
    cum1 = [0] + [F[L + 1] - 1 for L in range(1, 300)]             # C1: F_(L+1) - 1 codewords of length <= L
    l1, l3, lt = _lengths(cum1, ns), _lengths(c3.cum[:300], ns), _lengths(t011.cum[:300], ns)
    for name, cum in (("C1", cum1), ("C3", c3.cum), ("T_011", t011.cum)):
        ref = {"C1": c1, "C3": c3, "T_011": t011}[name]
        bad = [n for n in (1, 2, 3, 4, 5, 8, 100, 10 ** 5, 1999999) if ref.length(n) != int(_lengths(cum, [n])[0])]
        if bad:
            problems.append(("length table", name, bad))
    d13, d3t = l1 - l3, l3 - lt
    hist13 = {int(k): int(v) for k, v in zip(*np.unique(d13, return_counts=True))}
    hist3t = {int(k): int(v) for k, v in zip(*np.unique(d3t, return_counts=True))}
    c3_longer_than_c1 = [int(n) for n in ns[d13 < 0][:20]]
    t011_longer_than_c3 = [int(n) for n in ns[d3t < 0][:20]]
    cum_ineq_t_vs_c3 = [L for L in range(1, 300) if t011.cum[L] < c3.cum[L]]
    cum_ineq_c3_vs_c1 = [L for L in range(1, 300) if c3.cum[L] < cum1[L]]
    ratios = {"cum_011/cum_C3 at L=300": round(t011.cum[300] / c3.cum[300], 9),
              "phi^2/2": round((1 + 5 ** 0.5) ** 2 / 8, 9),
              "cum_C3/cum_C1 at L=299": round(c3.cum[299] / cum1[299], 9),
              "2/phi": round(4 / (1 + 5 ** 0.5), 9)}
    avg_gain = {}
    for e in (40, 80, 120):
        N = 2 ** e
        avg_gain[f"2^{e}"] = {"C1 - C3": round(_avg_length(cum1, N) - _avg_length(c3.cum, N), 6),
                              "C3 - T_011": round(_avg_length(c3.cum, N) - _avg_length(t011.cum, N), 6)}
    # 4. benchmarks
    codes = [c1, c3, t011, PatternCode("0111"), PatternCode("101")]
    synth = {}
    for d in sources():
        row = {c.name: round(expected_length(c, d) - d.entropy, 4) for c in codes}
        synth[d.name] = row
    data = {}
    for d in datasets():
        data[d.name] = {c.name: round(expected_length(c, d), 4) for c in codes}

    def c3_rank(row):
        order = sorted(row, key=row.get)
        return order.index("Fraenkel-Klein C3") + 1

    c3_beats_t011 = [s for s, r in {**synth, **data}.items() if r["Fraenkel-Klein C3"] < r["T_011"]]
    c3_best_of_five = [s for s, r in {**synth, **data}.items() if c3_rank(r) == 1]
    return {
        "problems": problems,
        "first_codewords": first,
        "counts_2F_r_minus_2_checked_up_to_length": 20,
        "prefix_pairs_among_first_codewords": prefix_pairs,
        "kraft_partial_sum_L_le_1500": round(kraft, 12),
        "length_diff_C1_minus_C3_n_le_2e6": hist13,
        "length_diff_C3_minus_T011_n_le_2e6": hist3t,
        "n_where_C3_longer_than_C1": c3_longer_than_c1,
        "n_where_T011_longer_than_C3": t011_longer_than_c3,
        "L_with_cum_T011_below_cum_C3": cum_ineq_t_vs_c3,
        "L_with_cum_C3_below_cum_C1": cum_ineq_c3_vs_c1,
        "ratios": ratios,
        "average_length_difference": avg_gain,
        "synthetic_redundancy": synth,
        "data_bits_per_value": data,
        "sources_where_C3_beats_T011": c3_beats_t011,
        "sources_where_C3_best_of_C1_C3_T011_T0111_T101": c3_best_of_five,
        "summary": [
            f"C3 implementation: problems = {len(problems)}; first 12 codewords match the paper: {first == PAPER_LIST}; "
            f"not prefix-free ({prefix_pairs} prefix pairs among the first codewords); Kraft partial sum "
            f"{round(kraft, 12)}",
            f"n <= 2e6: C3 longer than C1 only for n in {c3_longer_than_c1}; T_011 longer than C3 only for n in "
            f"{t011_longer_than_c3}; (C3 - T_011) histogram {hist3t}",
            f"cum inequalities fail only at L = {cum_ineq_t_vs_c3} (T_011 vs C3) and L = {cum_ineq_c3_vs_c1} (C3 vs C1)",
            f"ratios {ratios}",
            f"average length difference (bits) {avg_gain}",
            f"C3 beats T_011 on: {c3_beats_t011}",
        ],
    }
