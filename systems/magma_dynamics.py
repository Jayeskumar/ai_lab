"""Fibonacci dynamics in finite magmas (cycle C16, System E2).

A finite magma (M, *) with M = {0, ..., n-1} and Cayley table T[a, b] = a * b defines the order-2 recurrence

    x_{k+1} = x_k * x_{k-1}                      (forward)
    x_{k+1} = x_{k-1} * x_k                      (mirror  = forward recurrence of the opposite magma)

and hence the *pair map* P(a, b) = (b, b * a) on the n^2 states (x_{k-1}, x_k) = (a, b), encoded as s = a*n + b.
Every function M x M -> M is the feedback of some magma, so the pair maps of n-element magmas are exactly the
order-2 feedback shift registers over an n-letter alphabet.

This module computes the functional graph of P: cycles, periods, transients; batched versions handle all magmas of
order <= 3 and all row-permutation magmas of order 4 at once.
"""

from __future__ import annotations

import itertools
from collections import Counter
from math import factorial, gcd

import numpy as np


# ------------------------------------------------------------------ pair maps
def pair_next(T: np.ndarray, mirror: bool = False) -> np.ndarray:
    """Successor array of the pair map: state a*n + b -> b*n + (b*a)  (mirror: b*n + (a*b))."""
    T = np.asarray(T, dtype=np.int64)
    n = T.shape[0]
    a = np.repeat(np.arange(n), n)
    b = np.tile(np.arange(n), n)
    c = T[a, b] if mirror else T[b, a]
    return b * n + c


def analyze(nxt: np.ndarray) -> dict:
    """Cycle structure of a functional graph given by a successor array (O(S) time, iterative)."""
    nxt = np.asarray(nxt, dtype=np.int64)
    S = nxt.size
    state = np.zeros(S, dtype=np.int8)        # 0 unseen, 1 on current path, 2 done
    on_cycle = np.zeros(S, dtype=bool)
    cycle_lengths = Counter()
    nl = nxt.tolist()
    st = state  # alias
    for s0 in range(S):
        if st[s0]:
            continue
        path = []
        v = s0
        while st[v] == 0:
            st[v] = 1
            path.append(v)
            v = nl[v]
        if st[v] == 1:                         # found a new cycle starting at v
            i = path.index(v)
            cyc = path[i:]
            cycle_lengths[len(cyc)] += 1
            for u in cyc:
                on_cycle[u] = True
        for u in path:
            st[u] = 2
    # transients: distance to the cycle set, by reverse BFS
    indeg_lists = [[] for _ in range(S)]
    for u in range(S):
        indeg_lists[nl[u]].append(u)
    dist = np.full(S, -1, dtype=np.int64)
    frontier = list(np.nonzero(on_cycle)[0])
    for u in frontier:
        dist[u] = 0
    d = 0
    while frontier:
        d += 1
        new = []
        for v in frontier:
            for u in indeg_lists[v]:
                if dist[u] < 0:
                    dist[u] = d
                    new.append(u)
        frontier = new
    is_perm = bool(np.unique(nxt).size == S)
    return {
        "states": S,
        "is_permutation": is_perm,
        "n_cycles": int(sum(cycle_lengths.values())),
        "cycle_lengths": {int(k): int(v) for k, v in sorted(cycle_lengths.items())},
        "max_period": int(max(cycle_lengths)) if cycle_lengths else 0,
        "periodic_states": int(on_cycle.sum()),
        "max_transient": int(dist.max()),
    }


