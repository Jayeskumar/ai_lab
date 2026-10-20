"""Skeptic batch 1.1 -- CLM-C19-15 (and the written steps of C19 Theorems 1, 2, 7, 8), from scratch.

Setting (proofs/paper/C19.md): chips on levels k = 0, 1, ...; a chip on level k is worth F_{k+1}
(F_1 = 1, F_2 = 2, F_{i+1} = F_i + F_{i-1}). Moves (paper index i = level + 1):
  C1 : 2 chips on level 0 -> 1 chip on level 1
  C_i: chips on levels i-2 and i-1 -> 1 chip on level i            (i >= 2)
  S2 : 2 chips on level 1 -> chips on levels 0 and 2
  S_i: 2 chips on level i-1 -> chips on levels i-3 and i            (i >= 3)
L(n) = longest game from n chips on level 0 (exhaustive search here), B(n) = sum a_i delta_i over the
Zeckendorf digits, a_i = F_{i+2} - i - 2, D(n) = B(n) - L(n), Psi(c) = sum_k c_k a_{k+1}.

Checked:
 T1  every move changes Psi by +1 (C1, splits) or +i (C_i, i >= 2); |G| = B(n) - sum (i-1) MC_i(G) on random games;
 T2  (exhaustive, small n) every maximal split-only sequence ends at lazy(n) and has Psi(lazy(n)) moves;
     lazy(n) computed by brute force over all sets of levels (and its uniqueness checked);
 T8  L(n) >= Psi(lazy(n)), D(n) <= B(n) - Psi(lazy(n)) <= 1 + (t+1)(t+6)/2 (t = top level of lazy(n));
     for larger n only the arithmetic part B(n) - Psi(lazy(n)) <= 1 + (t+1)(t+6)/2.
usage: python c19_checks.py [NMAX_EXHAUSTIVE] [NMAX_SPLIT] [NMAX_ARITH]
"""
import functools
import itertools
import json
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.setrecursionlimit(100000)

F = [None, 1, 2]                      # F[i], i >= 1
while len(F) < 120:
    F.append(F[-1] + F[-2])


def a(i):                             # chip weight of paper index i (level i - 1)
    return F[i + 2] - i - 2


def zeck(n):
    """Zeckendorf digits as a set of levels (greedy)."""
    levels = []
    i = max(j for j in range(1, len(F)) if F[j] <= n) if n else 0
    while n:
        while F[i] > n:
            i -= 1
        levels.append(i - 1)
        n -= F[i]
        i -= 2
    return sorted(levels)


def B(n):
    return sum(a(k + 1) for k in zeck(n))


def psi(c):
    return sum(ck * a(k + 1) for k, ck in enumerate(c))


def is_lazy(K):
    if not K:
        return True
    top = max(K)
    S = set(K)
    return all(not (k not in S and k + 1 not in S) for k in range(0, top - 1))


def lazy_bruteforce(n):
    """All sets of distinct levels with value n and no two consecutive empty levels below the top."""
    top = 0
    while F[top + 1] <= n:
        top += 1
    out = []
    for r in range(0, top + 1):
        for K in itertools.combinations(range(top), r):
            if sum(F[k + 1] for k in K) == n and is_lazy(K):
                out.append(K)
    return out


def lazy_fast(n):
    """Recursive construction via the intervals [F_{t+2} - 1, F_{t+3} - 2] of lazy strings with top t."""
    K = []
    while n:
        t = 0
        while not (F[t + 2] - 1 <= n <= F[t + 3] - 2):
            t += 1
        K.append(t)
        n -= F[t + 1]
    return sorted(K)


def to_config(K, length):
    c = [0] * length
    for k in K:
        c[k] += 1
    return c


def moves(c):
    """All (kind, i, new configuration) for configuration c (tuple of counts)."""
    out = []
    L = len(c)
    def bump(cc, k, d):
        while len(cc) <= k:
            cc.append(0)
        cc[k] += d
    if L > 0 and c[0] >= 2:
        cc = list(c); bump(cc, 0, -2); bump(cc, 1, 1); out.append(("C", 1, cc))
    for i in range(2, L + 1):           # C_i: levels i-2, i-1 -> i
        if c[i - 2] >= 1 and c[i - 1] >= 1:
            cc = list(c); bump(cc, i - 2, -1); bump(cc, i - 1, -1); bump(cc, i, 1); out.append(("C", i, cc))
    if L > 1 and c[1] >= 2:
        cc = list(c); bump(cc, 1, -2); bump(cc, 0, 1); bump(cc, 2, 1); out.append(("S", 2, cc))
    for i in range(3, L + 1):           # S_i: level i-1 twice -> levels i-3, i
        if c[i - 1] >= 2:
            cc = list(c); bump(cc, i - 1, -2); bump(cc, i - 3, 1); bump(cc, i, 1); out.append(("S", i, cc))
    norm = []
    for kind, i, cc in out:
        while cc and cc[-1] == 0:
            cc.pop()
        norm.append((kind, i, tuple(cc)))
    return norm


