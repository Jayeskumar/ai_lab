"""EXP-C10-01: the cost of counting in classical representations."""

import math

from systems.counting_cost import SYSTEMS, changes

META = {
    "id": "EXP-C10-01",
    "cycle": "C10",
    "title": "Average and worst-case digit changes per increment in classical representations",
    "agent": "Mathematical Explorer",
    "question": "How many digits change, on average and at worst, when counting n -> n+1 in different "
                "representations?",
    "hypothesis": "Base b: b/(b-1); Gray code: 1; factorial base: e - 1; negabinary and balanced ternary match "
                  "their unsigned counterparts; skew binary has bounded worst case. (Inventor's bold guess H-C10-0: "
                  "Zeckendorf, being 'sparser', costs less than binary.)",
    "assumptions": ["n < 10^6 (exchange-based systems excluded here, see EXP-C10-03)"],
    "methodology": "Count positions whose digit differs between n and n+1 for all n < N.",
    "falsification": "Averages differing from the predicted constants by more than O(log N / N).",
}

N = 10**6
PRED = {"binary": 2, "ternary": 1.5, "decimal": 10 / 9, "gray": 1, "factorial": math.e - 1,
        "negabinary": 2, "balanced_ternary": 1.5}


def run():
    rows = {}
    for name, f in SYSTEMS.items():
        if name.startswith("base_"):
            continue
        prev, tot, worst = f(0), 0, 0
        for n in range(1, N):
            cur = f(n)
            c = changes(prev, cur)
            tot += c
            worst = max(worst, c)
            prev = cur
        rows[name] = {"average": round(tot / (N - 1), 7), "worst": worst, "predicted": PRED.get(name)}
    return {"N": N, "rows": rows,
            "summary": [f"{k}: avg {v['average']} (pred {v['predicted']}), worst {v['worst']}" for k, v in rows.items()]}
