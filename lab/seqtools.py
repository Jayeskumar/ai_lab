"""Sequence tools for the Explorer: exact linear-recurrence guessing and checks.

All arithmetic is exact (fractions).  A guessed recurrence is reported only if
it is *over-determined* by the data (at least ``2*order + margin`` terms), and
even then it is computational evidence, not a proof.
"""

from __future__ import annotations

from fractions import Fraction


def berlekamp_massey(seq):
    """Minimal linear recurrence over Q: returns c with s[n] = sum c[i] s[n-1-i]."""
    s = [Fraction(x) for x in seq]
    C, B = [Fraction(1)], [Fraction(1)]
    L, m, b = 0, 1, Fraction(1)
    for n in range(len(s)):
        d = s[n] + sum(C[i] * s[n - i] for i in range(1, L + 1))
        if d == 0:
            m += 1
            continue
        T = C[:]
        coef = d / b
        C = C + [Fraction(0)] * max(0, len(B) + m - len(C))
        for i, bi in enumerate(B):
            C[i + m] -= coef * bi
        if 2 * L <= n:
            L, B, b, m = n + 1 - L, T, d, 1
        else:
            m += 1
    return [-c for c in C[1:L + 1]]


def guess_recurrence(seq, margin: int = 4):
    """Return (coefficients, verified_terms) or None if the data does not over-determine it."""
    c = berlekamp_massey(seq)
    L = len(c)
    if len(seq) < 2 * L + margin:
        return None
    for n in range(L, len(seq)):
        if sum(c[i] * seq[n - 1 - i] for i in range(L)) != seq[n]:
            return None
    return c, len(seq)


def series_coefficients(num, den, n_terms):
    """Power-series coefficients of num(x)/den(x) (lists, constant term first, den[0] != 0)."""
    out = []
    num = list(num) + [0] * n_terms
    for n in range(n_terms):
        v = Fraction(num[n])
        for i in range(1, min(n, len(den) - 1) + 1):
            v -= den[i] * out[n - i]
        out.append(v / den[0])
    return [int(x) if x.denominator == 1 else x for x in out]


def recurrence_to_str(c):
    terms = []
    for i, ci in enumerate(c, 1):
        if ci == 0:
            continue
        coef = "" if ci == 1 else ("-" if ci == -1 else f"{ci}*")
        terms.append(f"{coef}a(n-{i})")
    return "a(n) = " + " + ".join(terms).replace("+ -", "- ")
