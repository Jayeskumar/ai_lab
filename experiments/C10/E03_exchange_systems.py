"""EXP-C10-03: the cost of counting in the exchange numeration systems of C02."""

import itertools
from fractions import Fraction

from systems.counting_cost import CarryCounter

META = {
    "id": "EXP-C10-03",
    "cycle": "C10",
    "title": "Firings and digit changes per increment for the 31 terminating carry rules",
    "agent": "Mathematical Explorer",
    "question": "How expensive is counting in the bases that emerge from exchange rules?",
    "hypothesis": "H-C10-1: the average number of firings per increment tends to 1/(m - sum b) for every "
                  "terminating carry rule. H-C10-2 (for J = 1 rules m[k] -> q[k+1]): average digit changes = "
                  "1 + 1/(m - q).",
    "assumptions": ["n < 200000 per rule", "incremental counter validated against full stabilisation"],
    "methodology": "Run the incremental counter; record average firings, average and worst digit changes; "
                   "compare with 1/(m - B) and, for J = 1, with 1 + 1/(m - q).",
    "falsification": "Average firings deviating from 1/(m-B) beyond O(log N/N); a J = 1 rule violating H-C10-2.",
}

N = 200_000
RULES = [(m, b) for m in (2, 3, 4) for J in (1, 2, 3) for b in itertools.product(range(4), repeat=J)
         if b[-1] != 0 and sum(b) < m]


def run():
    rows = []
    for m, b in RULES:
        C = CarryCounter(m, b)
        tf = tc = worst = 0
        for _ in range(N):
            c, f = C.increment()
            tc += c
            tf += f
            worst = max(worst, c)
        B = sum(b)
        rows.append({"m": m, "b": list(b), "avg_firings": round(tf / N, 6), "pred_firings": round(1 / (m - B), 6),
                     "avg_changes": round(tc / N, 6), "worst_changes": worst,
                     "J1_prediction": round(1 + 1 / (m - B), 6) if len(b) == 1 else None})
    fir_dev = max(abs(r["avg_firings"] - r["pred_firings"]) for r in rows)
    j1_dev = max(abs(r["avg_changes"] - r["J1_prediction"]) for r in rows if r["J1_prediction"] is not None)
    return {"N": N, "rows": rows, "max_firing_deviation": fir_dev, "max_J1_change_deviation": j1_dev,
            "summary": [f"{len(rows)} rules: max |avg firings - 1/(m-B)| = {fir_dev}",
                        f"J=1 rules: max |avg changes - (1 + 1/(m-q))| = {j1_dev}"] +
                       [f"m={r['m']} b={r['b']}: firings {r['avg_firings']} changes {r['avg_changes']} worst "
                        f"{r['worst_changes']}" for r in rows[:12]]}
