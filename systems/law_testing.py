"""Algorithms that decide whether a finite magma (Cayley table T, T[a, b] = a*b) is associative (cycle C17).

Every function returns (verdict, probes) where ``probes`` counts table look-ups of the form T[a, b]; this is the
machine-independent cost measure used in the benchmarks (wall-clock times are recorded separately).

* ``naive``        - all n^3 triples (vectorised in slices).
* ``light``        - Light's test: if the set S generates the magma, it is associative iff (x*s)*y = x*(s*y)
                     for all x, y and all s in S (cost 4 n^2 |S|).
* ``anchored``     - for an anchored magma (x*0 = x+1 mod n) associativity holds iff x*(y+1) = (x*y)+1 for all
                     x, y (C06 Theorem 1: this identity forces x*y = x+y+1); cost 2 n^2.
* ``rajagopalan_schulman`` - randomised one-sided test over GF(2): random subsets u, v, w; compare the formal
                     products (u*v)*w and u*(v*w) in the magma algebra; cost O(n^2) per round.
* ``random_triples`` - sample random triples (cost 4 per triple).
* ``generating_set`` - greedy generating set (cost counted separately).
"""

from __future__ import annotations

import numpy as np


def naive(T: np.ndarray, slab: int = 64):
    n = T.shape[0]
    probes = 0
    for a0 in range(0, n, slab):
        A = np.arange(a0, min(n, a0 + slab))
        ab = T[A, :]                                   # (s, n): a*b
        left = T[ab[:, :, None], np.arange(n)[None, None, :]]   # (a*b)*c
        right = T[A[:, None, None], T[None, :, :]]               # a*(b*c)
        probes += 4 * len(A) * n * n
        if not np.array_equal(left, right):
            return False, probes
    return True, probes


def light(T: np.ndarray, gens):
    n = T.shape[0]
    probes = 0
    for s in gens:
        xs = T[:, s]                      # x*s
        sy = T[s, :]                      # s*y
        left = T[xs, :]                   # (x*s)*y
        right = T[:, sy]                  # x*(s*y)
        probes += 2 * n + 2 * n * n
        if not np.array_equal(left, right):
            return False, probes
    return True, probes


def anchored(T: np.ndarray):
    """Decide associativity of an anchored magma (requires T[x, 0] = x+1 mod n for all x)."""
    n = T.shape[0]
    x = np.arange(n)
    if not np.array_equal(T[:, 0], (x + 1) % n):
        raise ValueError("not anchored")
    ok = np.array_equal(T[:, (x + 1) % n], (T + 1) % n)
    return bool(ok), 2 * n * n


def _formal_product(T: np.ndarray, u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """(sum_a u_a a) * (sum_b v_b b) in the magma algebra over GF(2): c -> sum over a*b = c of u_a v_b mod 2."""
    n = T.shape[0]
    w = np.outer(u, v).astype(np.int64)                   # n^2 weights
    out = np.bincount(T.ravel(), weights=w.ravel(), minlength=n)
    return (out.astype(np.int64) & 1)


def rajagopalan_schulman(T: np.ndarray, rounds: int, rng: np.random.Generator):
    n = T.shape[0]
    probes = 0
    for _ in range(rounds):
        u, v, w = (rng.integers(0, 2, n) for _ in range(3))
        uv = _formal_product(T, u, v)
        left = _formal_product(T, uv, w)
        vw = _formal_product(T, v, w)
        right = _formal_product(T, u, vw)
        probes += 4 * n * n
        if not np.array_equal(left, right):
            return False, probes
    return True, probes


def random_triples(T: np.ndarray, samples: int, rng: np.random.Generator):
    n = T.shape[0]
    a, b, c = (rng.integers(0, n, samples) for _ in range(3))
    bad = T[T[a, b], c] != T[a, T[b, c]]
    if bad.any():
        k = int(np.argmax(bad)) + 1
        return False, 4 * k
    return True, 4 * samples


def generating_set(T: np.ndarray):
    """Greedy: repeatedly add the smallest element not yet generated; returns (gens, probes)."""
    n = T.shape[0]
    probes = 0
    inside = np.zeros(n, dtype=bool)
    gens = []
    while not inside.all():
        g = int(np.argmin(inside))
        gens.append(g)
        inside[g] = True
        changed = True
        while changed:
            idx = np.nonzero(inside)[0]
            prod = T[np.ix_(idx, idx)].ravel()
            probes += idx.size ** 2
            new = ~inside[prod]
            changed = bool(new.any())
            inside[prod] = True
    return gens, probes


# ------------------------------------------------------------------ benchmark families
def cyclic_group(n):
    x = np.arange(n)
    return (x[:, None] + x[None, :]) % n


def anchored_assoc(n):
    x = np.arange(n)
    return (x[:, None] + x[None, :] + 1) % n


def corrupt(T: np.ndarray, rng: np.random.Generator, protect_column0: bool = False):
    """Change one entry (outside column 0 if protect_column0) to a different value."""
    U = T.copy()
    n = U.shape[0]
    while True:
        a, b = int(rng.integers(0, n)), int(rng.integers(0, n))
        if protect_column0 and b == 0:
            continue
        U[a, b] = (U[a, b] + 1 + int(rng.integers(0, n - 1))) % n
        return U


def random_magma(n, rng):
    return rng.integers(0, n, (n, n))


def count_bad_triples(T: np.ndarray, slab: int = 64) -> int:
    n = T.shape[0]
    bad = 0
    for a0 in range(0, n, slab):
        A = np.arange(a0, min(n, a0 + slab))
        left = T[T[A, :][:, :, None], np.arange(n)[None, None, :]]
        right = T[A[:, None, None], T[None, :, :]]
        bad += int((left != right).sum())
    return bad
