"""EXP-C06-01: Laver tables - the unique left-distributive structures with a successor anchor."""

import random

import numpy as np

from lab import oeis
from systems.laver import is_left_distributive, laver_table, recursion_table, row_period

META = {
    "id": "EXP-C06-01",
    "cycle": "C06",
    "title": "Laver tables: construction, left-distributivity and periods",
    "agent": "Mathematical Explorer",
    "question": "What does a single composition law (left self-distributivity x(yz) = (xy)(xz)) produce when "
                "the operation is anchored to a successor (x * 0 = x + 1 mod N)?",
    "hypothesis": "Laver's recursion yields a left-distributive table exactly when N is a power of 2 (the Laver "
                  "tables A_n); the period of row 0 (Laver's row 1) follows OEIS A098820.",
    "assumptions": ["N <= 4096; exhaustive LD check for N <= 256, 2e5 random triples for N = 512..4096"],
    "methodology": "Run Laver's recursion for every N <= 64 and for N = 2^n up to 4096; test left-distributivity; "
                   "compute periods of row 0 and of all rows; OEIS check of the period sequence.",
    "falsification": "An LD table from the recursion for N not a power of 2, a power of 2 failing LD, or a period "
                     "sequence differing from A098820.",
    "seed": 6,
}


def run():
    rng = random.Random(META["seed"])
    general = {}
    for N in range(1, 65):
        T = recursion_table(N)
        general[N] = "recursion breaks down" if T is None else ("LD" if is_left_distributive(T) else "not LD")
    ld_N = [N for N, s in general.items() if s == "LD"]
    periods, ld_checks = [], {}
    for n in range(0, 13):
        T = laver_table(n)
        N = 2 ** n
        if N <= 256:
            ok = is_left_distributive(T)
            method = "exhaustive"
        else:
            ok = True
            for _ in range(200_000):
                a, b, c = (rng.randrange(N) for _ in range(3))
                if T[a, T[b, c]] != T[T[a, b], T[a, c]]:
                    ok = False
                    break
            method = "random 2e5"
        anchor = all(T[x, 0] == (x + 1) % N for x in range(N))
        ld_checks[n] = {"N": N, "LD": ok, "method": method, "anchor": anchor}
        periods.append(row_period(T, 0))
    row_periods_A4 = [row_period(laver_table(4), a) for a in range(16)]
    o = oeis.novelty_check(periods)
    return {
        "recursion_outcome_N_1_64": general,
        "LD_tables_from_recursion": ld_N,
        "laver_checks": ld_checks,
        "row0_periods_n0_12": periods,
        "row_periods_A4": row_periods_A4,
        "oeis_periods": {"status": o["status"], "hits": o.get("hits", [])[:2]},
        "summary": [
            f"Laver's recursion gives an LD table exactly for N in {ld_N} (N <= 64)",
            f"A_n LD-verified for n <= 12 (exhaustive up to N = 256): {all(v['LD'] for v in ld_checks.values())}",
            f"row-0 periods n = 0..12: {periods}; OEIS {o['status']} {[h['anumber'] for h in o.get('hits', [])[:2]]}",
        ],
    }
