"""EXP-C11-07: corrected average-gain formula for unbordered terminators (after EXP-C11-06)."""

from systems.codes import PatternCode, growth_rate

META = {
    "id": "EXP-C11-07",
    "cycle": "C11",
    "title": "Average one-bit gain of unbordered terminators: corrected constant (2 - lambda)/(lambda - 1)^2",
    "agent": "Mathematical Skeptic",
    "question": "EXP-C11-06 refuted the predicted average gain log_lambda(1/(lambda-1)) for k >= 3. Does the "
                "level-fraction argument give the right constant?",
    "hypothesis": "H-C11-5: the average length gain of T_u (u unbordered, |u| = k+1) over T_(1^k) on [1, N] tends to "
                  "(r - 1)/(lambda - 1) = (2 - lambda)/(lambda - 1)^2 with r = 1/(lambda - 1), lambda the k-bonacci "
                  "constant (each saved codeword saves exactly one bit).",
    "assumptions": ["N = 2^40, 2^80, 2^120 (exact, from cumulative counts)"],
    "methodology": "Exact average codeword lengths from cumulative counts; compare with both formulas.",
    "falsification": "Disagreement with (2 - lambda)/(lambda - 1)^2 that does not shrink as N grows.",
}


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


def run():
    import math
    rows = {}
    for k, u in ((2, "011"), (3, "0111"), (4, "01111"), (5, "011111"), (6, "0111111")):
        lam = growth_rate("1" * k)
        A, B = PatternCode("1" * k, max_len=600), PatternCode(u, max_len=600)
        rows[u] = {"lambda_k": round(lam, 9),
                   "corrected_prediction": round((2 - lam) / (lam - 1) ** 2, 6),
                   "refuted_prediction_log_form": round(math.log(1 / (lam - 1)) / math.log(lam), 6),
                   "measured": {f"2^{e}": round(avg_len(A, 2 ** e) - avg_len(B, 2 ** e), 6) for e in (40, 80, 120)}}
    return {"rows": rows,
            "summary": [f"{u}: corrected {r['corrected_prediction']}, old {r['refuted_prediction_log_form']}, measured "
                        f"{r['measured']}" for u, r in rows.items()]}
