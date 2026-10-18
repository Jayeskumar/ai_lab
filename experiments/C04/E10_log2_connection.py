"""EXP-C04-10: derivational complexity of aab -> ba equals OEIS A247983 (a truncation index for log 2)."""

import mpmath as mp

from experiments.C04.E04_aab_ba_formula import formula_D

META = {
    "id": "EXP-C04-10",
    "cycle": "C04",
    "title": "D(n+2) for aab -> ba equals A247983(n) = least k with log 2 - sum_{h<=k} 1/(h 2^h) < 2^-n",
    "agent": "Historian and Novelty Analyst",
    "question": "Is the OEIS match of EXP-C04-09 an identity or a coincidence of 60 terms?",
    "hypothesis": "H-C04-8: A247983(n) = n - J(n) with J(n) = max{j >= 0 : 2^j + j <= n + 1}, hence "
                  "A247983(n) = D(n + 2) for all n >= 1 (D the derivational complexity of aab -> ba).",
    "assumptions": ["A247983 as defined in the OEIS (name field, cached)", "mpmath with n + 80 bits of precision"],
    "methodology": "For n = 1..1500 compute the least k with log(2) - sum_{h=1..k} 1/(h 2^h) < 2^-n in "
                   "high-precision arithmetic (with a margin check that the decisive comparisons are far from "
                   "the rounding level), and compare with n - J(n) and with D(n + 2).",
    "falsification": "Any n with a mismatch.",
}


def J(n):
    j = 0
    while 2 ** (j + 1) + (j + 1) <= n + 1:
        j += 1
    return j


def run():
    mismatches, min_margin_bits = [], None
    N = 1500
    for n in range(1, N + 1):
        mp.mp.prec = n + 80
        threshold = mp.mpf(2) ** (-n)
        k0 = max(1, n - J(n) - 2)
        tail = mp.log(2) - mp.fsum(mp.mpf(1) / (h * mp.mpf(2) ** h) for h in range(1, k0 + 1))
        k = k0
        # step forward until the tail drops below the threshold
        while not tail < threshold:
            k += 1
            tail -= mp.mpf(1) / (k * mp.mpf(2) ** k)
        # verify that k - 1 fails (k0 was chosen below the expected answer)
        prev_tail = tail + mp.mpf(1) / (k * mp.mpf(2) ** k)
        ok_prev = k == 1 or not prev_tail < threshold
        margin = min(abs(tail / threshold - 1), abs(prev_tail / threshold - 1))
        mb = float(-mp.log(margin, 2)) if margin > 0 else float("inf")
        min_margin_bits = mb if min_margin_bits is None else max(min_margin_bits, mb)
        expected = n - J(n)
        if k != expected or not ok_prev or k != formula_D(n + 2) or k0 > expected:
            mismatches.append({"n": n, "k": k, "expected": expected, "D(n+2)": formula_D(n + 2)})
    return {
        "n_checked": N,
        "mismatches": mismatches[:10],
        "n_mismatches": len(mismatches),
        "worst_relative_margin_bits": round(min_margin_bits, 2),
        "first_terms": [n - J(n) for n in range(1, 41)],
        "summary": [
            f"A247983(n) computed for n = 1..{N} with n+80 bits: mismatches with n - J(n) or D(n+2): {len(mismatches)}",
            f"closest decisive comparison is 2^-{min_margin_bits:.1f} away in relative terms (precision n+80 bits)",
        ],
    }
