"""Cycle C04: derivations of one-rule string rewriting systems and rewriting games.

A one-rule system is a pair ``(l, r)`` of words over {a, b}.  The tools here

* certify termination (length decrease, lexicographic monotonicity for
  length-preserving rules, or a strictly decreasing linear interpretation
  ``a -> c_a x + d_a`` over the naturals) or non-termination (a verified
  self-embedding derivation ``w ->+ x w y``);
* build the full derivation graph from a set of start words and compute, for
  every word, the minimum/maximum number of steps to a normal form and the
  Sprague-Grundy value of the *rewriting game* (a move = one rewrite step,
  the player unable to move loses);
* compute Grundy values of octal games independently (for comparison).
"""

from __future__ import annotations

import itertools
from collections import deque

from systems.rewriting import one_step, words


# ------------------------------------------------------------------ rules
def all_rules(alphabet: str = "ab", max_l: int = 3, max_r: int = 3):
    """All rules l -> r with 1 <= |l| <= max_l, 0 <= |r| <= max_r, l != r."""
    lhs = [w for L in range(1, max_l + 1) for w in words(alphabet, L)]
    rhs = [""] + [w for L in range(1, max_r + 1) for w in words(alphabet, L)]
    return [(l, r) for l in lhs for r in rhs if l != r]


def borders(w: str) -> list[str]:
    return [w[:i] for i in range(1, len(w)) if w[:i] == w[-i:]]


def critical_peaks(rule):
    """Critical peaks of a single rule: for each border b of l (l = p b = b s), the
    overlap word p b s and its two one-step reducts (r s, p r)."""
    l, r = rule
    out = []
    for b in borders(l):
        p, s = l[: len(l) - len(b)], l[len(b):]
        out.append({"border": b, "peak": p + b + s, "left": r + s, "right": p + r})
    return out


# ------------------------------------------------------- termination certificates
def _compose(word, interp):
    """Coefficients (c, d) of the composite map [w](x) = [w_1]([w_2](...[w_n](x)))."""
    c, d = 1, 0
    for ch in reversed(word):
        ca, da = interp[ch]
        c, d = ca * c, ca * d + da
    return c, d


def linear_interpretation(rule, alphabet="ab", max_coef=4, max_const=4):
    """Search a strictly monotone linear interpretation over N proving termination.

    Letters are interpreted as x -> c x + d with c >= 1, d >= 0; a word as the
    composition of its letters.  If [l](x) > [r](x) for all x >= 0, i.e.
    c_l >= c_r and d_l > d_r, every rewrite step strictly decreases [w](0),
    so the system terminates.  Both reading directions are tried (the second
    corresponds to the mirrored rule).  Returns a certificate dict or None.
    """
    l, r = rule
    for direction in ("right-to-left", "left-to-right"):
        L, R = (l, r) if direction == "right-to-left" else (l[::-1], r[::-1])
        for coefs in itertools.product(range(1, max_coef + 1), repeat=len(alphabet)):
            for consts in itertools.product(range(0, max_const + 1), repeat=len(alphabet)):
                interp = {ch: (coefs[i], consts[i]) for i, ch in enumerate(alphabet)}
                cl, dl = _compose(L, interp)
                cr, dr = _compose(R, interp)
                if cl >= cr and dl > dr:
                    return {"direction": direction, "interpretation": {k: list(v) for k, v in interp.items()},
                            "lhs": [cl, dl], "rhs": [cr, dr]}
    return None


def occurrences_count(word: str, f: str) -> int:
    return sum(1 for i in range(len(word) - len(f) + 1) if word[i:i + len(f)] == f)


def factor_count_certificate(rule, alphabet="ab", max_f=3):
    """Find a factor f whose number of occurrences drops by >= 1 at every rewrite step.

    Only occurrences overlapping the rewritten window can change, and they are
    determined by at most |f| - 1 letters of context on each side; checking all
    such contexts (including shorter ones, for word ends) is therefore a proof.
    """
    l, r = rule
    for L in range(1, max_f + 1):
        for f in words(alphabet, L):
            ctx = [w for k in range(0, L) for w in words(alphabet, k)]
            drops = []
            for x in ctx:
                for y in ctx:
                    drops.append(occurrences_count(x + l + y, f) - occurrences_count(x + r + y, f))
            if min(drops) >= 1:
                return {"factor": f, "min_drop": min(drops), "max_drop": max(drops)}
    return None


def weighted_factor_certificate(rule, alphabet="ab", max_f=4):
    """Nonnegative integer weights w_f on factors (|f| <= max_f) such that sum_f w_f * occ(f, .)
    drops by >= 1 at every rewrite step in every context.  Found with a linear program,
    then rounded and re-verified in exact integer arithmetic (the returned certificate is
    only the exactly verified one)."""
    import numpy as np
    from scipy.optimize import linprog
    l, r = rule
    fs = [w for L in range(1, max_f + 1) for w in words(alphabet, L)]
    ctx = [w for k in range(0, max_f) for w in words(alphabet, k)]
    rows = []
    for x in ctx:
        for y in ctx:
            rows.append([occurrences_count(x + l + y, f) - occurrences_count(x + r + y, f) for f in fs])
    res = linprog(np.zeros(len(fs)), A_ub=-np.array(rows), b_ub=-np.ones(len(rows)),
                  bounds=[(0, None)] * len(fs), method="highs")
    if res.status != 0:
        return None
    for scale in range(1, 13):
        w = [int(round(v * scale)) for v in res.x]
        if all(sum(wi * d for wi, d in zip(w, row)) >= 1 for row in rows):
            return {"weights": {f: wi for f, wi in zip(fs, w) if wi}, "contexts_checked": len(rows)}
    return None


