"""Expected-length benchmarking of integer codes against distributions (cycle C11).

All codes used here have nondecreasing length functions (checked in EXP-C11-01), so the
expected length is computed exactly from the *breakpoints* of the length function and the
distribution's cdf -- no sampling error for the synthetic distributions.
"""

from __future__ import annotations

import math

import numpy as np

from systems.codes import Golomb, PatternCode


# ------------------------------------------------------------------ breakpoints
def breakpoints(code, nmax: int):
    """[(lo, hi, L)]: length(n) == L for lo <= n <= hi, covering 1..nmax (length must be nondecreasing)."""
    if isinstance(code, PatternCode):
        out, prev = [], 0
        for L, c in enumerate(code.cum):
            if c > prev:
                lo, hi = prev + 1, min(c, nmax)
                out.append((lo, hi, L))
                if c >= nmax:
                    return out
            prev = c
        raise ValueError("pattern code table too short for nmax")
    out, n = [], 1
    while n <= nmax:
        L = code.length(n)
        hi, step = n, 1
        while hi + step <= nmax and code.length(hi + step) == L:
            hi += step
            step *= 2
        top = min(hi + step, nmax)
        if code.length(top) == L:
            hi = top
        else:
            lo_, hi_ = hi, top
            while hi_ - lo_ > 1:
                mid = (lo_ + hi_) // 2
                if code.length(mid) == L:
                    lo_ = mid
                else:
                    hi_ = mid
            hi = lo_
        out.append((n, hi, L))
        n = hi + 1
    return out


# ------------------------------------------------------------------ distributions
class Dist:
    name = "dist"
    nmax = 1

    def cdf(self, n):
        raise NotImplementedError

    entropy = float("nan")


class Zipf(Dist):
    def __init__(self, s, N=10**6):
        self.name, self.nmax = f"Zipf(s={s}, N=1e6)", N
        w = np.arange(1, N + 1, dtype=np.float64) ** (-s)
        p = w / w.sum()
        self._c = np.concatenate([[0.0], np.cumsum(p)])
        self.entropy = float(-(p * np.log2(p)).sum())

    def cdf(self, n):
        return self._c[np.minimum(np.asarray(n), self.nmax)]


class LogUniform(Dist):
    def __init__(self, N=10**6):
        self.name, self.nmax = f"log-uniform 1/n on [1,{N:.0e}]", N
        w = 1.0 / np.arange(1, N + 1, dtype=np.float64)
        p = w / w.sum()
        self._c = np.concatenate([[0.0], np.cumsum(p)])
        self.entropy = float(-(p * np.log2(p)).sum())

    def cdf(self, n):
        return self._c[np.minimum(np.asarray(n), self.nmax)]


class Geometric(Dist):
    def __init__(self, p):
        self.p = p
        self.name = f"geometric(p={p})"
        self.nmax = int(math.ceil(math.log(1e-18) / math.log1p(-p))) + 1
        q = 1 - p
        self.entropy = (-p * math.log2(p) - q * math.log2(q)) / p

    def cdf(self, n):
        n = np.asarray(n, dtype=np.float64)
        return -np.expm1(n * math.log1p(-self.p))


class Uniform(Dist):
    def __init__(self, K):
        self.K = K
        self.name, self.nmax = f"uniform [1, 2^{K}]", 2 ** K
        self.entropy = float(K)

    def cdf(self, n):
        n = np.asarray(n, dtype=np.float64)
        return np.minimum(n, self.nmax) / self.nmax


class Empirical(Dist):
    def __init__(self, name, values):
        vals = np.asarray(values, dtype=np.int64)
        assert vals.min() >= 1
        self.name = name
        self.size = int(len(vals))
        self.u, cnt = np.unique(vals, return_counts=True)
        self._c = np.concatenate([[0.0], np.cumsum(cnt) / cnt.sum()])
        self.nmax = int(self.u[-1])
        p = cnt / cnt.sum()
        self.entropy = float(-(p * np.log2(p)).sum())          # zeroth-order (memoryless) entropy

    def cdf(self, n):
        idx = np.searchsorted(self.u, np.asarray(n), side="right")
        return self._c[idx]


# ------------------------------------------------------------------ expected lengths
def expected_length(code, dist) -> float:
    if isinstance(code, Golomb):
        return golomb_expected(code.M, dist)
    bps = breakpoints(code, dist.nmax)
    lo = np.array([b[0] for b in bps], dtype=np.int64)
    hi = np.array([b[1] for b in bps], dtype=np.int64)
    L = np.array([b[2] for b in bps], dtype=np.float64)
    mass = dist.cdf(hi) - dist.cdf(lo - 1)
    return float((mass * L).sum())


def golomb_expected(M: int, dist) -> float:
    b = (M - 1).bit_length()
    u = (1 << b) - M
    Q = dist.nmax // M + 1
    if Q > 5_000_000:
        return float("inf")          # quotient range too large: never competitive here
    q = np.arange(Q, dtype=np.int64)
    base = q * M                     # x = n - 1 in [qM, qM + M - 1]  <=>  n in [qM + 1, qM + M]
    if b == 0:
        mass = dist.cdf(base + 1) - dist.cdf(base)
        return float((mass * (q + 1)).sum())
    m_short = dist.cdf(base + u) - dist.cdf(base)
    m_long = dist.cdf(base + M) - dist.cdf(base + u)
    return float((m_short * (q + b) + m_long * (q + 1 + b)).sum())


def tuned_golomb(dist):
    cands = set(range(1, 65)) | {2 ** k for k in range(0, 41)}
    x = 1.0
    while x < 4 * dist.nmax:
        cands.add(int(x))
        x *= 1.08
    best = min((golomb_expected(M, dist), M) for M in sorted(cands) if M >= 1)
    rice = min((golomb_expected(2 ** k, dist), k) for k in range(0, 41))
    return {"golomb_M": best[1], "golomb_E": best[0], "rice_k": rice[1], "rice_E": rice[0]}
