"""Greedy numeration systems and 'circle' products (System C).

A base sequence G = (G_0 = 1 < G_1 < ...) gives every n >= 0 a greedy expansion
n = sum_i d_i G_i (take the largest G_k <= remaining, as many times as fits).
The circle product with shift s is

    a o b = sum_{i, j} d_i(a) d_j(b) G_{i+j+s}.

For G_i = F_{i+2} (1, 2, 3, 5, 8, ...) and s = 2 this is Knuth's Fibonacci
multiplication a o b = sum F_{k_i + l_j} over Zeckendorf indices k_i, l_j >= 2.
"""

from __future__ import annotations

from functools import lru_cache


class BaseSequence:
    """A strictly increasing integer sequence with G[0] = 1, extended on demand."""

    def __init__(self, name: str, initial, coeffs):
        """``coeffs = (a_1, ..., a_d)``: G_{k} = a_1 G_{k-1} + ... + a_d G_{k-d} for k >= len(initial)."""
        self.name = name
        self.G = list(initial)
        self.coeffs = tuple(coeffs)
        assert self.G[0] == 1 and all(x < y for x, y in zip(self.G, self.G[1:]))

    def extend(self, k: int):
        d = len(self.coeffs)
        while len(self.G) <= k:
            nxt = sum(a * self.G[-1 - i] for i, a in enumerate(self.coeffs) if len(self.G) - 1 - i >= 0)
            if nxt <= self.G[-1]:
                raise ValueError(f"{self.name}: sequence not increasing")
            self.G.append(nxt)
        return self.G

    def __getitem__(self, k):
        if k >= len(self.G):
            self.extend(k)
        return self.G[k]

    def greedy(self, n: int) -> dict:
        """Greedy digits as {index: digit} (memoised)."""
        cache = self.__dict__.setdefault("_cache", {})
        if n in cache:
            return cache[n]
        cache[n] = self._greedy(n)
        return cache[n]

    def _greedy(self, n: int) -> dict:
        while self.G[-1] <= n:
            self.extend(len(self.G))
        out = {}
        k = len(self.G) - 1
        while n and k >= 0:
            g = self.G[k]
            if g <= n:
                out[k] = n // g
                n -= out[k] * g
            k -= 1
        assert n == 0
        return out

    def circle(self, a: int, b: int, s: int) -> int:
        da, db = self.greedy(a), self.greedy(b)
        return sum(x * y * self[i + j + s] for i, x in da.items() for j, y in db.items())


def two_term(p: int, q: int, g1: int | None = None) -> BaseSequence:
    """G_{k+1} = p G_k + q G_{k-1}; default G_1 = p + 1 (Fraenkel's canonical initial value)."""
    g1 = p + 1 if g1 is None else g1
    return BaseSequence(f"G(k+1)={p}G(k)+{q}G(k-1); G0=1,G1={g1}", [1, g1], (p, q))


FIBONACCI = two_term(1, 1)           # 1, 2, 3, 5, 8, ...
