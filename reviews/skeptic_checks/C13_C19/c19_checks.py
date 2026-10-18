"""Skeptic checks for cycle C19 (own code; does not import systems/ or lab/).

Inputs produced by the C programs in this directory:
  out/c19_exact_*.txt    exhaustive DP (c19_exact.c): n, #positions, L, B, D, split length, lazy digits, flags
  out/c19_greedy.txt     strategy simulation for all n < NMAX (c19_greedy.c): n, L, W, B, split length, lazy ok
Checks:
  (1) Conjecture CLM-C19-05 (own implementation of the recursion as stated in the claim) against the exact DP
      (n <= 200, independent of the Cusenza strategy theorem) and against the strategy simulation (n < NMAX).
  (2) CLM-C19-03 / Theorem 4: L(F_k) formula vs exact DP (F_k <= 200) and vs a phase-2 simulation for k <= 90.
  (3) CLM-C19-06 two-summand law; CLM-C19-09 (D <= h(top), L strictly increasing).
  (4) Refuted hypotheses CLM-C19-10..13: n = 12; (4,2) ambiguity; lazy-run rank test; insertion (n = 3, count).
  (5) Large random n (up to 10^15): recursion vs phase-2 simulation started from the lazy representation.
"""
import json
import os
import random
import sys
from fractions import Fraction
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

FIB = [1, 2]
while len(FIB) < 120:
    FIB.append(FIB[-1] + FIB[-2])           # FIB[k] = F_{k+1}, level k


def h(k):
    return k * k // 4


def zeck(n):
    """Levels of the Zeckendorf representation (greedy), highest first."""
    out = []
    k = len(FIB) - 1
    while n:
        while FIB[k] > n:
            k -= 1
        out.append(k)
        n -= FIB[k]
        k -= 2
    return out


def B(n):
    return sum(FIB[k + 2] - (k + 1) - 2 for k in zeck(n))


def top_level(n):
    return zeck(n)[0]


# ---------------------------------------------------------------- the conjectured recursion, from the claim text
@lru_cache(maxsize=None)
def rho(p, m):
    if m == 0:
        return 0
    i = top_level(m)
    t = m - FIB[i]
    if i == 0:
        r = 1
    elif i % 2 == p:
        r = h(i) + 2
    else:
        r = h(i + 1) + 1
    if i % 2 == p:
        return r + max(0, rho(p, t) - h(i - 2))
    return r


@lru_cache(maxsize=None)
def D_rec(n):
    if n == 0:
        return 0
    j = top_level(n)
    m = n - FIB[j]
    return h(j) + D_rec(m) - rho(j % 2, m)


# ---------------------------------------------------------------- lazy representation and phase-2 simulation
def lazy(n):
    """Lazy digits (level 0 first), constructed from the definition: the top level t is the unique t with
    F_{t+2} - 1 <= n <= F_{t+3} - 2 (sum of all levels 0..t is FIB[t+2] - 2); then recurse on the rest with
    the constraint that the remainder must again be lazy with top >= t - 2.  Implemented by a search that is
    verified against the definition."""
    if n == 0:
        return []
    t = 0
    while FIB[t + 2] - 2 < n:
        t += 1
    d = [0] * (t + 1)
    rem = n
    for k in range(t, -1, -1):
        below = FIB[k + 1] - 2          # sum of levels 0..k-1
        if rem > below:
            d[k] = 1
            rem -= FIB[k]
    assert rem == 0
    # definition check
    assert all(x in (0, 1) for x in d) and d[-1] == 1
    assert not any(d[k] == 0 and d[k + 1] == 0 for k in range(t))
    assert sum(FIB[k] for k, x in enumerate(d) if x) == n
    return d


def strategy_from(c):
    """Play the Cusenza strategy (lowest split-type move first, else smallest combine) from configuration c
    (list of counts); return (moves, W)."""
    c = list(c) + [0] * 8
    moves = W = 0
    lo = 0                      # every level below lo holds <= 1 chip
    while True:
        if any(c[-4:]):
            c += [0] * 8
        k = next((j for j in range(lo, len(c)) if c[j] >= 2), None)
        if k is not None:
            c[k] -= 2
            if k == 0:
                c[1] += 1
            elif k == 1:
                c[0] += 1
                c[2] += 1
            else:
                c[k - 2] += 1
                c[k + 1] += 1
            moves += 1
            lo = max(0, k - 2)
            continue
        m = next((j for j in range(len(c) - 1) if c[j] and c[j + 1]), None)
        if m is None:
            return moves, W, c
        c[m] -= 1
        c[m + 1] -= 1
        c[m + 2] += 1
        moves += 1
        W += m + 1
        lo = m


