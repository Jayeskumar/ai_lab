"""Laver tables and successor-anchored magmas (System B).

Convention: elements {0, ..., N-1}; the *anchor* column is 0 and x * 0 = x + 1 (mod N).
(Laver's convention {1..N} with p * 1 = p + 1 is the relabelling p -> p - 1.)
"""

from __future__ import annotations

import numpy as np


def laver_table(n: int) -> np.ndarray:
    """A_n on {0..2^n - 1} (0-based), computed by Laver's recursion; returns T[a, b] = a * b."""
    N = 2 ** n
    # work in Laver's 1-based convention, then relabel
    L = np.zeros((N + 1, N + 1), dtype=np.int64)
    for q in range(1, N + 1):
        L[N, q] = q
    for p in range(N - 1, 0, -1):
        L[p, 1] = p + 1
        for q in range(1, N):
            r = L[p, q]
            if r <= p:
                raise ValueError("Laver recursion failed (p * q <= p)")
            L[p, q + 1] = L[r, p + 1]
    return (L[1:, 1:] - 1).astype(np.int64)


def recursion_table(N: int):
    """Run Laver's recursion for an arbitrary N; return the table or None if it breaks down."""
    L = np.zeros((N + 1, N + 1), dtype=np.int64)
    for q in range(1, N + 1):
        L[N, q] = q
    for p in range(N - 1, 0, -1):
        L[p, 1] = p + 1
        for q in range(1, N):
            r = L[p, q]
            if r <= p:
                return None
            L[p, q + 1] = L[r, p + 1]
    return (L[1:, 1:] - 1).astype(np.int64)


def is_left_distributive(T: np.ndarray) -> bool:
    n = T.shape[0]
    ar = np.arange(n)
    for a in range(n):           # row by row keeps memory O(n^2)
        lhs = T[a][T]                        # a * (b * c)  as matrix over (b, c)
        rhs = T[np.ix_(T[a], T[a])]          # (a*b) * (a*c)
        if not np.array_equal(lhs, rhs):
            return False
    return True


def row_period(T: np.ndarray, a: int) -> int:
    """Least p > 0 with a * (b + p) = a * b for all b (Laver rows are periodic)."""
    N = T.shape[0]
    row = T[a]
    # in 0-based relabelling, Laver's column q is index q-1; periods are the same
    for p in range(1, N + 1):
        if N % p == 0 and all(row[b] == row[(b + p) % N] for b in range(N)):
            return p
    return N
