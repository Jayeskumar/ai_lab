"""EXP-C19-01: exact longest Zeckendorf games for n <= 150 by dynamic programming (no strategy assumed)."""

import json
import time

from lab.paths import RESULTS
from systems.zeckendorf_game import (FIB, cusenza_bound, fib_partitions, greedy_game, greedy_length_fast,
                                     longest_exact)

META = {
    "id": "EXP-C19-01",
    "cycle": "C19",
    "title": "Exact longest Zeckendorf games for n <= 150 and independent check of the published strategy",
    "agent": "Mathematical Explorer",
    "question": "What is the longest game L(n) for n <= 150, computed without assuming any strategy, and does "
                "the split-first greedy strategy of Cusenza et al. (2022, Thm 1.2) attain it?",
    "hypothesis": "H-C19-0: the greedy strategy attains L(n) for every n <= 150; the published values (n <= 49) "
                  "and the lab's earlier values (n <= 60) are reproduced; Cusenza's bound sum a_i delta_i is "
                  "attained exactly for n = F_k - 1 (their Thm 1.4).",
    "assumptions": ["levels 0, 1, 2, ... carry F_1 = 1, F_2 = 2, F_3 = 3, ...",
                    "exact DP over all configurations reachable from n ones (memoised longest path; the move "
                    "graph is acyclic because the game terminates)"],
    "methodology": "For each n <= 150: memoised longest path over all reachable configurations; compare with "
                   "C02 values (results/EXP-C02-02.json, n <= 40), the Skeptic's values (n = 41..60), the simple "
                   "and the fast greedy implementations, and Cusenza's bound; record the state counts and compare "
                   "them with the number of partitions of n into Fibonacci parts.",
    "falsification": "Any n where the greedy is shorter than the exact optimum, a mismatch with earlier values, "
                     "or bound equality at some n != F_k - 1.",
}

SKEPTIC_41_60 = [81, 84, 85, 87, 89, 91, 95, 96, 98, 101, 102, 106, 109, 113, 117, 118, 120, 122, 124, 127]
NMAX = 150


def run():
    t0 = time.perf_counter()
    exact, states = [], []
    for n in range(NMAX + 1):
        L, s = longest_exact(n, return_states=True)
        exact.append(L)
        states.append(s)
    t_exact = time.perf_counter() - t0
    c02 = json.loads((RESULTS / "EXP-C02-02.json").read_text())["results"]["max_len_seq"]
    known = c02 + SKEPTIC_41_60
    greedy = [greedy_game(n)["length"] for n in range(NMAX + 1)]
    fast = [greedy_length_fast(n) for n in range(NMAX + 1)]
    bound = [cusenza_bound(n) for n in range(NMAX + 1)]
    fk1 = {FIB[k] - 1 for k in range(len(FIB)) if FIB[k] - 1 <= NMAX}
    eq = [n for n in range(1, NMAX + 1) if bound[n] == exact[n]]
    parts = fib_partitions(NMAX + 1)
    return {
        "L_exact": exact,
        "states": states,
        "known_values_match_n_le_60": exact[:61] == known,
        "greedy_equals_exact": greedy == exact,
        "fast_greedy_equals_exact": fast == exact,
        "greedy_mismatches": [n for n in range(NMAX + 1) if greedy[n] != exact[n]],
        "bound_equality_set": eq,
        "bound_equality_iff_Fk_minus_1": set(eq) == {m for m in fk1 if m >= 1},
        "states_equal_fib_partitions": states == parts[:NMAX + 1],
        "max_states": max(states),
        "timings": {"exact_dp_s": round(t_exact, 1), "total_s": round(time.perf_counter() - t0, 1)},
        "summary": [
            f"exact longest games for n <= {NMAX} (max {max(states)} states at n = {NMAX}); known values n <= 60 "
            f"reproduced: {exact[:61] == known}",
            f"split-first greedy = exact optimum for all n <= {NMAX}: {greedy == exact} (fast implementation: "
            f"{fast == exact})",
            f"Cusenza bound attained exactly at n in {eq} - i.e. iff n = F_k - 1: "
            f"{set(eq) == {m for m in fk1 if m >= 1}}",
            f"reachable configurations = partitions of n into Fibonacci parts for every n <= {NMAX}: "
            f"{states == parts[:NMAX + 1]}",
        ],
    }