def self_embedding(rule, seeds, max_depth=14, max_len=40, max_states=20000):
    """Find a derivation w ->+ x w y (certificate of non-termination). Returns the path or None."""
    for start in seeds:
        parent = {start: None}
        q = deque([(start, 0)])
        while q:
            u, d = q.popleft()
            if d >= max_depth:
                continue
            for v in sorted(set(one_step(u, [rule]))):
                if start in v:
                    path = [v, u]
                    while parent[path[-1]] is not None:
                        path.append(parent[path[-1]])
                    return list(reversed(path))
                if v in parent or len(v) > max_len or len(parent) >= max_states:
                    continue
                parent[v] = u
                q.append((v, d + 1))
    return None


def check_self_embedding(rule, path) -> bool:
    """Independent check of a non-termination certificate."""
    if len(path) < 2:
        return False
    for u, v in zip(path, path[1:]):
        if v not in one_step(u, [rule]):
            return False
    return path[0] in path[-1]


def classify_termination(rule, seed_len=6):
    l, r = rule
    if len(r) < len(l):
        return {"status": "TERMINATING", "proof": "length decreases"}
    if len(r) == len(l):
        return {"status": "TERMINATING", "proof": "length-preserving, lexicographically monotone"}
    if l in r:
        path = [l, r]
        return {"status": "NON-TERMINATING", "proof": "self-embedding", "certificate": path,
                "certificate_ok": check_self_embedding(rule, path)}
    cert = linear_interpretation(rule)
    if cert is not None:
        return {"status": "TERMINATING", "proof": "linear interpretation", "certificate": cert}
    cert = factor_count_certificate(rule)
    if cert is not None:
        return {"status": "TERMINATING", "proof": "factor count decreases", "certificate": cert}
    seeds = [w for L in range(1, seed_len + 1) for w in words("ab", L)]
    path = self_embedding(rule, seeds)
    if path is not None:
        return {"status": "NON-TERMINATING", "proof": "self-embedding", "certificate": path,
                "certificate_ok": check_self_embedding(rule, path)}
    return {"status": "UNKNOWN"}


# ------------------------------------------------------------ derivation graphs
class GraphLimit(Exception):
    pass


def derivation_graph(starts, rule, limit=400_000):
    """Successor lists of every word reachable from ``starts``."""
    succ = {}
    seen = set(starts)
    q = deque(starts)
    while q:
        w = q.popleft()
        s = sorted(set(one_step(w, [rule])))
        succ[w] = s
        for x in s:
            if x not in seen:
                seen.add(x)
                if len(seen) > limit:
                    raise GraphLimit(len(seen))
                q.append(x)
    return succ


def graph_values(succ):
    """For an acyclic derivation graph: per word (min steps, max steps, Grundy value).

    Raises ValueError if the graph has a cycle.
    """
    pred = {w: [] for w in succ}
    remaining = {}
    for w, s in succ.items():
        remaining[w] = len(s)
        for x in s:
            pred[x].append(w)
    ready = deque(w for w, k in remaining.items() if k == 0)
    val = {}
    while ready:
        w = ready.popleft()
        s = succ[w]
        if not s:
            val[w] = (0, 0, 0)
        else:
            mins = [val[x][0] for x in s]
            maxs = [val[x][1] for x in s]
            gs = {val[x][2] for x in s}
            g = 0
            while g in gs:
                g += 1
            val[w] = (1 + min(mins), 1 + max(maxs), g)
        for p in pred[w]:
            remaining[p] -= 1
            if remaining[p] == 0:
                ready.append(p)
    if len(val) != len(succ):
        raise ValueError("derivation graph has a cycle")
    return val


def steps_reachable(word, rule, k):
    """Set of words reachable in exactly k steps."""
    level = {word}
    for _ in range(k):
        level = {x for u in level for x in one_step(u, [rule])}
    return level


def equal_length_joinable(x, y, rule, max_k=30):
    """Smallest k with a common word reachable from x and from y in exactly k steps, else None."""
    lx, ly = {x}, {y}
    for k in range(max_k + 1):
        if lx & ly:
            return k
        lx = {v for u in lx for v in one_step(u, [rule])}
        ly = {v for u in ly for v in one_step(u, [rule])}
        if not lx or not ly:
            return None
    return None


# ------------------------------------------------------------------ octal games
def octal_grundy(code: str, n_max: int) -> list[int]:
    """Grundy values G(0..n_max) of the octal game with the given code (e.g. '0.07', '0.6').

    Digit d_k (k >= 1 after the point) is a sum of 1 (a whole heap of exactly k may
    be removed), 2 (removing k may leave one nonempty heap), 4 (removing k may leave
    two nonempty heaps).
    """
    ds = [int(ch) for ch in code.split(".")[1]]
    G = [0] * (n_max + 1)
    for n in range(1, n_max + 1):
        opts = set()
        for k, d in enumerate(ds, start=1):
            if d & 1 and n == k:
                opts.add(0)
            if d & 2 and n > k:
                opts.add(G[n - k])
            if d & 4 and n - k >= 2:
                for a in range(1, (n - k) // 2 + 1):
                    opts.add(G[a] ^ G[n - k - a])
        g = 0
        while g in opts:
            g += 1
        G[n] = g
    return G


def subtraction_grundy(subtract: int, minimum: int, n_max: int) -> list[int]:
    """Heap n -> n - subtract, allowed when n >= minimum."""
    G = [0] * (n_max + 1)
    for n in range(n_max + 1):
        opts = {G[n - subtract]} if n >= minimum and n - subtract >= 0 else set()
        g = 0
        while g in opts:
            g += 1
        G[n] = g
    return G


def runs_of(word: str, letter: str = "a") -> list[int]:
    return [len(x) for x in word.split("b" if letter == "a" else "a") if x]
