"""Magma cellular automata (cycle C15).

A finite magma (M, *) on {0, ..., n-1}, given by its Cayley table ``T[a, b] = a * b``, defines the
one-dimensional cellular automaton

    c'_i = c_i * c_{i+1}

on cyclic rows (indices mod L) or on one-sided infinite rows.  Its *t-step local map*
F_t : M^(t+1) -> M is F_0(x_0) = x_0 and

    F_t(x_0, ..., x_t) = F_{t-1}(x_0, ..., x_{t-1}) * F_{t-1}(x_1, ..., x_t),

so that cell i at time t equals F_t(c_i, ..., c_{i+t}).  This module computes F_t as a full table
(an array with t+1 axes), its essential variables, its ordered-BDD widths (the number of distinct
residual functions after reading a prefix, in both reading directions), the dynamics of the global
map on cyclic rows, surjectivity/injectivity on bi-infinite rows (pair-graph criterion), algebraic
properties of the table, and three fast-forward algorithms (affine, commutative-semigroup, cycle
detection) next to the direct simulation baseline.
"""

from __future__ import annotations

import itertools
import math
from functools import lru_cache

import numpy as np


# ------------------------------------------------------------------ tables and classes
def all_tables(n: int) -> np.ndarray:
    """All n^(n*n) Cayley tables as an int8 array of shape (N, n, n), in lexicographic order."""
    flat = np.array(list(itertools.product(range(n), repeat=n * n)), dtype=np.int8)
    return flat.reshape(-1, n, n)


def encode(tables: np.ndarray) -> np.ndarray:
    """Base-n code of each table (row-major), as int64."""
    n = tables.shape[-1]
    w = n ** np.arange(n * n - 1, -1, -1, dtype=np.int64)
    return tables.reshape(len(tables), -1).astype(np.int64) @ w


def transforms(tables: np.ndarray, anti: bool = True):
    """Yield every relabelling (and, if anti, transposition) of all tables at once."""
    n = tables.shape[-1]
    for p in itertools.permutations(range(n)):
        p = np.array(p, dtype=np.int8)
        inv = np.argsort(p)
        U = p[tables[:, inv][:, :, inv]]          # U[p[a], p[b]] = p[T[a, b]]
        yield U
        if anti:
            yield np.transpose(U, (0, 2, 1))


def canonical_codes(tables: np.ndarray, anti: bool = True) -> np.ndarray:
    """Minimum code over isomorphisms (and anti-isomorphisms if anti) of each table."""
    best = None
    for U in transforms(tables, anti):
        c = encode(U)
        best = c if best is None else np.minimum(best, c)
    return best


def classes(n: int, anti: bool = True):
    """Representatives (smallest code) of the magmas of order n up to isomorphism (and anti-isomorphism),
    with class sizes.  Returns (reps (K, n, n), sizes (K,), canonical codes of all tables)."""
    tabs = all_tables(n)
    can = canonical_codes(tabs, anti)
    uniq, first, counts = np.unique(can, return_index=True, return_counts=True)
    reps = tabs[first]
    # representative = the table whose own code equals the canonical code
    own = encode(tabs)
    rep_idx = {int(c): i for i, c in enumerate(own) if own[i] == can[i]}
    reps = np.stack([tabs[rep_idx[int(c)]] for c in uniq])
    return reps, counts, can


# ------------------------------------------------------------------ algebraic properties
def is_associative(T) -> bool:
    n = T.shape[0]
    a = np.arange(n)[:, None, None]
    b = np.arange(n)[None, :, None]
    c = np.arange(n)[None, None, :]
    return bool((T[T[a, b], c] == T[a, T[b, c]]).all())


def is_commutative(T) -> bool:
    return bool((T == T.T).all())


def is_medial(T) -> bool:
    n = T.shape[0]
    x, y, z, w = np.ix_(range(n), range(n), range(n), range(n))
    return bool((T[T[x, y], T[z, w]] == T[T[x, z], T[y, w]]).all())


def rows_are_permutations(T) -> bool:
    """x -> a*x bijective for every a (the CA is permutive in the right cell)."""
    n = T.shape[0]
    return all(len(set(T[a, :].tolist())) == n for a in range(n))


def cols_are_permutations(T) -> bool:
    """x -> x*b bijective for every b (the CA is permutive in the left cell)."""
    n = T.shape[0]
    return all(len(set(T[:, b].tolist())) == n for b in range(n))