def batch_analyze(nxt: np.ndarray) -> dict:
    """Vectorised cycle statistics for a batch of successor arrays of shape (B, S).

    Returns arrays (length B): max_period, n_cycles, periodic_states, max_transient, is_permutation."""
    nxt = np.asarray(nxt, dtype=np.int64)
    B, S = nxt.shape
    rows = np.arange(B)[:, None]
    # land on cycles: apply the map S times (doubling)
    pos = np.tile(np.arange(S), (B, 1))
    step = nxt.copy()
    k = S
    while k:
        if k & 1:
            pos = step[rows, pos]
        step = step[rows, step]
        k >>= 1
    on_cycle = np.zeros((B, S), dtype=bool)
    on_cycle[rows, pos] = True                     # image of f^S = set of periodic states
    # period of each periodic state: least t >= 1 with f^t(v) = v
    period = np.zeros((B, S), dtype=np.int64)
    cur = nxt.copy()
    idx = np.tile(np.arange(S), (B, 1))
    for t in range(1, S + 1):
        hit = (cur == idx) & on_cycle & (period == 0)
        period[hit] = t
        if not (on_cycle & (period == 0)).any():
            break
        cur = nxt[rows, cur]
    max_period = period.max(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        inv = np.where(on_cycle, 1.0 / np.maximum(period, 1), 0.0)
    n_cycles = np.rint(inv.sum(axis=1)).astype(np.int64)
    # transients: number of steps until the orbit is on a cycle
    trans = np.zeros((B, S), dtype=np.int64)
    cur = idx.copy()
    for t in range(S + 1):
        oc = on_cycle[rows, cur]
        trans[~oc] = t + 1
        if oc.all():
            break
        cur = nxt[rows, cur]
    is_perm = np.array([np.unique(r).size == S for r in nxt]) if B <= 2000 else \
        (np.sort(nxt, axis=1) == np.arange(S)).all(axis=1)
    return {"max_period": max_period, "n_cycles": n_cycles, "periodic_states": on_cycle.sum(axis=1),
            "max_transient": trans.max(axis=1), "is_permutation": is_perm}


# ------------------------------------------------------------------ families of tables
def all_magmas(n: int) -> np.ndarray:
    """All n^(n^2) tables of order n as an array (B, n, n) (n <= 3)."""
    cells = n * n
    B = n ** cells
    codes = np.arange(B)
    digits = np.zeros((B, cells), dtype=np.int64)
    for i in range(cells):
        digits[:, cells - 1 - i] = codes % n
        codes //= n
    return digits.reshape(B, n, n)


def row_permutation_magmas(n: int) -> np.ndarray:
    """All tables whose rows (left translations L_a = a * .) are permutations: (n!)^n tables."""
    perms = np.array(list(itertools.permutations(range(n))), dtype=np.int64)
    idx = np.array(list(itertools.product(range(len(perms)), repeat=n)), dtype=np.int64)
    return perms[idx]                               # (B, n, n): row a = perms[idx[:, a]]


def batch_pair_next(tables: np.ndarray, mirror: bool = False) -> np.ndarray:
    """Pair-map successor arrays for a batch of tables (B, n, n) -> (B, n^2)."""
    B, n, _ = tables.shape
    a = np.repeat(np.arange(n), n)
    b = np.tile(np.arange(n), n)
    c = tables[:, a, b] if mirror else tables[:, b, a]
    return b[None, :] * n + c


def canonical_codes(tables: np.ndarray) -> np.ndarray:
    """Isomorphism-invariant code of each table (minimum over relabellings of the base-n encoding)."""
    B, n, _ = tables.shape
    weights = n ** np.arange(n * n - 1, -1, -1, dtype=np.int64)
    best = None
    for p in itertools.permutations(range(n)):
        p = np.array(p)
        inv = np.argsort(p)
        U = p[tables[:, inv[:, None], inv[None, :]]]          # relabelled tables
        code = (U.reshape(B, -1) * weights).sum(axis=1)
        best = code if best is None else np.minimum(best, code)
    return best


def latin_squares(n: int) -> np.ndarray:
    """All Latin squares of order n (backtracking; n <= 5)."""
    out = []
    sq = -np.ones((n, n), dtype=np.int64)
    rows_used = [set() for _ in range(n)]
    cols_used = [set() for _ in range(n)]

    def rec(k):
        if k == n * n:
            out.append(sq.copy())
            return
        i, j = divmod(k, n)
        for v in range(n):
            if v not in rows_used[i] and v not in cols_used[j]:
                sq[i, j] = v
                rows_used[i].add(v)
                cols_used[j].add(v)
                rec(k + 1)
                rows_used[i].discard(v)
                cols_used[j].discard(v)
        sq[i, j] = -1

    rec(0)
    return np.array(out, dtype=np.int64)


def affine_table(N: int, alpha: int, beta: int, gamma: int) -> np.ndarray:
    x = np.arange(N)
    return (alpha * x[:, None] + beta * x[None, :] + gamma) % N


# ------------------------------------------------------------------ arithmetic helpers
def pisano(m: int) -> int:
    """Pisano period pi(m): period of the Fibonacci numbers modulo m (pi(1) = 1)."""
    if m == 1:
        return 1
    a, b, k = 0, 1, 0
    while True:
        a, b = b, (a + b) % m
        k += 1
        if a == 0 and b == 1:
            return k


def matrix_order_mod(M, N: int, limit: int = 10 ** 7) -> int | None:
    """Multiplicative order of a 2x2 integer matrix modulo N (None if not invertible or limit exceeded)."""
    (a, b), (c, d) = M
    if gcd((a * d - b * c) % N, N) != 1:
        return None
    I = ((1 % N, 0), (0, 1 % N))
    X = ((a % N, b % N), (c % N, d % N))
    P = X
    k = 1
    while P != I:
        (p, q), (r, s) = P
        P = (((p * a + q * c) % N, (p * b + q * d) % N), ((r * a + s * c) % N, (r * b + s * d) % N))
        k += 1
        if k > limit:
            return None
    return k


def de_bruijn_count(n: int) -> int:
    """Number of de Bruijn cycles of order 2 over n symbols: (n!)^n / n^2 (van Aardenne-Ehrenfest--de Bruijn)."""
    return factorial(n) ** n // (n * n)


# ------------------------------------------------------------------ full-period quasigroups (universal cycles)
def table_from_cycle(seq) -> np.ndarray:
    """Magma whose pair map follows the cyclic sequence: T[b, a] = symbol after the consecutive pair (a, b)."""
    L = len(seq)
    n = int(round(L ** 0.5))
    T = -np.ones((n, n), dtype=np.int64)
    for i in range(L):
        a, b, c = seq[i - 1], seq[i], seq[(i + 1) % L]
        if T[b, a] not in (-1, c):
            raise ValueError("pair occurs twice with different successors")
        T[b, a] = c
    return T


def is_latin_table(T) -> bool:
    T = np.asarray(T)
    n = T.shape[0]
    r = np.arange(n)
    return bool((np.sort(T, axis=1) == r).all() and (np.sort(T, axis=0) == r[:, None]).all())


def _uc_dfs(n: int, count: bool, node_budget: int):
    """DFS over cyclic sequences of length n^2 starting with 0, 0 in which all ordered pairs at distance 1 and at
    distance 2 are distinct.  Every such cycle contains the pair (0, 0) exactly once, so rotating it to the front
    gives a bijection with full-period quasigroups (Theorem 4 of proofs/paper/C16.md).
    Returns (count or first sequence, nodes used, complete flag)."""
    import sys
    sys.setrecursionlimit(max(10000, 4 * n * n))
    L = n * n
    seq = [0, 0]
    u1 = [[False] * n for _ in range(n)]
    u2 = [[False] * n for _ in range(n)]
    u1[0][0] = True
    state = {"nodes": 0, "count": 0, "first": None, "stopped": False}

    def rec():
        state["nodes"] += 1
        if state["nodes"] > node_budget:
            state["stopped"] = True
            return True
        if len(seq) == L:
            a, b = seq[-2], seq[-1]
            x0, x1 = seq[0], seq[1]
            if not u1[b][x0] and not u2[a][x0] and not u2[b][x1] and (a, x0) != (b, x1):
                state["count"] += 1
                if state["first"] is None:
                    state["first"] = list(seq)
                return not count
            return False
        a, b = seq[-2], seq[-1]
        for v in range(n):
            if u1[b][v] or u2[a][v]:
                continue
            seq.append(v)
            u1[b][v] = True
            u2[a][v] = True
            stop = rec()
            seq.pop()
            u1[b][v] = False
            u2[a][v] = False
            if stop:
                return True
        return False

    rec()
    complete = not state["stopped"]
    return (state["count"] if count else state["first"]), state["nodes"], complete


def count_universal_cycles(n: int, node_budget: int = 10 ** 8):
    return _uc_dfs(n, True, node_budget)


def first_universal_cycle(n: int, node_budget: int = 10 ** 7):
    return _uc_dfs(n, False, node_budget)


def universal_cycle_sat(n: int, conf_budget: int | None = None):
    """SAT encoding (CaDiCaL via pysat): a cyclic sequence of length n^2 with every ordered pair exactly once at
    distance 1 and exactly once at distance 2, normalised to start with 0, 0.  Returns (status, sequence)."""
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Cadical153
    L = n * n
    P = IDPool()

    def s(i, v):
        return P.id(("s", i % L, v))

    cl = []
    for i in range(L):
        cl += CardEnc.equals([s(i, v) for v in range(n)], 1, vpool=P, encoding=EncType.pairwise).clauses
    cl += [[s(0, 0)], [s(1, 0)]]
    for d in (1, 2):
        for u in range(n):
            for v in range(n):
                lits = []
                for i in range(L):
                    t = P.id(("t", d, i, u, v))
                    cl += [[-t, s(i, u)], [-t, s(i + d, v)], [t, -s(i, u), -s(i + d, v)]]
                    lits.append(t)
                cl += CardEnc.equals(lits, 1, vpool=P, encoding=EncType.seqcounter).clauses
    with Cadical153(bootstrap_with=cl) as S:
        if conf_budget is None:
            ok = S.solve()
        else:
            S.conf_budget(conf_budget)
            ok = S.solve_limited()
        if ok is None:
            return "UNKNOWN", None
        if not ok:
            return "UNSAT", None
        m = set(x for x in S.get_model() if x > 0)
        return "SAT", [next(v for v in range(n) if s(i, v) in m) for i in range(L)]


def product_table(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Direct product of two magmas, elements (i, j) encoded as i * |B| + j."""
    n1, n2 = A.shape[0], B.shape[0]
    i = np.repeat(np.arange(n1), n2)
    j = np.tile(np.arange(n2), n1)
    return (A[i[:, None], i[None, :]] * n2 + B[j[:, None], j[None, :]]).astype(np.int64)


def left_division_table(T: np.ndarray) -> np.ndarray:
    """D[b, c] = the a with b * a = c (defined when every row is a permutation)."""
    n = T.shape[0]
    D = np.zeros_like(T)
    for b in range(n):
        D[b, T[b]] = np.arange(n)
    return D


def row_sign_product(T: np.ndarray) -> int:
    """Product over b of the signs of the left translations a -> b * a (each must be a permutation)."""
    sgn = 1
    for row in np.asarray(T):
        seen = np.zeros(len(row), dtype=bool)
        for s0 in range(len(row)):
            if seen[s0]:
                continue
            length, v = 0, s0
            while not seen[v]:
                seen[v] = True
                v = row[v]
                length += 1
            if length % 2 == 0:
                sgn = -sgn
    return sgn