def D_phase2(n):
    """Deficit of the strategy game, computed from lazy(n) (Theorem 2: phase 1 ends there and has no combine)."""
    _, W, _ = strategy_from(lazy(n))
    return W


# ---------------------------------------------------------------- exact longest game from a position (small n)
def moves(c):
    c = tuple(c)
    out = []
    n = len(c)
    g = lambda k: c[k] if k < n else 0
    for k in range(n):
        if c[k] >= 2:
            d = list(c) + [0, 0]
            d[k] -= 2
            if k == 0:
                d[1] += 1
            elif k == 1:
                d[0] += 1
                d[2] += 1
            else:
                d[k - 2] += 1
                d[k + 1] += 1
            out.append(tuple(d))
        if c[k] and g(k + 1):
            d = list(c) + [0, 0]
            d[k] -= 1
            d[k + 1] -= 1
            d[k + 2] += 1
            out.append(tuple(d))
    return [tuple(_trim(x)) for x in out]


def _trim(x):
    x = list(x)
    while x and x[-1] == 0:
        x.pop()
    return x


def longest_from(c):
    memo = {}

    def f(p):
        if p in memo:
            return memo[p]
        ms = moves(p)
        v = 0 if not ms else 1 + max(f(q) for q in ms)
        memo[p] = v
        return v
    sys.setrecursionlimit(100000)
    return f(tuple(_trim(c)))


def read_exact():
    rows = {}
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith("c19_exact_") and fn.endswith(".txt"):
            for line in open(os.path.join(OUT, fn)):
                p = line.split()
                rows[int(p[0])] = {"states": int(p[1]), "L": int(p[2]), "B": int(p[3]), "D": int(p[4])}
    return rows


def read_greedy():
    L, W, Bv, SL, LZ = [], [], [], [], []
    for line in open(os.path.join(OUT, "c19_greedy.txt")):
        n, l, w, b, sl, lz = map(int, line.split())
        assert n == len(L)
        L.append(l)
        W.append(w)
        Bv.append(b)
        SL.append(sl)
        LZ.append(lz)
    return L, W, Bv, SL, LZ


def lazy_runs(n):
    d = lazy(n)
    out, k = [], 0
    while k < len(d):
        if d[k]:
            s = k
            while k < len(d) and d[k]:
                k += 1
            out.append((s, k - s))
        else:
            k += 1
    return out