def affine_form(T):
    """If T is isomorphic to x*y = a x + b y + c (mod n) for n prime, return (perm, a, b, c) with
    perm the relabelling that makes it so; else None."""
    n = T.shape[0]
    if n not in (2, 3, 5, 7):
        return None
    X = np.arange(n)[:, None]
    Y = np.arange(n)[None, :]
    for p in itertools.permutations(range(n)):
        p = np.array(p)
        inv = np.argsort(p)
        U = p[T[np.ix_(inv, inv)]]
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    if np.array_equal(U, (a * X + b * Y + c) % n):
                        return p.tolist(), a, b, c
    return None


def wolfram_rule(T) -> int:
    """Elementary-CA rule number of a 2-element magma CA c'_i = c_i * c_{i+1} (left neighbour ignored)."""
    assert T.shape == (2, 2)
    return int(sum(int(T[c, r]) << (4 * l + 2 * c + r) for l in (0, 1) for c in (0, 1) for r in (0, 1)))


# ------------------------------------------------------------------ light cones
def light_cones(T, t_max: int):
    """Yield (t, F_t) for t = 0..t_max; F_t is an array with t+1 axes of length n."""
    n = T.shape[0]
    F = np.arange(n, dtype=np.int8)
    yield 0, F
    for t in range(1, t_max + 1):
        F = T[F[..., None], F[None, ...]]
        yield t, F


def essential_variables(F) -> list[int]:
    """Indices k such that F depends on its k-th argument."""
    out = []
    for k in range(F.ndim):
        if not (F == np.take(F, [0], axis=k)).all():
            out.append(k)
    return out


def _distinct_rows(M) -> int:
    M = np.ascontiguousarray(M)
    if M.shape[1] == 0:
        return 1
    v = M.view(np.dtype((np.void, M.dtype.itemsize * M.shape[1]))).ravel()
    return int(len(np.unique(v)))


def obdd_widths(F) -> list[int]:
    """Number of distinct residual functions after reading the first k arguments, k = 0..t+1
    (the level widths of the reduced ordered BDD/branching program in the natural variable order)."""
    n = F.shape[0] if F.ndim else 1
    m = F.ndim
    flat = F.reshape(-1)
    return [_distinct_rows(flat.reshape(n ** k, n ** (m - k))) for k in range(m + 1)]


def streaming_width(F) -> tuple[int, int]:
    """(forward width, backward width): max level width reading left-to-right and right-to-left."""
    fw = max(obdd_widths(F))
    bw = max(obdd_widths(np.transpose(F, tuple(range(F.ndim - 1, -1, -1)))))
    return fw, bw


def is_constant(F) -> bool:
    return bool((F == F.flat[0]).all())


