"""Cost of counting: digit changes per increment in various representation systems.

Each system provides ``digits(n)`` -> tuple (least significant first, no trailing
zeros).  ``changes(a, b)`` counts positions whose digit differs.
"""

from __future__ import annotations

from math import factorial

from systems.exchange import stabilize_carry


def changes(a, b) -> int:
    n = max(len(a), len(b))
    return sum((a[i] if i < len(a) else 0) != (b[i] if i < len(b) else 0) for i in range(n))


def base_b(b):
    def digits(n):
        out = []
        while n:
            out.append(n % b)
            n //= b
        return tuple(out)
    return digits


def gray(n):
    g = n ^ (n >> 1)
    return tuple((g >> i) & 1 for i in range(g.bit_length()))


def factorial_base(n):
    out, k = [], 2
    while n:
        out.append(n % k)
        n //= k
        k += 1
    return tuple(out)


def zeckendorf(n):
    fib = [1, 2]
    while fib[-1] <= n:
        fib.append(fib[-1] + fib[-2])
    out = [0] * len(fib)
    for k in range(len(fib) - 1, -1, -1):
        if fib[k] <= n:
            out[k] = 1
            n -= fib[k]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def negabinary(n):
    out = []
    while n:
        n, r = divmod(n, -2)
        if r < 0:
            n, r = n + 1, r + 2
        out.append(r)
    return tuple(out)


def balanced_ternary(n):
    out = []
    while n:
        r = n % 3
        if r == 2:
            r = -1
        out.append(r)
        n = (n - r) // 3
    return tuple(out)


def skew_binary(n):
    """Canonical skew-binary: weights 2^(k+1)-1, digits 0/1/2, only the lowest nonzero digit may be 2."""
    ws = [1]
    while ws[-1] <= n:
        ws.append(2 * ws[-1] + 1)
    out = [0] * len(ws)
    for k in range(len(ws) - 1, -1, -1):
        while ws[k] <= n:
            out[k] += 1
            n -= ws[k]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def carry_rule(m, b):
    def digits(n):
        return tuple(stabilize_carry((n,), m, b)[0])
    return digits


SYSTEMS = {
    "binary": base_b(2),
    "ternary": base_b(3),
    "decimal": base_b(10),
    "gray": gray,
    "factorial": factorial_base,
    "zeckendorf": zeckendorf,
    "negabinary": negabinary,
    "balanced_ternary": balanced_ternary,
    "skew_binary": skew_binary,
    "base_3/2 (3[k]->2[k+1])": carry_rule(3, (2,)),
    "base_1.3028 (3[k]->[k+1]+[k+2])": carry_rule(3, (1, 1)),
}


class CarryCounter:
    """Incremental counter for a carry rule m[k] -> sum_j b_j [k+j]: add one token, stabilise locally.

    ``increment()`` returns (digit_changes, firings) for the step n -> n+1.  By the abelian
    property (C02) the resulting configuration equals rep(n+1).
    """

    def __init__(self, m, b):
        self.m, self.b = m, tuple(b)
        self.c = [0] * (len(b) + 2)

    def increment(self):
        m, b, c = self.m, self.b, self.c
        before = {0: c[0]}
        c[0] += 1
        firings = 0
        stack = [0]          # any processing order gives the same result (abelian property)
        while stack:
            k = stack.pop()
            if c[k] < m:
                continue
            t = c[k] // m
            c[k] -= t * m
            firings += t
            for j, bj in enumerate(b, start=1):
                if bj:
                    idx = k + j
                    if idx >= len(c):
                        c.extend([0] * (idx + 1 - len(c)))
                    if idx not in before:
                        before[idx] = c[idx]
                    c[idx] += t * bj
                    if c[idx] >= m:
                        stack.append(idx)
        changes = sum(1 for i, v in before.items() if c[i] != v)
        return changes, firings
