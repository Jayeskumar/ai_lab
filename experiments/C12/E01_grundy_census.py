"""EXP-C12-01: Grundy sequences of 19 relational one-heap games and their structure."""

import numpy as np

from systems.relational_games import arithmetic_period, eventual_period

from experiments.C12.games_catalog import catalogue

META = {
    "id": "EXP-C12-01",
    "cycle": "C12",
    "title": "Grundy census of 19 relational one-heap games",
    "agent": "Mathematical Explorer",
    "question": "What structure do Sprague-Grundy values have when the moves of a one-heap game are defined by "
                "relations (divisibility, coprimality, membership in a sparse set, bitwise inclusion, splitting) "
                "instead of fixed magnitudes?",
    "hypothesis": "H-C12-0 (exploratory): every game shows one of three behaviours within the computed range - "
                  "eventually periodic, arithmetic-periodic, or a closed form in a number-theoretic function.",
    "assumptions": ["heaps n <= 1e5 (cheap option sets), 2e4 (floor division), 5e3 (option sets of size ~n)",
                    "period search p <= 2000 with at least 3 repetitions of the periodic tail"],
    "methodology": "Exact Grundy computation (bitset method for sparse subtraction sets); record max value, "
                   "growth, P-position density, eventual (arithmetic) periodicity.",
    "falsification": "A game with none of the three behaviours refutes H-C12-0 within the range.",
}


def run():
    rows = {}
    seqs = {}
    for name, (desc, kind, solve) in catalogue().items():
        g = solve()
        seqs[name] = g
        a = np.asarray(g)
        N = len(g) - 1
        per = eventual_period(g)
        ari = None if per else arithmetic_period(g)
        P = [n for n in range(len(g)) if g[n] == 0]
        rows[name] = {
            "description": desc, "relation": kind, "N": N,
            "first_values": g[:40], "max_value": int(a.max()),
            "max_value_first_half": int(a[: N // 2 + 1].max()),
            "P_density": round(len(P) / (N + 1), 6), "first_P_positions": P[:30],
            "eventual_period": per, "arithmetic_period": ari,
        }
    from lab.runner import save_artifact
    art = save_artifact("EXP-C12-01", "grundy_sequences", {k: v for k, v in seqs.items()})
    periodic = [k for k, r in rows.items() if r["eventual_period"]]
    arith = [k for k, r in rows.items() if r["arithmetic_period"]]
    neither = [k for k, r in rows.items() if not r["eventual_period"] and not r["arithmetic_period"]]
    return {
        "rows": rows,
        "sequences_artifact": art,
        "periodic": periodic,
        "arithmetic_periodic": arith,
        "no_period_found": neither,
        "summary": [f"{len(rows)} games; eventually periodic: {len(periodic)}; arithmetic-periodic: {len(arith)}; "
                    f"neither (within range): {len(neither)}"] +
                   [f"{k}: max {r['max_value']} (N={r['N']}), period {r['eventual_period']}, arith "
                    f"{r['arithmetic_period']}, P-density {r['P_density']}" for k, r in rows.items()],
    }
