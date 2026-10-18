"""EXP-C11-08: the running average gain oscillates between two explicit constants (after EXP-C11-07)."""

from systems.codes import PatternCode, growth_rate

META = {
    "id": "EXP-C11-08",
    "cycle": "C11",
    "title": "Running average gain of unbordered terminators: liminf (2-l)/(l-1)^2, limsup l(2-l)/(l-1)",
    "agent": "Mathematical Skeptic",
    "question": "EXP-C11-07 showed the average gain over [1, N] does not converge for k >= 3. Are its extreme values "
                "the ones predicted by the level structure?",
    "hypothesis": "H-C11-6: let lambda = k-bonacci constant, O = T_(1^k), U = T_u (u unbordered, |u| = k+1). At the "
                  "ends of O's length levels, the running average gain tends to (2-lambda)/(lambda-1)^2 (its liminf); "
                  "at the ends of the saved initial segments of the levels it tends to lambda(2-lambda)/(lambda-1) "
                  "(its limsup). For k = 2 both equal 1.",
    "assumptions": ["levels L up to 500 (exact integers)", "k = 2..6"],
    "methodology": "Exact running sums of the length difference evaluated at N = cum_O(L) and at N = cum_U(L-1) "
                   "for large L; compare with both constants.",
    "falsification": "Values at large L not approaching the two constants.",
}


def run():
    rows = {}
    for k, u in ((2, "011"), (3, "0111"), (4, "01111"), (5, "011111"), (6, "0111111")):
        lam = growth_rate("1" * k)
        O, U = PatternCode("1" * k, max_len=700), PatternCode(u, max_len=700)

        def gain_upto(N):
            # exact sum over n <= N of len_O(n) - len_U(n)
            def total(code):
                tot, prev = 0, 0
                for L, c in enumerate(code.cum):
                    if c > prev:
                        hi = min(c, N)
                        tot += (hi - prev) * L
                        if c >= N:
                            return tot
                        prev = c
                raise ValueError
            return (total(O) - total(U)) / N

        lo_vals = [round(gain_upto(O.cum[L]), 6) for L in (100, 200, 400)]
        hi_vals = [round(gain_upto(U.cum[L - 1]), 6) for L in (100, 200, 400)]
        rows[u] = {"pred_liminf": round((2 - lam) / (lam - 1) ** 2, 6), "at_level_ends_L=100,200,400": lo_vals,
                   "pred_limsup": round(lam * (2 - lam) / (lam - 1), 6), "at_saved_segment_ends_L=100,200,400": hi_vals}
    return {"rows": rows,
            "summary": [f"{u}: liminf pred {r['pred_liminf']} vs {r['at_level_ends_L=100,200,400']}; limsup pred "
                        f"{r['pred_limsup']} vs {r['at_saved_segment_ends_L=100,200,400']}" for u, r in rows.items()]}