@functools.lru_cache(maxsize=None)
def longest(c):
    best = 0
    for _, _, cc in moves(c):
        best = max(best, 1 + longest(cc))
    return best


def random_game(n, rng):
    c = (n,)
    G = []
    while True:
        ms = moves(c)
        if not ms:
            return G, c
        kind, i, cc = rng.choice(ms)
        G.append((kind, i, psi(cc) - psi(c)))
        c = cc


def split_phase_ends(n):
    """All terminal configurations of split-only play (C1 and S_i) from n chips on level 0, with the set of
    path lengths leading to each."""
    @functools.lru_cache(maxsize=None)
    def go(c):
        ms = [(k, i, cc) for k, i, cc in moves(c) if k == "S" or (k == "C" and i == 1)]
        if not ms:
            return frozenset([(c, 0)])
        res = set()
        for _, _, cc in ms:
            for end, ln in go(cc):
                res.add((end, ln + 1))
        return frozenset(res)
    return go((n,))


def main():
    n_ex = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    n_sp = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    n_ar = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
    t0 = time.time()
    rep = {"T1_move_deltas": {}, "T1_random_games_failures": 0, "T2_failures": [], "lazy_failures": [],
           "T8_failures": [], "T8_arith_failures": [], "table": []}
    rng = random.Random(7)
    # lazy representation: brute force vs fast, uniqueness
    for n in range(1, 400):
        bf = lazy_bruteforce(n)
        if len(bf) != 1 or list(bf[0]) != lazy_fast(n):
            rep["lazy_failures"].append(n)
    # T1: move deltas and the identity on random games
    for n in range(2, 300):
        for _ in range(3):
            G, end = random_game(n, rng)
            for kind, i, d in G:
                key = f"{kind}{i}"
                rep["T1_move_deltas"].setdefault(key, set()).add(d)
            if tuple(to_config(zeck(n), max(zeck(n)) + 1)) != end:
                rep["T1_random_games_failures"] += 1
            weighted = sum(i - 1 for kind, i, _ in G if kind == "C" and i >= 2)
            if len(G) != B(n) - weighted:
                rep["T1_random_games_failures"] += 1
    rep["T1_move_deltas"] = {k: sorted(v) for k, v in sorted(rep["T1_move_deltas"].items(), key=lambda kv: (kv[0][0], int(kv[0][1:])))}
    # T2 exhaustive on small n
    for n in range(1, n_sp + 1):
        ends = split_phase_ends(n)
        K = lazy_fast(n)
        lz = tuple(to_config(K, max(K) + 1))
        if {e for e, _ in ends} != {lz} or {ln for _, ln in ends} != {psi(lz)}:
            rep["T2_failures"].append(n)
    # T8 with the exhaustive longest game
    worst = 0.0
    for n in range(1, n_ex + 1):
        L = longest((n,))
        K = lazy_fast(n)
        t = max(K)
        P = psi(to_config(K, t + 1))
        Bn = B(n)
        D = Bn - L
        bound = 1 + (t + 1) * (t + 6) // 2
        ok = (L >= P) and (0 <= D <= Bn - P <= bound)
        if not ok:
            rep["T8_failures"].append((n, L, Bn, P, t))
        phi2 = ((1 + 5 ** 0.5) / 2) ** 2
        if n >= 3:
            worst = max(worst, (phi2 * n - L) / math.log(n) ** 2)
        rep["table"].append((n, L, Bn, D, P, t, bound))
    rep["max_(phi^2 n - L(n))/log(n)^2_for_n<=%d" % n_ex] = round(worst, 3)
    # arithmetic part for many n
    ratio = 0.0
    for n in range(1, n_ar + 1):
        K = lazy_fast(n)
        t = max(K)
        P = psi(to_config(K, t + 1))
        Bn = B(n)
        bound = 1 + (t + 1) * (t + 6) // 2
        if Bn - P > bound or Bn - P < 0:
            rep["T8_arith_failures"].append(n)
        ratio = max(ratio, (Bn - P) / bound)
    rep["max_(B-Psi(lazy))/bound_n<=%d" % n_ar] = round(ratio, 4)
    rep["positions_cached"] = longest.cache_info().currsize
    rep["seconds"] = round(time.time() - t0, 1)
    short = {k: v for k, v in rep.items() if k != "table"}
    print(json.dumps(short, indent=1))
    json.dump(rep, open(os.path.join(HERE, "c19_checks.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
