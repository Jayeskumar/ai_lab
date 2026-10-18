"""Catalogue of the relational one-heap games of cycle C12 (shared by the C12 experiments)."""

from math import gcd

import numpy as np

from systems.relational_games import (divisor_lists, grundy_options, grundy_split, grundy_subtraction, mex,
                                      primes_upto)

N_FAST = 100_000      # games with cheap option sets
N_QUAD = 5_000        # games whose option sets have size ~n
N_DIV = 20_000        # floor-division game


def _fib_upto(N):
    f = [1, 2]
    while f[-1] <= N:
        f.append(f[-1] + f[-2])
    return f


def _coprime_vec(N, want_coprime):
    g = np.zeros(N + 1, dtype=np.int64)
    for n in range(2, N + 1):
        m = np.arange(1, n)
        sel = (np.gcd(m, n) == 1) if want_coprime else (np.gcd(m, n) > 1)
        vals = g[m[sel]]
        if vals.size == 0:
            continue
        present = np.zeros(int(vals.max()) + 2, dtype=bool)
        present[vals] = True
        g[n] = int(np.argmin(present))
    return [int(x) for x in g]


def _mod_game(N):
    g = np.zeros(N + 1, dtype=np.int64)
    for n in range(2, N + 1):
        vals = g[n % np.arange(1, n)]
        present = np.zeros(int(vals.max()) + 2, dtype=bool)
        present[vals] = True
        g[n] = int(np.argmin(present))
    return [int(x) for x in g]


def _floor_div_game(N):
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        opts = set()
        k = 2
        while k <= n:
            q = n // k
            opts.add(g[q])
            k = n // q + 1 if q else n + 1
        g[n] = mex(opts)
    return g


def catalogue():
    """name -> (description, relation type, solver thunk returning g[0..N])."""
    C = {}
    C["G01 subtract a divisor d<n"] = ("n -> n-d, d | n, d < n", "divisibility", lambda: _div_game(N_FAST, "lt"))
    C["G02 subtract any divisor"] = ("n -> n-d, d | n (d = n allowed: n -> 0)", "divisibility",
                                      lambda: _div_game(N_FAST, "le"))
    C["G03 subtract a nontrivial proper divisor"] = ("n -> n-d, d | n, 1 < d < n", "divisibility",
                                                      lambda: _div_game(N_FAST, "nontrivial"))
    C["G04 move to a proper divisor"] = ("n -> m, m | n, m < n (positions n >= 1)", "divisibility",
                                          lambda: _div_game(N_FAST, "to_divisor"))
    C["G05 move to a smaller coprime"] = ("n -> m, 1 <= m < n, gcd(m, n) = 1", "coprimality",
                                           lambda: _coprime_vec(N_QUAD, True))
    C["G06 move to a smaller non-coprime"] = ("n -> m, 1 <= m < n, gcd(m, n) > 1", "coprimality",
                                               lambda: _coprime_vec(N_QUAD, False))
    C["G08 subtract a square"] = ("n -> n-k^2, k >= 1", "additive set", lambda: grundy_subtraction(
        N_FAST, [k * k for k in range(1, 400)]))
    C["G09 subtract a Fibonacci number"] = ("n -> n-F, F in {1,2,3,5,8,...}", "additive set",
                                             lambda: grundy_subtraction(N_FAST, _fib_upto(N_FAST)))
    C["G10 subtract a power of 2"] = ("n -> n-2^i", "additive set",
                                       lambda: grundy_subtraction(N_FAST, [2 ** i for i in range(18)]))
    C["G10b subtract a power of 3"] = ("n -> n-3^i", "additive set",
                                        lambda: grundy_subtraction(N_FAST, [3 ** i for i in range(12)]))
    C["G10c subtract a power of 4"] = ("n -> n-4^i", "additive set",
                                        lambda: grundy_subtraction(N_FAST, [4 ** i for i in range(10)]))
    C["G11 subtract a prime"] = ("n -> n-p, p prime", "additive set",
                                  lambda: grundy_subtraction(N_FAST, primes_upto(N_FAST)))
    C["G12 subtract a triangular number"] = ("n -> n-k(k+1)/2, k >= 1", "additive set",
                                              lambda: grundy_subtraction(N_FAST, [k * (k + 1) // 2 for k in
                                                                                  range(1, 450)]))
    C["G13 move to a proper binary submask"] = ("n -> m, m AND n = m, m != n", "bitwise",
                                                 lambda: grundy_options(N_FAST, lambda n: _submasks(n)))
    C["G16 split into coprime parts"] = ("n -> (a, b), a + b = n, gcd(a, b) = 1", "splitting",
                                          lambda: grundy_split(N_QUAD, lambda a, b: np.gcd(a, b) == 1))
    C["G17 split into dividing parts"] = ("n -> (a, b), a + b = n, a | b", "splitting",
                                           lambda: grundy_split(N_QUAD, lambda a, b: b % a == 0))
    C["G18 Grundy's game (unequal split)"] = ("n -> (a, b), a + b = n, a != b", "splitting",
                                               lambda: grundy_split(N_QUAD, lambda a, b: a != b))
    C["G19 move to a remainder"] = ("n -> n mod k, 1 <= k < n", "divisibility",
                                     lambda: _mod_game(N_QUAD))
    C["G20 move to a quotient"] = ("n -> floor(n/k), 2 <= k <= n", "divisibility",
                                    lambda: _floor_div_game(N_DIV))
    return C


_DIVS = {}


def _divs(N):
    if N not in _DIVS:
        _DIVS[N] = divisor_lists(N)
    return _DIVS[N]


def _div_game(N, kind):
    divs = _divs(N)
    if kind == "lt":
        return grundy_options(N, lambda n: [n - d for d in divs[n] if d < n])
    if kind == "le":
        return grundy_options(N, lambda n: [n - d for d in divs[n]])
    if kind == "nontrivial":
        return grundy_options(N, lambda n: [n - d for d in divs[n] if 1 < d < n])
    if kind == "to_divisor":
        return grundy_options(N, lambda n: [d for d in divs[n] if d < n])
    raise ValueError(kind)


def _submasks(n):
    out = []
    m = (n - 1) & n
    while True:
        out.append(m)
        if m == 0:
            break
        m = (m - 1) & n
    return out if n else []
