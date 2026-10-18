"""EXP-C15-04: how often does cycle detection fast-forward an order-3 magma automaton?"""

import time

import numpy as np

from systems.magma_ca import cycle_fast_forward

META = {
    "id": "EXP-C15-04",
    "cycle": "C15",
    "title": "Cycle detection as a universal fast-forward: transient plus period of random cyclic rows",
    "agent": "Application Researcher",
    "question": "For each of the 1734 order-3 magma automata, after how many steps (transient mu plus period lambda) "
                "does a random cyclic row of length L = 16, 32, 64 repeat? Cycle detection answers any query t in "
                "mu + lambda simulated steps.",
    "hypothesis": "H-C15-5 (bold): for most classes (at least half), a random cyclic row of length 32 repeats within "
                  "5000 steps, so cycle detection fast-forwards most magma automata; long cycles occur only for "
                  "classes with geometric streaming width.",
    "assumptions": ["one seeded random row per class and length", "cap 5000 simulated steps (rows that do not repeat "
                    "within the cap are reported as 'not found')", "width classes from EXP-C15-02"],
    "methodology": "cycle_fast_forward with a dictionary of visited rows; record mu, lambda or 'not found'; group by "
                   "the width class of EXP-C15-02.",
    "falsification": "Fewer than half of the classes repeat within the cap at L = 32, or a bounded/linear-width class "
                     "that does not repeat within the cap.",
    "seed": 1515,
}

CAP = 5000


def run():
    import json
    from lab.paths import RESULTS
    census = json.loads((RESULTS / "EXP-C15-02.json").read_text())["results"]["rows"]
    rng = np.random.default_rng(META["seed"])
    t0 = time.perf_counter()
    per_L = {}
    for L in (16, 32, 64):
        found, mus, lams, by_class, not_found_tables = 0, [], [], {}, []
        for r in census:
            T = np.array(r["table"], dtype=np.int8)
            row = rng.integers(0, 3, L).astype(np.int8)
            _, steps, mu, lam = cycle_fast_forward(T, row, 10 ** 12, cap=CAP)
            c = r["width_class"]
            bc = by_class.setdefault(c, {"classes": 0, "found": 0, "max_mu_plus_lam": 0})
            bc["classes"] += 1
            if mu is not None:
                found += 1
                mus.append(mu)
                lams.append(lam)
                bc["found"] += 1
                bc["max_mu_plus_lam"] = max(bc["max_mu_plus_lam"], mu + lam)
            elif c in ("bounded", "linear"):
                not_found_tables.append(r["table"])
        per_L[str(L)] = {"found": found, "of": len(census), "median_mu": float(np.median(mus)) if mus else None,
                         "median_lambda": float(np.median(lams)) if lams else None,
                         "max_mu": int(max(mus)) if mus else None, "max_lambda": int(max(lams)) if lams else None,
                         "by_width_class": by_class, "bounded_or_linear_not_found": not_found_tables[:10],
                         "n_bounded_or_linear_not_found": len(not_found_tables)}
    return {
        "per_L": per_L,
        "timings": {"total_s": round(time.perf_counter() - t0, 1)},
        "summary": [f"L={L}: {v['found']}/{v['of']} repeat within {CAP} steps; median mu {v['median_mu']}, median "
                    f"lambda {v['median_lambda']}; bounded/linear-width classes not repeating: "
                    f"{v['n_bounded_or_linear_not_found']}" for L, v in per_L.items()],
    }
