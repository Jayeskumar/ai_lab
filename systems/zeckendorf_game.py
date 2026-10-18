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
