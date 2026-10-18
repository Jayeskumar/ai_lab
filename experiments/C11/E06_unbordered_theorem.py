"""EXP-C11-06: unbordered terminators versus all-ones terminators (the x/(1-x) theorem and the one-bit gain)."""

import itertools
import math

from systems.codes import PatternCode, autocorrelation, growth_rate

META = {
    "id": "EXP-C11-06",
    "cycle": "C11",
    "title": "Unbordered terminators: count series x/(1-x) times the all-ones series; T_011 beats Fibonacci by one bit",
    "agent": "Formal Verifier",
    "question": "Why do unbordered terminators beat 1^k at practical sizes although 1^k has the larger growth rate?",
    "hypothesis": "T-C11-A: for every unbordered u of length k+1, the codeword counts satisfy f_u(L) = sum_{l<L} "
                  "f_(1^k)(l) (generating function x/(1-x) times that of T_(1^k)); hence cum_u/cum_(1^k) -> "
                  "1/(lambda_k - 1) and T_u is shorter than T_(1^k) by log_(lambda_k)(1/(lambda_k - 1)) bits on "
                  "average (exactly 1 bit for k = 2). T-C11-B: for n >= 5, T_011 is never longer than the Fibonacci "
                  "code and is exactly one bit shorter except for at most L values of n in each block of F_L "
                  "integers.",
    "assumptions": ["all unbordered patterns of length 3..9, lengths L <= 200 (exact integers)",
                    "exhaustive comparison n <= 2e6 and block-wise comparison up to L = 90"],
    "methodology": "Exact count identities; exact length comparison; average length gap over [1, 2^40] from "
                   "breakpoints compared with the predicted constant.",
    "falsification": "Any count mismatch, any n >= 5 where T_011 is longer than Fibonacci, or more than L "
                     "equal-length n in a block.",
}


def run():
    mism = []
    for k in range(2, 9):
        ones = PatternCode("1" * k, max_len=200).count
        for bits in itertools.product("01", repeat=k + 1):
            u = "".join(bits)
            if sum(autocorrelation(u)) != 1:
                continue
            fu = PatternCode(u, max_len=200).count
            pred = [sum(ones[:L]) for L in range(201)]
            if fu != pred:
                mism.append(u)
    # T_011 versus Fibonacci (T_11), exhaustive
    A, B = PatternCode("011", max_len=200), PatternCode("11", max_len=200)
    longer, equal, shorter_by = [], 0, {}
    for n in range(1, 2_000_001):
        d = B.length(n) - A.length(n)
        if d < 0:
            longer.append(n)
        elif d == 0:
            equal += 1
        shorter_by[d] = shorter_by.get(d, 0) + 1
    # block-wise: n in [cum_11(L-1)+1, cum_11(L)] has Fibonacci length L; count equal-length n per block
    block_violations = []
    for L in range(5, 91):
        lo, hi = B.cum[L - 1] + 1, B.cum[L]
        # T_011 lengths are nondecreasing: equal-length n form a suffix of the block
        eq = sum(1 for n in (hi - j for j in range(0, 200)) if lo <= n and A.length(n) == L)
        if eq > L or A.length(lo) > L:
            block_violations.append(L)
    # average length gap over [1, 2^40] (exact via breakpoints of both codes) vs predicted constants
    def avg_len(code, N):
        tot, prev = 0, 0
        for L, c in enumerate(code.cum):
            if c > prev:
                hi = min(c, N)
                tot += (hi - prev) * L
                if c >= N:
                    return tot / N
                prev = c
        raise ValueError
    gaps = {}
    for k, u in ((2, "011"), (3, "0111"), (4, "01111"), (5, "011111")):
        lam = growth_rate("1" * k)
        pred = math.log(1 / (lam - 1)) / math.log(lam)
        N = 2 ** 40
        gaps[u] = {"avg_gap_bits_[1,2^40]": round(avg_len(PatternCode("1" * k), N) - avg_len(PatternCode(u), N), 4),
                   "predicted_log_lambda(1/(lambda-1))": round(pred, 4)}
    return {
        "count_identity_mismatches": mism,
        "T011_longer_than_fibonacci_for_n": longer,
        "length_difference_histogram_n_le_2e6": shorter_by,
        "equal_length_count_n_le_2e6": equal,
        "block_violations": block_violations,
        "average_gaps": gaps,
        "summary": [
            f"x/(1-x) identity: mismatches {len(mism)} over all unbordered patterns of length 3..9",
            f"T_011 longer than Fibonacci only for n in {longer}; length differences (Fib - T011) for n <= 2e6: {shorter_by}",
            f"block-wise check L = 5..90: violations {block_violations}",
            f"average gaps vs prediction: {gaps}",
        ],
    }