# ------------------------------------------------------------------ cyclic dynamics
@lru_cache(maxsize=None)
def _digits(n: int, L: int):
    codes = np.arange(n ** L, dtype=np.int64)
    d = ((codes[:, None] // (n ** np.arange(L, dtype=np.int64))) % n).astype(np.int8)
    return d, np.roll(d, -1, axis=1), (n ** np.arange(L, dtype=np.int64))


def cyclic_map(T, L: int) -> np.ndarray:
    """Successor code of every cyclic configuration of length L (cell i = base-n digit i)."""
    n = T.shape[0]
    d, r, w = _digits(n, L)
    return (T[d, r].astype(np.int64) * w).sum(axis=1)


def functional_graph_stats(f: np.ndarray) -> dict:
    """Periodic points, fixed points, maximal cycle length, maximal transient and bijectivity of a map
    on {0, ..., N-1} given as an array."""
    N = len(f)
    alive = np.ones(N, dtype=bool)
    transient = 0
    while True:
        img = np.zeros(N, dtype=bool)
        img[f[alive]] = True
        if (img == alive).all():
            break
        alive = img
        transient += 1
    periodic = np.nonzero(alive)[0]
    seen = np.zeros(N, dtype=bool)
    max_cycle, n_cycles = 0, 0
    lcm = 1
    for x in periodic:
        if seen[x]:
            continue
        length, y = 0, x
        while not seen[y]:
            seen[y] = True
            y = f[y]
            length += 1
        n_cycles += 1
        max_cycle = max(max_cycle, length)
        lcm = lcm * length // math.gcd(lcm, length)
    return {"periodic": int(len(periodic)), "fixed": int((f == np.arange(N)).sum()), "cycles": n_cycles,
            "max_cycle": max_cycle, "period_lcm": int(lcm), "max_transient": transient,
            "bijective": bool(len(periodic) == N)}


# ------------------------------------------------------------------ bi-infinite rows: pair graph
def _pair_graph(T):
    n = T.shape[0]
    V = [(u, v) for u in range(n) for v in range(n)]
    adj = {x: [(u2, v2) for u2 in range(n) for v2 in range(n) if T[x[0], u2] == T[x[1], v2]] for x in V}
    return V, adj


def is_surjective(T) -> bool:
    """Surjectivity on bi-infinite rows, via the Garden-of-Eden theorem: surjective iff pre-injective iff the
    pair graph has no path diagonal -> off-diagonal ... -> diagonal (a 'diamond')."""
    V, adj = _pair_graph(T)
    start = {y for x in V if x[0] == x[1] for y in adj[x] if y[0] != y[1]}
    seen, stack = set(start), list(start)
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y[0] == y[1]:
                return False
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return True


def is_injective(T) -> bool:
    """Injectivity on bi-infinite rows: no off-diagonal vertex of the pair graph lies on a bi-infinite path,
    i.e. none is both reachable from a cycle and able to reach a cycle (diagonal vertices lie on cycles)."""
    V, adj = _pair_graph(T)
    radj = {x: [] for x in V}
    for x in V:
        for y in adj[x]:
            radj[y].append(x)

    def on_cycle_closure(graph):
        # vertices with an infinite forward path = complement of those removed by repeatedly deleting sinks
        out = {x: len(graph[x]) for x in V}
        rev = {x: [] for x in V}
        for x in V:
            for y in graph[x]:
                rev[y].append(x)
        alive = set(V)
        queue = [x for x in V if out[x] == 0]
        while queue:
            x = queue.pop()
            if x not in alive:
                continue
            alive.discard(x)
            for p in rev[x]:
                if p in alive:
                    out[p] -= 1
                    if out[p] == 0:
                        queue.append(p)
        return alive

    forward_infinite = on_cycle_closure(adj)      # vertices starting an infinite forward path
    backward_infinite = on_cycle_closure(radj)    # vertices ending an infinite backward path
    return not any(x[0] != x[1] and x in forward_infinite and x in backward_infinite for x in V)


# ------------------------------------------------------------------ fast-forward algorithms
def direct(T, row, t: int):
    """Baseline: t steps of direct simulation on a cyclic row (numpy, O(L t))."""
    row = np.asarray(row)
    for _ in range(t):
        row = T[row, np.roll(row, -1)]
    return row


def _cyclic_mul(p, q, mod: int):
    """Product of two operators sum_j p_j S^j, sum_j q_j S^j modulo S^L - 1 and mod, via FFT (exact for
    the sizes used here: coefficients < mod <= 64, L <= 2^16)."""
    L = len(p)
    fp = np.fft.rfft(p.astype(np.float64))
    fq = np.fft.rfft(q.astype(np.float64))
    r = np.fft.irfft(fp * fq, n=L)
    return (np.rint(r).astype(np.int64)) % mod


def operator_power(coeffs, t: int, mod: int):
    """(sum_j coeffs_j S^j)^t modulo S^L - 1 and mod, by binary exponentiation."""
    L = len(coeffs)
    result = np.zeros(L, dtype=np.int64)
    result[0] = 1 % mod
    base = np.asarray(coeffs, dtype=np.int64) % mod
    while t:
        if t & 1:
            result = _cyclic_mul(result, base, mod)
        t >>= 1
        if t:
            base = _cyclic_mul(base, base, mod)
    return result


def apply_operator(coeffs, row, mod: int):
    """(sum_j coeffs_j S^j row)_i = sum_j coeffs_j row_{i+j} (mod), S the left shift; via FFT."""
    L = len(row)
    # cyclic correlation: out_i = sum_j c_j r_{i+j}  =  IFFT( conj(FFT(c)) * FFT(r) )
    fc = np.fft.rfft(np.asarray(coeffs, dtype=np.float64))
    fr = np.fft.rfft(np.asarray(row, dtype=np.float64))
    out = np.fft.irfft(np.conj(fc) * fr, n=L)
    return np.rint(out).astype(np.int64) % mod


def affine_fast_forward(a: int, b: int, c: int, n: int, row, t: int):
    """Row after t steps of x*y = a x + b y + c (mod n) on a cyclic row: P^t row + c (1 + q + ... + q^(t-1)) with
    P = a + b S (S the left shift) and q = a + b; O(L log L log t)."""
    L = len(row)
    coeffs = np.zeros(L, dtype=np.int64)
    coeffs[0] = a % n
    coeffs[1 % L] = (coeffs[1 % L] + b) % n
    Pt = operator_power(coeffs, t, n)
    lin = apply_operator(Pt, row, n)
    # geometric sum sum_{s<t} q^s mod n, assembled from blocks of length 2^k (binary digits of t)
    q = (a + b) % n
    block_sum, block_pow = 1 % n, q          # sum_{s<2^k} q^s and q^(2^k)
    acc_g, acc_p, tt = 0, 1, t
    while tt:
        if tt & 1:
            acc_g = (acc_g + acc_p * block_sum) % n
            acc_p = (acc_p * block_pow) % n
        tt >>= 1
        block_sum = (block_sum + block_pow * block_sum) % n
        block_pow = (block_pow * block_pow) % n
    return (lin + c * acc_g) % n


def element_powers(T, x: int, upto: int):
    """x^1, x^2, ..., x^upto in a semigroup (x^m = x * x^(m-1))."""
    out = [x]
    for _ in range(upto - 1):
        out.append(int(T[out[-1], x]))
    return out


def index_period(T, x: int):
    """Index i and period p of the cyclic subsemigroup generated by x: x^(i+p) = x^i, minimal."""
    n = T.shape[0]
    seen = {}
    v, m = x, 1
    while v not in seen:
        seen[v] = m
        v = int(T[v, x])
        m += 1
    i = seen[v]
    return i, m - i


def commutative_semigroup_fast_forward(T, row, t: int):
    """Row after t steps on a cyclic row for a commutative semigroup table T, using
    F_t(x_0..x_t) = prod_k x_k^C(t,k) (Theorem 1): cell i = prod_j c_{i+j}^(N_j) with N_j = sum_{k = j mod L} C(t,k),
    the coefficients of (1 + S)^t mod S^L - 1.  Exponents are reduced with the index/period of each element; valid
    for t >= 2L + max index (smaller t: direct simulation)."""
    row = np.asarray(row)
    L = len(row)
    n = T.shape[0]
    ip = [index_period(T, x) for x in range(n)]
    imax = max(i for i, _ in ip)
    if t < 2 * L + imax + 1:
        return direct(T, row, t)
    M = 1
    for _, p in ip:
        M = M * p // math.gcd(M, p)
    coeffs = np.zeros(L, dtype=np.int64)
    coeffs[0] = 1
    coeffs[1 % L] += 1
    N = operator_power(coeffs, t, M)          # N_j mod M; every true N_j >= imax here
    # power lookup: pw[x][e] = x^(i_x + ((e - i_x) mod p_x)) for residues e mod M
    pw = np.zeros((n, M), dtype=np.int8)
    for x in range(n):
        i, p = ip[x]
        powers = element_powers(T, x, i + p)          # x^1 .. x^(i+p)
        for e in range(M):
            # smallest exponent m >= i with m = e (mod p); true exponent is huge and = e (mod M), M multiple of p
            m = i + ((e - i) % p)
            pw[x, e] = powers[m - 1]
    out = None
    for j in range(L):
        vals = pw[np.roll(row, -j), N[j]]
        out = vals if out is None else T[out, vals]
    return out


def cycle_fast_forward(T, row, t: int, cap: int = 200_000):
    """Simulate a cyclic row, remembering every state, until a state repeats; then jump to time t.
    Returns (row_t or None if no repetition within cap steps and t > cap, steps_simulated, mu, lam)."""
    row = np.asarray(row, dtype=np.int8)
    seen = {row.tobytes(): 0}
    history = [row]
    for s in range(1, min(t, cap) + 1):
        row = T[row, np.roll(row, -1)]
        key = row.tobytes()
        if key in seen:
            mu = seen[key]
            lam = s - mu
            idx = mu + (t - mu) % lam if t >= mu else t
            return history[idx], s, mu, lam
        seen[key] = s
        history.append(row)
    if t <= cap:
        return row, t, None, None
    return None, cap, None, None
