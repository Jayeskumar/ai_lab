"""EXP-C16-05: how hard is it to find full-period quasigroups? DFS, SAT and sampling compared."""

import time

import numpy as np

from systems.magma_dynamics import (analyze, count_universal_cycles, first_universal_cycle, is_latin_table,
                                    orbit_length_from_origin, pair_next, random_latin, table_from_cycle,
                                    universal_cycle_sat)

META = {
    "id": "EXP-C16-05",
    "cycle": "C16",
    "title": "Search methods for full-period quasigroups: depth-first search, SAT and random sampling",
    "agent": "Mathematical Explorer",
    "question": "Which method finds full-period quasigroups (cycles with all pairs distinct at distances 1 and 2) "
                "for growing n, and what does a partial count for n = 6 show?",
    "hypothesis": "H-C16-11 (Explorer): exact search (lexicographic DFS, SAT) scales worse than random sampling of "
                  "Latin squares, whose success rate is about 1/n^2 per sample.",
    "assumptions": ["deterministic budgets - DFS: 3,000,000 nodes per n (first solution) and 20,000,000 nodes for "
                    "the partial count at n = 6; SAT (CaDiCaL via pysat): 300,000 conflicts per n; sampling: seeded",
                    "every solution is re-verified by an independent cycle analysis"],
    "methodology": "For n = 5..10 run the lexicographic DFS and the SAT encoding with the budgets above; count the "
                   "solutions the DFS enumerates for n = 6 within its budget (a lower bound, normalised cycles); "
                   "sample 1500 random Latin squares per n and record the success rate.",
    "falsification": "Exact search succeeding for every n where sampling succeeds, within the same budget.",
    "seed": 160505,
}


def verified(seq, n):
    if seq is None:
        return None
    T = table_from_cycle(seq)
    return bool(is_latin_table(T) and analyze(pair_next(T))["max_period"] == n * n)


def run():
    rng = np.random.default_rng(META["seed"])
    timings, rows = {}, {}
    for n in range(5, 11):
        t0 = time.perf_counter()
        seq, nodes, complete = first_universal_cycle(n, node_budget=3_000_000)
        t_dfs = time.perf_counter() - t0
        t0 = time.perf_counter()
        status, sseq = universal_cycle_sat(n, conf_budget=300_000)
        t_sat = time.perf_counter() - t0
        t0 = time.perf_counter()
        hits = sum(1 for _ in range(1500) if orbit_length_from_origin(random_latin(n, rng)) == n * n)
        t_smp = time.perf_counter() - t0
        rows[str(n)] = {"dfs": {"found": seq is not None, "nodes": int(nodes), "verified": verified(seq, n)},
                        "sat": {"status": status, "verified": verified(sseq, n)},
                        "sampling": {"samples": 1500, "hits": int(hits), "rate": round(hits / 1500, 4),
                                     "one_over_n_squared": round(1 / n ** 2, 4)}}
        timings[str(n)] = {"dfs": round(t_dfs, 2), "sat": round(t_sat, 2), "sampling": round(t_smp, 2)}
    t0 = time.perf_counter()
    cnt, nodes, complete = count_universal_cycles(6, node_budget=20_000_000)
    timings["count6"] = round(time.perf_counter() - t0, 2)
    return {
        "rows": rows,
        "partial_count_n6": {"solutions_found": int(cnt), "nodes": int(nodes), "complete": bool(complete)},
        "timings": timings,
        "summary": [f"n={n}: DFS {'found' if r['dfs']['found'] else 'none'} ({r['dfs']['nodes']} nodes), SAT "
                    f"{r['sat']['status']}, sampling {r['sampling']['hits']}/1500" for n, r in rows.items()] +
                   [f"n=6 partial DFS count: {cnt} solutions in {nodes} nodes (complete: {complete})"],
    }
