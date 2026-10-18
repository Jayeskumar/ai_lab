"""EXP-C19-02: anatomy of the longest game - an exact identity, the lazy split phase, a refuted decomposition."""

import random

from systems.zeckendorf_game import (FIB, combine_weight, cusenza_bound, greedy_game, lazy_digits, moves,
                                     random_game, split_phase, split_phase_fast, zeckendorf_digits)

META = {
    "id": "EXP-C19-02",
    "cycle": "C19",
    "title": "Anatomy of the longest Zeckendorf game: the identity L = B - W, the lazy split phase, insertion",
    "agent": "Formal Verifier",
    "question": "Is the length of EVERY game equal to B(n) - sum_{i>=2} (i-1) MC_i (B = Cusenza's bound)? Where "
                "does the split phase of the greedy game end? Is L(n+1) = L(n) + (longest game from Zeck(n) + 1)?",
    "hypothesis": "H-C19-A (derived from a potential): length = B(n) - W for every game. H-C19-B: splits and "
                  "combine-1s, applied in any order, end at the lazy Fibonacci representation of n after the same "
                  "number of moves. H-C19-4 (bold): L(n+1) = L(n) + lambda(n), lambda(n) the longest game from the "
                  "Zeckendorf representation of n plus one extra 1.",
    "assumptions": ["random games choose uniformly among legal moves (seeded)", "lazy representation computed by "
                    "the top-down algorithm and checked to have no two consecutive zeros"],
    "methodology": "Greedy games for n < 1500 and 1500 random games (n <= 200): compare length with B(n) - W. "
                   "Split phase (lowest-first) for n < 5000 against the lazy digits; 300 random firing orders "
                   "(n <= 600). Exact longest games from Zeck(m) + [1] for m < 300.",
    "falsification": "A game violating the identity; a split phase ending elsewhere or with a different length; "
                     "H-C19-4: any m with L(m+1) != L(m) + lambda(m).",
    "seed": 19,
}


def longest_from(c):
    memo, stack = {}, [tuple(c)]
    while stack:
        x = stack[-1]
        if x in memo:
            stack.pop()
            continue
        succ = [d for _, d in moves(x)]
        pend = [d for d in succ if d not in memo]
        if pend:
            stack.extend(pend)
            continue
        memo[x] = 1 + max(memo[d] for d in succ) if succ else 0
        stack.pop()
    return memo[tuple(c)]


def run():
    rng = random.Random(META["seed"])
    # (A) identity on greedy and random games
    bad_greedy = []
    for n in range(1500):
        g = greedy_game(n)
        if g["length"] != cusenza_bound(n) - combine_weight(g["counts"]):
            bad_greedy.append(n)
    bad_random, rand_lengths = [], []
    for _ in range(1500):
        n = rng.randint(0, 200)
        g = random_game(n, rng)
        rand_lengths.append(g["length"])
        if g["length"] != cusenza_bound(n) - combine_weight(g["counts"]) or list(g["final"]) != zeckendorf_digits(n):
            bad_random.append(n)
    # (B) split phase ends at the lazy representation
    lazy_ok, lazy_bad = 0, []
    for n in range(1, 5000):
        d = lazy_digits(n)
        assert sum(FIB[k] for k, x in enumerate(d) if x) == n
        assert not any(d[k] == 0 and d[k + 1] == 0 for k in range(len(d) - 1))
        s, _ = split_phase_fast(n)
        if list(s) == d:
            lazy_ok += 1
        else:
            lazy_bad.append(n)
    order_bad = []
    for _ in range(300):
        n = rng.randint(1, 600)
        s0, k0 = split_phase(n)
        s1, k1 = split_phase(n, order="random", rng=rng)
        if s0 != s1 or k0 != k1:
            order_bad.append(n)
    # (C) insertion decomposition
    lengths = [greedy_game(m)["length"] for m in range(301)]
    fails, first = 0, []
    for m in range(300):
        z = zeckendorf_digits(m) or [0]
        z[0] += 1
        lam = longest_from(tuple(z))
        if lengths[m + 1] != lengths[m] + lam:
            fails += 1
            if len(first) < 5:
                first.append({"m": m, "L(m+1)": lengths[m + 1], "L(m)": lengths[m], "lambda": lam})
    return {
        "identity_greedy_violations_n_lt_5000": bad_greedy,
        "identity_random_game_violations": bad_random,
        "random_games": 1500,
        "random_length_range": [min(rand_lengths), max(rand_lengths)],
        "split_phase_equals_lazy": lazy_ok,
        "split_phase_not_lazy": lazy_bad[:20],
        "random_order_mismatches": order_bad,
        "insertion_failures_m_lt_300": fails,
        "insertion_counterexamples": first,
        "summary": [
            f"identity length = B(n) - sum (i-1) MC_i: violations on greedy games n < 1500: {len(bad_greedy)}; "
            f"on 1500 random games: {len(bad_random)}",
            f"split phase (splits + combine-1s) ends at the lazy representation for {lazy_ok} of 4999 n; "
            f"random firing orders change the end point or the length in {len(order_bad)} of 300 cases",
            f"H-C19-4 (L(m+1) = L(m) + lambda(m)) fails for {fails} of 300 m, first: {first[:2]}",
        ],
    }
