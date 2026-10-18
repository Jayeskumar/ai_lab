"""EXP-C08-04: does the sign of the conjugate root explain non-monotone associativity thresholds?"""

import random

import numpy as np

from systems.circle import BaseSequence

META = {
    "id": "EXP-C08-04",
    "cycle": "C08",
    "title": "Sign of the conjugate root versus monotonicity of the associative-shift set",
    "agent": "Mathematical Explorer",
    "question": "Why is the set of associative shifts sometimes not upward-closed (e.g. s = 2 and s >= 4 but not 3)?",
    "hypothesis": "H-C08-4: for quadratic Pisot base sequences, if the conjugate root beta is positive the set of "
                  "associative shifts is upward-closed; non-monotone sets occur only when beta < 0 (the factor "
                  "beta^s flips the sign of the conjugate of the product and the conjugate window is asymmetric).",
    "assumptions": ["quadratic recurrences G_(k+1) = p G_k + q G_(k-1) with p in 1..5, q in -3..3 (q != 0), Pisot "
                    "with real conjugate, several initial values G_1", "shifts 0..10", "tests: exhaustive [1,12]^3 "
                    "plus 800 random triples in [1,1e5]^3"],
    "methodology": "Classify each sequence by the sign of beta; compute the associative-shift set; check "
                   "upward-closure.",
    "falsification": "A positive-beta sequence with a non-upward-closed associative-shift set.",
    "seed": 44,
}


def assoc(G, s, rng):
    for a in range(1, 13):
        for b in range(1, 13):
            ab = G.circle(a, b, s)
            for c in range(1, 13):
                if G.circle(ab, c, s) != G.circle(a, G.circle(b, c, s), s):
                    return False
    for _ in range(800):
        a, b, c = (rng.randint(1, 10**5) for _ in range(3))
        if G.circle(G.circle(a, b, s), c, s) != G.circle(a, G.circle(b, c, s), s):
            return False
    return True


def run():
    rng = random.Random(META["seed"])
    rows, violations = [], []
    for p in range(1, 6):
        for q in (-3, -2, -1, 1, 2, 3):
            r = np.roots([1, -p, -q])
            if np.iscomplexobj(r) and np.max(np.abs(np.imag(r))) > 1e-12:
                continue
            r = sorted(np.real(r), key=abs)
            beta, alpha = r[0], r[1]
            if not (alpha > 1 and abs(beta) < 1 - 1e-9) or abs(beta) < 1e-12:
                continue
            for g1 in range(2, 7):
                try:
                    G = BaseSequence(f"G(k+1)={p}G(k)+({q})G(k-1); 1,{g1}", [1, g1], (p, q))
                    G.extend(60)
                except ValueError:
                    continue
                if any(G.G[i] * G.G[i] == G.G[i - 1] * G.G[i + 1] for i in range(1, 6)):
                    continue  # geometric
                shifts = [s for s in range(0, 11) if assoc(G, s, rng)]
                upward = bool(shifts) and shifts == list(range(shifts[0], 11))
                row = {"G": G.name, "head": G.G[:7], "beta": round(float(beta), 6), "alpha": round(float(alpha), 6),
                       "associative_shifts": shifts, "upward_closed": upward}
                rows.append(row)
                if beta > 0 and shifts and not upward:
                    violations.append(row)
    pos = [r for r in rows if r["beta"] > 0]
    neg = [r for r in rows if r["beta"] < 0]
    return {
        "rows": rows,
        "violations": violations,
        "summary": [
            f"{len(rows)} quadratic Pisot sequences: {len(pos)} with beta > 0, {len(neg)} with beta < 0",
            f"beta > 0: non-upward-closed shift sets = {len(violations)}; with no associative shift <= 10: "
            f"{sum(not r['associative_shifts'] for r in pos)}",
            f"beta < 0: non-upward-closed shift sets = {sum(bool(r['associative_shifts']) and not r['upward_closed'] for r in neg)}"
            f"; with no associative shift <= 10: {sum(not r['associative_shifts'] for r in neg)}",
        ],
    }
