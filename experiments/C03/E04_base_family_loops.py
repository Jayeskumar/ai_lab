"""EXP-C03-04: loops of the base family (1, q, r, k) with long-derivation search; loop sizes."""

from systems.srs_termination import check_loop, find_loop_forward_closures, find_loop_strategies, lift_zeros, rule

META = {
    "id": "EXP-C03-04",
    "cycle": "C03",
    "title": "Base-family loops (1, q, r, k), q < r < 2q: closing the gap and measuring loop sizes",
    "agent": "Formal Verifier",
    "question": "Does every base rule 0 1^q -> 1^r 0^k with q < r < 2q, k >= 2 loop (as required by the "
                "non-terminating half of H-C03-4), and how large are the loops?",
    "hypothesis": "All base rules with q <= 6, k <= 6 have loop certificates; loop sizes grow rapidly with q.",
    "assumptions": ["rightmost/leftmost strategies from 0^a 1^b (a <= 3, b <= 40 q), at most 40000 steps and "
                    "words of at most 300000 letters; forward closures first for small cases"],
    "methodology": "For each base rule: forward closures (<= 60 letters), else long strategy runs; verify each "
                   "certificate and its lifts along 0 -> 0^p (p = 2..4).",
    "falsification": "A base rule with no loop although its derivations keep growing would leave the "
                     "non-terminating half of H-C03-4 unsupported for that rule.",
}


def run():
    rows, missing = [], []
    lifts_ok = 0
    for q in range(2, 7):
        for r in range(q + 1, 2 * q):
            for k in range(2, 7):
                l, rr = rule(1, q, r, k)
                c = find_loop_forward_closures(l, rr, max_len=60, max_pairs=30_000)
                how = "forward closures"
                if c is None:
                    c = find_loop_strategies(l, rr, max_steps=40_000, max_len=300_000, max_a=3, max_b=40 * q)
                    how = c["strategy"] if c else None
                if c is None or not check_loop(l, rr, c):
                    missing.append([1, q, r, k])
                    continue
                for p in (2, 3, 4):
                    if check_loop(*rule(p, q, r, k * p), lift_zeros(c, p, q, r, k)):
                        lifts_ok += 1
                rows.append({"rule": [1, q, r, k], "method": how, "start": c["start"], "steps": len(c["steps"]),
                             "final_length": len(c["end"])})
    biggest = max(rows, key=lambda x: x["steps"]) if rows else None
    return {
        "loops": rows,
        "missing": missing,
        "lifts_verified": lifts_ok,
        "largest_loop": biggest,
        "summary": [
            f"base rules (1,q,r,k), q = 2..6, q < r < 2q, k = 2..6: {len(rows)} loop certificates, missing {missing}",
            f"lifts to (p,q,r,kp), p = 2..4, verified: {lifts_ok}",
            f"largest loop: {biggest['rule']} with {biggest['steps']} steps, final word {biggest['final_length']} letters"
            if biggest else "no loops",
        ],
    }
