"""The Zeckendorf game (cycle C19): longest games, exactly and greedily.

Board: chips on levels k = 0, 1, 2, ... worth F_{k+1} in the indexing F_1 = 1, F_2 = 2, F_3 = 3, F_4 = 5, ...
(level k of the lab's Fibonacci exchange system, ``systems.exchange.FIBONACCI_RULES``).  Moves:

* C1   : 2[0]        -> [1]              (combine 1s; 1 + 1 = 2)
* C_i  : [i-2] + [i-1] -> [i]  for i >= 2 (combine consecutive; level i-2 and i-1, i.e. F_{i-1} + F_i = F_{i+1})
* S2   : 2[1]        -> [2] + [0]        (2 + 2 = 3 + 1)
* S_i  : 2[i-1]      -> [i] + [i-3]  for i >= 3  (2 F_i = F_{i+1} + F_{i-2})

Moves are named by the paper's 1-based index i of the Fibonacci number they act on (Cusenza et al.):
C_i combines F_{i-1} and F_i (levels i-2, i-1); S_i splits two copies of F_i (level i-1).

The game starts from n chips on level 0 and ends at the Zeckendorf representation.  ``longest_exact`` computes
the longest game by dynamic programming over all reachable configurations (no strategy assumed);
``greedy_game`` plays the strategy of Cusenza et al. (Fib. Quart. 60 (2022), Thm 1.2): a split or combine-1s
move whenever possible (we take the smallest index), otherwise the combine move with the smallest index.
"""

from __future__ import annotations

import sys
from functools import lru_cache

FIB = [1, 2]
while len(FIB) < 95:
    FIB.append(FIB[-1] + FIB[-2])          # FIB[k] = F_{k+1}: 1, 2, 3, 5, 8, ...


def zeckendorf_digits(n: int) -> list[int]:
    """0/1 digits d[k] (level k worth FIB[k]) of the greedy Zeckendorf representation of n."""
    if n == 0:
        return []
    k = max(i for i in range(len(FIB)) if FIB[i] <= n)
    d = [0] * (k + 1)
    for i in range(k, -1, -1):
        if FIB[i] <= n:
            d[i] = 1
            n -= FIB[i]
    return d


def Z(n: int) -> int:
    """Number of Zeckendorf summands."""
    return sum(zeckendorf_digits(n))


def IZ(n: int) -> int:
    """Sum of the 1-based indices of the Zeckendorf summands (F_1 = 1, F_2 = 2, ...)."""
    return sum(k + 1 for k, x in enumerate(zeckendorf_digits(n)) if x)


def cusenza_bound(n: int) -> int:
    """sum_i a_i delta_i with a_i = F_{i+2} - i - 2 (Cusenza et al., Thm 1.3); exact iff n = F_k - 1 (Thm 1.4)."""
    return sum(FIB[k + 2] - (k + 1) - 2 for k, x in enumerate(zeckendorf_digits(n)) if x)


def _trim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def moves(c: tuple):
    """All (name, successor) pairs of configuration c (a tuple of chip counts by level)."""
    out = []
    n = len(c)
    get = lambda k: c[k] if k < n else 0
    for k in range(n):
        x = c[k]
        if x >= 2:
            d = list(c) + [0, 0]
            d[k] -= 2
            if k == 0:
                d[1] += 1
                out.append(("C1", _trim(d)))
            elif k == 1:
                d[2] += 1
                d[0] += 1
                out.append(("S2", _trim(d)))
            else:
                d[k + 1] += 1
                d[k - 2] += 1
                out.append((f"S{k + 1}", _trim(d)))
        if x >= 1 and get(k + 1) >= 1:
            d = list(c) + [0, 0]
            d[k] -= 1
            d[k + 1] -= 1
            d[k + 2] += 1
            out.append((f"C{k + 2}", _trim(d)))
    return out


def longest_exact(n: int, return_states: bool = False):
    """Length of the longest game from n chips on level 0, by memoised DFS over the (acyclic) move graph."""
    start = (n,) if n else ()
    memo = {}
    stack = [start]
    while stack:
        c = stack[-1]
        if c in memo:
            stack.pop()
            continue
        succ = [d for _, d in moves(c)]
        pending = [d for d in succ if d not in memo]
        if pending:
            stack.extend(pending)
            continue
        memo[c] = 1 + max(memo[d] for d in succ) if succ else 0
        stack.pop()
    return (memo[start], len(memo)) if return_states else memo[start]


def greedy_game(n: int, record: bool = False):
    """Play the split-first greedy strategy; return (length, move counts) and optionally the move list."""
    c = [n] + [0] * 4
    counts = {}
    seq = [] if record else None
    length = 0
    while True:
        # extend board
        if c[-1] or c[-2]:
            c.extend([0, 0])
        move = None
        # splits / combine 1s, smallest index first
        for k, x in enumerate(c):
            if x >= 2:
                move = ("S", k)
                break
        if move is None:
            for k in range(len(c) - 1):
                if c[k] and c[k + 1]:
                    move = ("C", k)
                    break
        if move is None:
            break
        t, k = move
        if t == "S":
            c[k] -= 2
            if k == 0:
                c[1] += 1
                name = "C1"
            elif k == 1:
                c[2] += 1
                c[0] += 1
                name = "S2"
            else:
                c[k + 1] += 1
                c[k - 2] += 1
                name = f"S{k + 1}"
        else:
            c[k] -= 1
            c[k + 1] -= 1
            c[k + 2] += 1
            name = f"C{k + 2}"
        counts[name] = counts.get(name, 0) + 1
        length += 1
        if record:
            seq.append(name)
    final = _trim(c)
    return {"length": length, "counts": counts, "final": final, "moves": seq}


