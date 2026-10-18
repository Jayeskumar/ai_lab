"""Arithmetic of Knuth's circle semigroup (N_{>=1}, o).

By the theorem of cycle C08, n -> nu(n) = n*phi + n_star embeds (N_{>=1}, o) into the
multiplicative monoid of Z[phi], where n_star = floor((n+1)/phi) is the "shadow"
sum_{k in Z(n)} F(k-1).  Hence (Knuth's product, s = 2 / t = 0):

    a o b      = a*b + a*b_star + a_star*b
    (a o b)*   = a*b + a_star*b_star

Everything here is exact integer arithmetic.
"""

from __future__ import annotations

from math import isqrt


def shadow(n: int) -> int:
    """floor((n+1)/phi) = floor(((n+1)*sqrt5 - (n+1))/2), exactly."""
    m = n + 1
    return (isqrt(5 * m * m) - m) // 2


def circ(a: int, b: int) -> int:
    return a * b + a * shadow(b) + shadow(a) * b


def products_upto(N: int) -> dict[int, list[tuple[int, int]]]:
    """All representations n = a o b with 1 <= a <= b and n <= N."""
    out: dict[int, list[tuple[int, int]]] = {}
    a = 1
    while circ(a, a) <= N:
        b = a
        while True:
            n = circ(a, b)
            if n > N:
                break
            out.setdefault(n, []).append((a, b))
            b += 1
        a += 1
    return out


def factorizations(N: int, reps: dict[int, list[tuple[int, int]]], max_count: int = 64):
    """Multisets of irreducibles whose o-product is n, for every n <= N (truncated per n)."""
    fact: dict[int, set[tuple[int, ...]]] = {}
    for n in range(1, N + 1):
        if n not in reps:
            fact[n] = {(n,)}
            continue
        fs: set[tuple[int, ...]] = set()
        for a, b in reps[n]:
            for fa in fact[a]:
                for fb in fact[b]:
                    fs.add(tuple(sorted(fa + fb)))
                    if len(fs) >= max_count:
                        break
        fact[n] = fs
    return fact