def rank(rows, ncols):
    M = [[Fraction(x) for x in r] for r in rows]
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def main():
    res = {}
    ex = read_exact()
    nmax_exact = max(ex)
    # (1) recursion vs exact DP
    bad = [n for n in sorted(ex) if D_rec(n) != ex[n]["D"]]
    res["recursion_vs_exact"] = {"n_values": len(ex), "max_n": nmax_exact, "mismatches": bad}
    print("recursion vs exact DP on", len(ex), "values n <=", nmax_exact, "mismatches:", bad)
    # B formula check vs exact program's B
    assert all(B(n) == ex[n]["B"] for n in ex)
    # (2) Theorem 4 vs exact
    th4 = []
    for k in range(1, 40):
        n = FIB[k - 1]                               # F_k (paper index k)
        formula = FIB[k + 1] - k - 2 - (k - 1) ** 2 // 4  # F_{k+2} - k - 2 - floor((k-1)^2/4)
        if n in ex:
            th4.append((k, n, ex[n]["L"], formula))
    res["thm4_vs_exact"] = th4
    print("Theorem 4 vs exact DP:", [(k, n, L == f) for k, n, L, f in th4])
    # (2b) Theorem 4 vs phase-2 strategy simulation, levels j <= 89
    bad4 = []
    for j in range(0, 90):
        n = FIB[j]
        if D_phase2(n) != h(j):
            bad4.append(j)
        Lsim = B(n) - D_phase2(n)
        k = j + 1
        if Lsim != FIB[k + 1] - k - 2 - (k - 1) ** 2 // 4:
            bad4.append(("L", j))
    res["thm4_phase2_bad_levels_le_89"] = bad4
    print("Theorem 4 vs phase-2 simulation, levels <= 89: bad", bad4)
    # (1b) recursion vs greedy simulation, all n < NMAX
    L, W, Bv, SL, LZ = read_greedy()
    NM = len(L)
    assert all(Bv[n] == B(n) for n in range(0, NM, 997))
    badg = [n for n in range(NM) if W[n] != D_rec(n)]
    res["recursion_vs_greedy"] = {"range": [0, NM - 1], "mismatches": badg[:20], "n_mismatches": len(badg)}
    print("recursion vs strategy simulation, n <", NM, ": mismatches", len(badg), badg[:10])
    agree_exact = [n for n in sorted(ex) if n < NM and L[n] != ex[n]["L"]]
    print("greedy vs exact DP (n <= %d): mismatches" % min(NM - 1, nmax_exact), agree_exact)
    res["greedy_vs_exact_mismatch"] = agree_exact
    # (3) CLM-C19-09
    viol_top = [n for n in range(1, NM) if W[n] > h(top_level(n))]
    viol_mono = [n for n in range(1, NM - 1) if L[n + 1] <= L[n]]
    eq_top = [n for n in range(1, 400) if W[n] == h(top_level(n)) and h(top_level(n)) > 0]
    res["clm09"] = {"range": [1, NM - 1], "D_gt_h_top": viol_top[:10], "L_not_increasing": viol_mono[:10],
                    "equality_cases_below_400": eq_top}
    print("CLM-C19-09: D>h(top):", len(viol_top), " L non-increasing:", len(viol_mono),
          " equality D=h(top)>0 for n<400:", eq_top)
    # (3b) CLM-C19-06 two-summand law, j <= 24 by greedy table, 25..60 by phase-2 simulation
    def R2(j, i):
        if i == 0:
            return 1
        return (i + 1) ** 2 // 4 + 1 if (j - i) % 2 else i * i // 4 + 2
    bad2, n2 = [], 0
    for j in range(2, 61):
        for i in range(0, j - 1):
            n = FIB[j] + FIB[i]
            D = W[n] if n < NM else D_phase2(n)
            n2 += 1
            if D != h(j) + h(i) - R2(j, i):
                bad2.append((j, i))
    res["two_summand"] = {"pairs": n2, "bad": bad2[:20]}
    print("two-summand law, j <= 60:", n2, "pairs, violations", len(bad2), bad2[:5])
    # (4) refuted hypotheses
    D = W
    lv12 = zeck(12)
    model = sum(h(j) for j in lv12) - sum(R2(a, b) for a, b in zip(lv12, lv12[1:]))
    res["H1_n12"] = {"levels": lv12, "D": D[12], "model": model}
    print("H-C19-1 at n = 12: levels", lv12, "D", D[12], "model", model)
    print("H-C19-2: D(11)-D(3) =", D[11] - D[3], " D(12)-D(4) =", D[12] - D[4], " levels", zeck(11), zeck(12))
    res["H2"] = {"D11-D3": D[11] - D[3], "D12-D4": D[12] - D[4]}
    data = [(lazy_runs(n), D[n]) for n in range(1, 160)]
    runs = sorted({r for rs, _ in data for r in rs})
    idx = {r: c for c, r in enumerate(runs)}
    Am = [[sum(1 for r in rs if idx[r] == c) for c in range(len(runs))] for rs, _ in data]
    Ab = [row + [dv] for row, (_, dv) in zip(Am, data)]
    rA, rAb = rank(Am, len(runs)), rank(Ab, len(runs) + 1)
    res["H3_rank"] = {"distinct_runs": len(runs), "rank_A": rA, "rank_Ab": rAb}
    print("H-C19-3 lazy-run model, n < 160: runs", len(runs), "rank", rA, "augmented", rAb)
    fails, first = 0, []
    for m in range(300):
        z = [0] * (top_level(m) + 1 if m else 1)
        for k in zeck(m):
            z[k] = 1
        z[0] += 1
        lam = longest_from(z)
        if L[m + 1] != L[m] + lam:
            fails += 1
            if len(first) < 3:
                first.append((m, L[m + 1], L[m], lam))
    res["H4"] = {"fails_m_lt_300": fails, "first": first}
    print("H-C19-4: fails for", fails, "of 300; first", first)
    # (5) large random n: recursion vs phase-2 simulation
    rng = random.Random(1919)
    big = [rng.randrange(10 ** 6, 10 ** 15) for _ in range(3000)] + [FIB[j] + rng.randrange(0, FIB[j - 1])
                                                                       for j in range(30, 70) for _ in range(20)]
    badbig = [n for n in big if D_rec(n) != D_phase2(n)]
    res["large_random"] = {"tested": len(big), "mismatches": badbig[:10]}
    print("recursion vs phase-2 simulation on", len(big), "large n:", len(badbig), "mismatches", badbig[:3])
    # asymptotic ratio with phase-2 (strategy) values, not the recursion
    import math
    PHI = (1 + 5 ** 0.5) / 2
    asym = []
    for e in (3, 4, 5, 6, 7, 9, 12, 18):
        n = 10 ** e
        Lv = B(n) - D_phase2(n)
        asym.append((e, Lv, round((PHI ** 2 * n - Lv) / math.log(n, PHI) ** 2, 4), D_rec(n) == D_phase2(n)))
    res["asymptotics_phase2"] = asym
    print("asymptotic ratio (phase-2 strategy values):", asym)
    json.dump(res, open(os.path.join(OUT, "c19_checks.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
