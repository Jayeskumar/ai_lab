"""Mex-defined binary operations on the natural numbers (cycle C07).

A *mex operation* is defined by recursion on (a, b):

    f(a, b) = mex V(a, b),

where V(a, b) collects values computed from earlier entries.  The family studied here is
parametrised by a *spec* (L, R, D):

* ``L`` (bool): include the values f(a', b) for every a' < a ("move in the first argument");
* ``R`` (bool): include the values f(a, b') for every b' < b;
* ``D`` (tuple of masks in 1..7): for every pair a' < a, b' < b and every mask m in D include
  XOR of the selected values among x = f(a', b) (bit 1), y = f(a, b') (bit 2), z = f(a', b') (bit 4).

Conway's nim-sum is (L=True, R=True, D=()) and Conway's nim-product is (False, False, (7,)).
mex(S) is the least natural number not in S (mex of the empty set is 0).
"""

from __future__ import annotations

import itertools

import numpy as np

NIM_SUM = (True, True, ())
NIM_PRODUCT = (False, False, (7,))


def spec_name(spec) -> str:
    L, R, D = spec
    names = {1: "x", 2: "y", 3: "x^y", 4: "z", 5: "x^z", 6: "y^z", 7: "x^y^z"}
    parts = (["L"] if L else []) + (["R"] if R else []) + [f"D[{names[m]}]" for m in D]
    return "+".join(parts) if parts else "empty"


def all_specs():
    """All 2 * 2 * 2^7 = 512 specs (D ranges over subsets of the 7 masks)."""
    out = []
    for L in (False, True):
        for R in (False, True):
            for r in range(8):
                for D in itertools.combinations(range(1, 8), r):
                    out.append((L, R, D))
    return out


def table(spec, n: int, m: int | None = None) -> np.ndarray:
    """The n x m table (default n x n) of the mex operation, f[a, b] for a < n, b < m (vectorised per cell).

    Entries only depend on entries with smaller or equal coordinates, so a rectangular table is exact."""
    L, R, D = spec
    m = n if m is None else m
    f = np.zeros((n, m), dtype=np.int64)
    for a in range(n):
        for b in range(m):
            vals = []
            if L and a:
                vals.append(f[:a, b])
            if R and b:
                vals.append(f[a, :b])
            if D and a and b:
                x = np.broadcast_to(f[:a, b][:, None], (a, b))
                y = np.broadcast_to(f[a, :b][None, :], (a, b))
                z = f[:a, :b]
                for mask in D:
                    v = np.zeros((a, b), dtype=np.int64)
                    if mask & 1:
                        v = v ^ x
                    if mask & 2:
                        v = v ^ y
                    if mask & 4:
                        v = v ^ z
                    vals.append(v.ravel())
            if not vals:
                f[a, b] = 0
                continue
            allv = np.concatenate([np.ravel(v) for v in vals])
            size = allv.size + 1
            seen = np.zeros(size + 1, dtype=bool)
            seen[allv[allv <= size]] = True
            f[a, b] = int(np.argmin(seen))
    return f


def table_slow(spec, n: int) -> list[list[int]]:
    """Reference implementation with plain Python sets (for cross-checks)."""
    L, R, D = spec
    f = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            S = set()
            if L:
                S.update(f[i][b] for i in range(a))
            if R:
                S.update(f[a][j] for j in range(b))
            for i in range(a):
                for j in range(b):
                    x, y, z = f[i][b], f[a][j], f[i][j]
                    for m in D:
                        v = 0
                        if m & 1:
                            v ^= x
                        if m & 2:
                            v ^= y
                        if m & 4:
                            v ^= z
                        S.add(v)
            g = 0
            while g in S:
                g += 1
            f[a][b] = g
    return f


# ------------------------------------------------------------------ properties on a finite window
def closed_below(T: np.ndarray, k: int) -> bool:
    """Is {0, ..., k-1} closed under the operation (all values of T[:k, :k] < k)?"""
    return bool((T[:k, :k] < k).all())


def is_commutative(T) -> bool:
    return bool(np.array_equal(T, T.T))


def associativity_violations(T: np.ndarray, k: int) -> tuple[int, int]:
    """Count triples (a, b, c) in [0, k)^3 with (ab)c != a(bc), using the full table T (n x n, k <= n).

    Triples whose intermediate value a*b or b*c is >= n cannot be evaluated and are skipped.
    Returns (violations, evaluated_triples).
    """
    n = T.shape[0]
    A = T[:k, :k]
    a = np.arange(k)[:, None, None]
    b = np.arange(k)[None, :, None]
    c = np.arange(k)[None, None, :]
    ab = np.broadcast_to(A[:, :, None], (k, k, k))
    bc = np.broadcast_to(A[None, :, :], (k, k, k))
    ok = (ab < n) & (bc < n)
    left = T[np.where(ok, ab, 0), np.broadcast_to(c, (k, k, k))]
    right = T[np.broadcast_to(a, (k, k, k)), np.where(ok, bc, 0)]
    return int(((left != right) & ok).sum()), int(ok.sum())


def identity_elements(T: np.ndarray, k: int) -> list[int]:
    A = T[:k, :k]
    r = np.arange(k)
    return [e for e in range(k) if np.array_equal(A[e, :], r) and np.array_equal(A[:, e], r)]


def distributes_over_xor(T: np.ndarray, k: int) -> bool:
    """a*(b XOR c) = (a*b) XOR (a*c) on [0, k)^3 (requires b XOR c < k, true for k a power of 2)."""
    A = T[:k, :k]
    a = np.arange(k)[:, None, None]
    b = np.arange(k)[None, :, None]
    c = np.arange(k)[None, None, :]
    return bool((A[a, b ^ c] == (A[a, b] ^ A[a, c])).all())


def is_latin(T: np.ndarray, k: int) -> bool:
    A = T[:k, :k]
    return all(len(set(A[i, :])) == k for i in range(k)) and all(len(set(A[:, j])) == k for j in range(k))


def additive_period(row, min_tail: int = 200):
    """Smallest (p, s, b0) with row[b + p] = row[b] + s for all b0 <= b < len(row) - p, requiring the checked
    tail to have length >= max(min_tail, 3p); None if no such p <= len(row) // 4 exists."""
    r = np.asarray(row, dtype=np.int64)
    n = len(r)
    for p in range(1, n // 4 + 1):
        d = r[p:] - r[:-p]
        s = d[-1]
        bad = np.nonzero(d != s)[0]
        b0 = int(bad[-1]) + 1 if bad.size else 0
        if n - p - b0 >= max(min_tail, 3 * p):
            return p, int(s), b0
    return None
