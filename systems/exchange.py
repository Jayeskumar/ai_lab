"""Exchange systems: tokens on levels 0, 1, 2, ... rewritten by local exchange rules.

By cycle C01, a multiset of tokens is a word modulo commutation, i.e. a vector
of counts.  A configuration is a tuple ``c`` with ``c[k]`` tokens at level k.

* A **carry rule** ``(m, b)`` with ``b = (b_1, ..., b_J)`` fires at a level k
  holding at least m tokens: it removes m tokens there and adds ``b_j`` tokens
  at level ``k + j``.  Tokens only move upward.
* A **general exchange system** is a list of rule schemas ``(k_min, k_max, A, B)``
  where ``A`` and ``B`` map offsets to counts; at a level k with
  ``k_min <= k <= k_max`` (``k_max = None`` means unbounded) the configuration
  loses ``A[o]`` tokens at ``k + o`` and gains ``B[o]``.
"""

from __future__ import annotations

from collections import deque


def trim(c) -> tuple:
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


# ------------------------------------------------------------ carry rules
def stabilize_carry(config, m: int, b, max_level: int = 5000, max_firings: int = 10**9):
    """Fire until no level holds >= m tokens.

    Uses one upward sweep with batch firing (valid because tokens only move up and
    the system is abelian).  Returns (stable_config, firing_vector, terminated).
    """
    c = list(config) + [0] * (len(b) + 1)
    fires = [0] * len(c)
    total = 0
    k = 0
    while k < len(c):
        if c[k] >= m:
            t = c[k] // m
            c[k] -= t * m
            fires[k] += t
            total += t
            need = k + len(b) + 1
            if need > len(c):
                c += [0] * (need - len(c))
                fires += [0] * (need - len(fires))
            for j, bj in enumerate(b, start=1):
                c[k + j] += t * bj
            if total > max_firings:
                return trim(c), trim(fires), False
        k += 1
        if k > max_level and any(c[k:]):
            return trim(c), trim(fires), False
    return trim(c), trim(fires), True


def positive_root(m: int, b, digits: int = 40):
    """The unique r > 0 with sum_j b_j r^j = m (high-precision bisection)."""
    import mpmath as mp
    mp.mp.dps = digits
    f = lambda r: sum(bj * r ** j for j, bj in enumerate(b, start=1)) - m
    lo, hi = mp.mpf(0), mp.mpf(1)
    while f(hi) < 0:
        hi *= 2
    for _ in range(digits * 4):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def digits_msd_first(config) -> str:
    """Digit string, most significant (highest level) first; '0' for the empty configuration."""
    c = trim(config)
    if not c:
        return "0"
    return "".join(str(x) if x < 10 else f"[{x}]" for x in reversed(c))


# ------------------------------------------------------------ general systems
def apply_rules(c: tuple, rules):
    """All one-step successors of configuration c."""
    out = []
    n = len(c)
    for k_min, k_max, A, B in rules:
        hi = n - min(A) if A else n
        if k_max is not None:
            hi = min(hi, k_max)
        for k in range(k_min, max(hi, k_min - 1) + 1):
            ok = True
            for o, a in A.items():
                idx = k + o
                if idx < 0 or idx >= n or c[idx] < a:
                    ok = False
                    break
            if not ok:
                continue
            for o in B:
                if k + o < 0:
                    ok = False
            if not ok:
                continue
            top = max([n - 1] + [k + o for o in B])
            d = list(c) + [0] * (top + 1 - n)
            for o, a in A.items():
                d[k + o] -= a
            for o, x in B.items():
                d[k + o] += x
            out.append(trim(d))
    return out


def explore(initial, rules, max_states: int = 200_000):
    """Exhaustive derivation graph from ``initial``.

    Returns dict with the number of reachable configurations, the normal forms
    (sinks), whether a cycle exists, and min/max derivation lengths to a sink.
    ``None`` entries mean the state limit was hit.
    """
    start = trim(initial)
    succ = {}
    q = deque([start])
    seen = {start}
    while q:
        c = q.popleft()
        s = sorted(set(apply_rules(c, rules)))
        succ[c] = s
        for x in s:
            if x not in seen:
                seen.add(x)
                if len(seen) > max_states:
                    return {"states": None, "limit_hit": True}
                q.append(x)
    # topological order (detect cycles)
    indeg = {c: 0 for c in succ}
    for c, s in succ.items():
        for x in s:
            indeg[x] += 1
    order, dq = [], deque(c for c, d in indeg.items() if d == 0)
    while dq:
        c = dq.popleft()
        order.append(c)
        for x in succ[c]:
            indeg[x] -= 1
            if indeg[x] == 0:
                dq.append(x)
    has_cycle = len(order) != len(succ)
    sinks = [c for c, s in succ.items() if not s]
    res = {"states": len(succ), "limit_hit": False, "has_cycle": has_cycle, "sinks": sinks}
    if not has_cycle:
        lo, hi = {}, {}
        for c in reversed(order):
            if not succ[c]:
                lo[c] = hi[c] = 0
            else:
                lo[c] = 1 + min(lo[x] for x in succ[c])
                hi[c] = 1 + max(hi[x] for x in succ[c])
        res["min_len"], res["max_len"] = lo[start], hi[start]
    return res


def value(c, weights) -> int:
    return sum(x * w for x, w in zip(c, weights))


# The Fibonacci (Zeckendorf) exchange system: weights w_k = F(k+2) = 1, 2, 3, 5, 8, ...
FIBONACCI_RULES = [
    (0, None, {0: 1, 1: 1}, {2: 1}),      # [k] + [k+1] -> [k+2]
    (2, None, {0: 2}, {1: 1, -2: 1}),     # 2[k] -> [k+1] + [k-2]   (k >= 2)
    (1, 1, {0: 2}, {1: 1, -1: 1}),        # 2[1] -> [2] + [0]
    (0, 0, {0: 2}, {1: 1}),               # 2[0] -> [1]
]


def fib_weights(n: int) -> list[int]:
    w = [1, 2]
    while len(w) < n:
        w.append(w[-1] + w[-2])
    return w[:n]


def zeckendorf_config(n: int) -> tuple:
    """Greedy Zeckendorf representation as a 0/1 configuration over weights 1, 2, 3, 5, ..."""
    w = fib_weights(60)
    c = [0] * 60
    for k in range(59, -1, -1):
        if w[k] <= n:
            c[k] = 1
            n -= w[k]
    return trim(c)