def greedy_length_fast(n: int) -> int:
    """Same game as greedy_game, with a moving pointer to the lowest level that can change (faster)."""
    c = [0] * 100
    c[0] = n
    length = 0
    lo = 0
    while True:
        k = lo
        # find smallest split / combine-1 at or above lo; a move at level k only affects levels >= k - 2
        move_k = -1
        top = len(c) - 3
        j = k
        while j < top:
            if c[j] >= 2:
                move_k = j
                break
            j += 1
        if move_k >= 0:
            j = move_k
            c[j] -= 2
            if j == 0:
                c[1] += 1
            elif j == 1:
                c[2] += 1
                c[0] += 1
            else:
                c[j + 1] += 1
                c[j - 2] += 1
            length += 1
            lo = max(0, j - 2)
            continue
        # no split anywhere at or above lo; levels below lo hold at most one chip (invariant), so look for combines
        j = 0
        found = -1
        while j < top:
            if c[j] and c[j + 1]:
                found = j
                break
            j += 1
        if found < 0:
            return length
        c[found] -= 1
        c[found + 1] -= 1
        c[found + 2] += 1
        length += 1
        lo = found


# ------------------------------------------------------------------ structure of the longest game (C19)
def combine_weight(counts: dict) -> int:
    """W = sum_{i >= 2} (i - 1) MC_i over the consecutive-combine moves of a game (C1 excluded)."""
    return sum((int(k[1:]) - 1) * v for k, v in counts.items() if k.startswith("C") and k != "C1")


def random_game(n: int, rng) -> dict:
    """A uniformly random sequence of legal moves from n chips on level 0 (for checking identities)."""
    c = (n,) if n else ()
    counts, length = {}, 0
    while True:
        mv = moves(c)
        if not mv:
            return {"length": length, "counts": counts, "final": c}
        name, c = mv[rng.randrange(len(mv))]
        counts[name] = counts.get(name, 0) + 1
        length += 1


def split_phase(n: int, order=None, rng=None):
    """Apply split and combine-1 moves (only) until every level holds at most one chip.

    order=None fires the lowest possible level; order='random' fires a random possible level (rng required).
    Returns (stable configuration, number of moves)."""
    c = [n] + [0] * 64
    steps = 0
    while True:
        cand = [k for k, x in enumerate(c) if x >= 2]
        if not cand:
            return _trim(c), steps
        k = cand[0] if order is None else cand[rng.randrange(len(cand))]
        c[k] -= 2
        if k == 0:
            c[1] += 1
        elif k == 1:
            c[2] += 1
            c[0] += 1
        else:
            c[k + 1] += 1
            c[k - 2] += 1
        steps += 1


def lazy_digits(n: int) -> list[int]:
    """Top-down 'lazy' algorithm: take level l only if the lower levels together cannot hold the remainder.

    The result is checked separately to have no two consecutive zeros (which characterises the lazy
    representation, Brown 1965)."""
    if n == 0:
        return []
    t = 0
    while FIB[t + 2] - 2 < n:          # FIB[0] + ... + FIB[t] = FIB[t + 2] - 2
        t += 1
    d = [0] * (t + 1)
    r = n
    for l in range(t, -1, -1):
        lower = FIB[l + 1] - 2         # FIB[0] + ... + FIB[l - 1]
        if r > lower:
            d[l] = 1
            r -= FIB[l]
    assert r == 0
    return d


def _top(n: int) -> int:
    k = 0
    while FIB[k + 1] <= n:
        k += 1
    return k


def _h(k: int) -> int:
    return k * k // 4


_RHO_CACHE: dict = {}


def rho(p: int, m: int) -> int:
    """Auxiliary 'saving' sequences of the conjectured recursion (CLM-C19-06); p in {0, 1}."""
    key = (p, m)
    if key in _RHO_CACHE:
        return _RHO_CACHE[key]
    if m == 0:
        val = 0
    else:
        i = _top(m)
        t = m - FIB[i]
        if i == 0:
            base = 1
        elif i % 2 == p:
            base = _h(i) + 2
        else:
            base = _h(i + 1) + 1
        val = base + max(0, rho(p, t) - _h(i - 2)) if i % 2 == p else base
    _RHO_CACHE[key] = val
    return val


def deficit_rec(n: int) -> int:
    """Conjectured closed recursion for D(n) = B(n) - L(n):  D(0) = 0,
    D(F_j + m) = floor(j^2/4) + D(m) - rho_{j mod 2}(m)  for 0 <= m < F_{j-1} (levels j: F = 1, 2, 3, 5, ...)."""
    total = 0
    while n:
        j = _top(n)
        m = n - FIB[j]
        total += _h(j) - rho(j % 2, m)
        n = m
    return total


def longest_rec(n: int) -> int:
    """L(n) via the conjectured recursion (O(log^2 n) arithmetic operations)."""
    return cusenza_bound(n) - deficit_rec(n)


def fib_partitions(N: int) -> list[int]:
    """Number of partitions of n into parts 1, 2, 3, 5, 8, ... (multiplicities allowed), n < N."""
    p = [1] + [0] * (N - 1)
    for f in FIB:
        if f >= N:
            break
        for v in range(f, N):
            p[v] += p[v - f]
    return p


def split_phase_fast(n: int):
    """Lowest-first split phase with a moving pointer (same result as split_phase(n))."""
    c = [0] * 100
    c[0] = n
    steps = 0
    k = 0
    top = len(c) - 3
    while k < top:
        if c[k] >= 2:
            c[k] -= 2
            if k == 0:
                c[1] += 1
            elif k == 1:
                c[2] += 1
                c[0] += 1
            else:
                c[k + 1] += 1
                c[k - 2] += 1
            steps += 1
            k = max(0, k - 2)
        else:
            k += 1
    return _trim(c), steps
