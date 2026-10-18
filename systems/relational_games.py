"""System D: impartial one-heap games whose moves are defined by relations between numbers.

A game is given by its *option relation*: from a heap of size n a move goes to a
smaller position (one heap m < n, or -- for take-and-break games -- a pair of
heaps whose sizes sum to n).  The Sprague-Grundy value is

    g(n) = mex { g(m) : m an option of n }            (one-heap options)
    g(n) = mex { g(a) XOR g(b) : (a, b) an option }  (splitting options)

where mex A is the least natural number not in A.  Because every option is
smaller, the recursion is well founded and g is the unique solution of these
equations.  All computations here are exact.
"""

from __future__ import annotations

from math import gcd, isqrt

import numpy as np


# ------------------------------------------------------------------ basics
def mex(values) -> int:
    s = set(values)
    v = 0
    while v in s:
        v += 1
    return v


def divisor_lists(N: int) -> list[list[int]]:
    """divs[n] = sorted divisors of n (n <= N); divs[0] = []."""
    divs: list[list[int]] = [[] for _ in range(N + 1)]
    for d in range(1, N + 1):
        for m in range(d, N + 1, d):
            divs[m].append(d)
    return divs


def smallest_prime_factor(N: int) -> list[int]:
    spf = list(range(N + 1))
    for p in range(2, isqrt(N) + 1):
        if spf[p] == p:
            for m in range(p * p, N + 1, p):
                if spf[m] == m:
                    spf[m] = p
    return spf


def primes_upto(N: int) -> list[int]:
    spf = smallest_prime_factor(N)
    return [p for p in range(2, N + 1) if spf[p] == p]


# ------------------------------------------------------------------ solvers
def grundy_options(N: int, options) -> list[int]:
    """g(0..N) for a one-heap game; ``options(n, g)`` yields option positions m < n."""
    g = [0] * (N + 1)
    for n in range(N + 1):
        g[n] = mex(g[m] for m in options(n))
    return g


def grundy_subtraction(N: int, S) -> list[int]:
    """Subtraction game with move set S (positive integers): options n - s, s in S, s <= n.

    Bitset method: C[v] has bit n set iff some option of n has Grundy value v; when g(i) = v
    is fixed, every n = i + s acquires an option of value v.  Cost O(N^2 / wordsize).
    """
    S = sorted({s for s in S if 1 <= s <= N})
    mask = (1 << (N + 1)) - 1
    SB = 0
    for s in S:
        SB |= 1 << s
    C: list[int] = []
    g = [0] * (N + 1)
    for n in range(N + 1):
        v = 0
        while v < len(C) and (C[v] >> n) & 1:
            v += 1
        g[n] = v
        if v == len(C):
            C.append(0)
        C[v] |= (SB << n) & mask
    return g


def grundy_split(N: int, allowed) -> list[int]:
    """Take-and-break game: split a heap n into two nonempty heaps a + b = n (a <= b) with
    ``allowed(a, b)`` (vectorised over arrays a, b); option value g(a) XOR g(b)."""
    g = np.zeros(N + 1, dtype=np.int64)
    for n in range(2, N + 1):
        a = np.arange(1, n // 2 + 1)
        b = n - a
        ok = allowed(a, b)
        vals = np.bitwise_xor(g[a[ok]], g[b[ok]])
        if vals.size == 0:
            g[n] = 0
            continue
        present = np.zeros(vals.max() + 2, dtype=bool)
        present[vals] = True
        g[n] = int(np.argmin(present))
    return [int(x) for x in g]


# ------------------------------------------------------------------ structure detection
def eventual_period(seq, max_period: int = 2000, min_reps: int = 3):
    """Smallest period p (with its least preperiod) such that seq[n + p] = seq[n] for every
    n >= pre inside the data and the periodic tail covers at least ``min_reps`` periods.
    Returns (pre, p) or None."""
    a = np.asarray(seq)
    L = len(a)
    for p in range(1, min(max_period, L // min_reps) + 1):
        diff = np.nonzero(a[p:] != a[:-p])[0]
        pre = 0 if diff.size == 0 else int(diff[-1]) + 1
        if L - pre >= min_reps * p and L - pre >= p + 1:
            return pre, p
    return None


def arithmetic_period(seq, max_period: int = 2000, min_reps: int = 3):
    """Smallest p with seq[n + p] = seq[n] + s (s != 0 constant) for n >= pre; returns (pre, p, s) or None."""
    a = np.asarray(seq, dtype=np.int64)
    L = len(a)
    for p in range(1, min(max_period, L // min_reps) + 1):
        d = a[p:] - a[:-p]
        s = d[-1]
        if s == 0:
            continue
        bad = np.nonzero(d != s)[0]
        pre = 0 if bad.size == 0 else int(bad[-1]) + 1
        if L - pre >= min_reps * p and L - pre >= p + 1:
            return pre, p, int(s)
    return None


# ------------------------------------------------------------------ number-theoretic closed forms
def v2(n: int) -> int:
    return (n & -n).bit_length() - 1 if n else 0


def big_omega_table(N: int) -> list[int]:
    spf = smallest_prime_factor(N)
    om = [0] * (N + 1)
    for n in range(2, N + 1):
        om[n] = om[n // spf[n]] + 1
    return om


def prime_index_of_spf_table(N: int) -> list[int]:
    """0 for n = 1 (and 0), otherwise the index j of the smallest prime factor p_j (p_1 = 2)."""
    spf = smallest_prime_factor(N)
    idx = {}
    k = 0
    for p in range(2, N + 1):
        if spf[p] == p:
            k += 1
            idx[p] = k
    return [0, 0] + [idx[spf[n]] for n in range(2, N + 1)]
