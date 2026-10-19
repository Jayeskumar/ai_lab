"""EXP-C19-05: a provably correct O(log^2 n)-move method for the longest Zeckendorf game, and the recursion tested against it.

After the Skeptic's review (reviews/skeptic_C13_C19.md, C9): by Theorems 1-2 of proofs/paper/C19.md the strategy game
of Cusenza et al. first plays exactly Psi(lazy(n)) moves and reaches the lazy representation; only the second phase
needs to be played, and it has at most B(n) - Psi(lazy(n)) <= 1 + (t + 1)(t + 6)/2 moves (t the top level of
lazy(n)). This experiment checks the method against full simulation, tests the conjectured recursion CLM-C19-05
against it far beyond the old range, checks the move bound, and times both.
"""

import random
import time

from systems.zeckendorf_game import (FIB, cusenza_bound, greedy_length_fast, lazy_digits, longest_rec,
                                     longest_via_lazy, potential)

META = {
    "id": "EXP-C19-05",
    "cycle": "C19",
    "title": "The lazy-representation method for the longest Zeckendorf game: correctness checks, the move bound, "
             "and the recursion CLM-C19-05 tested against it",
    "agent": "Mathematical Explorer",
    "question": "Does L(n) = Psi(lazy(n)) + (second phase from lazy(n)) agree with full simulation, does the move "
                "bound hold, and does the conjectured recursion agree with this provably correct method on far more "
                "n than before?",
    "hypothesis": "Theorem 7 of proofs/paper/C19.md: the method equals the strategy game length for every n, with at "
                  "most 1 + (t + 1)(t + 6)/2 second-phase moves; CLM-C19-05 (conjecture) agrees with it everywhere.",
    "assumptions": ["the strategy game is optimal (Cusenza et al. 2022, Thm 1.2) - needed only to call its length "
                    "L(n); the identity with the simulated strategy game is unconditional",
                    "random samples with a fixed seed"],
    "methodology": "Compare with greedy_length_fast for every n < 20000; compare longest_rec (the recursion) with the "
                   "method for every n < 100000, 3000 random n in [1e6, 1e15) and 800 n = F_j + m (j = 30..69, "
                   "m < F_(j-1)); check second-phase moves <= B(n) - Psi(lazy(n)) <= 1 + (t + 1)(t + 6)/2 on all "
                   "tested n; time the method, the recursion and (n <= 1e7) full simulation.",
    "falsification": "Any mismatch with full simulation (would contradict Theorems 1-2), any violated bound, or any "
                     "n where the recursion and the method disagree (would refute CLM-C19-05).",
    "seed": 1905,
}


def bound(n):
    lz = lazy_digits(n)
    t = len(lz) - 1
    return cusenza_bound(n) - potential(lz), 1 + (t + 1) * (t + 6) // 2


def run():
    rng = random.Random(META["seed"])
    sim_mismatch = [n for n in range(1, 20000) if longest_via_lazy(n)[0] != greedy_length_fast(n)]
    tests = list(range(1, 100000))
    tests += [rng.randrange(10 ** 6, 10 ** 15) for _ in range(3000)]
    for _ in range(800):
        j = rng.randint(30, 69)
        tests.append(FIB[j] + rng.randrange(0, FIB[j - 1]))
    rec_mismatch, bound_viol, worst = [], [], (0, None)
    max_second = 0
    for n in tests:
        L, second = longest_via_lazy(n)
        if L != longest_rec(n):
            rec_mismatch.append(n)
        gap, cap = bound(n)
        if not second <= gap <= cap:
            bound_viol.append(n)
        max_second = max(max_second, second)
        if cap and gap / cap > worst[0]:
            worst = (gap / cap, n)
    timing, moves = {}, {}
    for n in (10 ** 6, 10 ** 7, 10 ** 9, 10 ** 15, 10 ** 18):
        t0 = time.perf_counter()
        L, second = longest_via_lazy(n)
        t1 = time.perf_counter()
        R = longest_rec(n)
        t2 = time.perf_counter()
        moves[str(n)] = {"L": L, "second_phase_moves": second, "recursion_agrees": R == L}
        timing[f"{n}/lazy_method_s"] = round(t1 - t0, 6)
        timing[f"{n}/recursion_s"] = round(t2 - t1, 6)
        if n <= 10 ** 7:
            t3 = time.perf_counter()
            S = greedy_length_fast(n)
            timing[f"{n}/full_simulation_s"] = round(time.perf_counter() - t3, 3)
            moves[str(n)]["full_simulation_agrees"] = S == L
    return {
        "full_simulation_mismatches_n_lt_20000": sim_mismatch,
        "n_tested_against_recursion": len(tests),
        "recursion_mismatches": rec_mismatch[:20],
        "n_recursion_mismatches": len(rec_mismatch),
        "bound_violations": bound_viol[:20],
        "max_second_phase_moves": max_second,
        "largest_gap_over_bound": {"ratio": round(worst[0], 4), "n": worst[1]},
        "large_n": moves,
        "timings": timing,
        "summary": [
            f"method vs full simulation, every n < 20000: {len(sim_mismatch)} mismatches",
            f"recursion CLM-C19-05 vs the method on {len(tests)} n (all n < 1e5, 3000 random n < 1e15, 800 F_j + m): "
            f"{len(rec_mismatch)} mismatches",
            f"second-phase moves <= B(n) - Psi(lazy(n)) <= 1 + (t+1)(t+6)/2 on every tested n: violations "
            f"{len(bound_viol)}; largest B - Psi(lazy) relative to the bound {round(worst[0], 3)} (n = {worst[1]})",
            "second-phase moves at n = 1e6, 1e9, 1e15, 1e18: " +
            ", ".join(f"{moves[str(n)]['second_phase_moves']}" for n in (10 ** 6, 10 ** 9, 10 ** 15, 10 ** 18)),
        ],
    }
