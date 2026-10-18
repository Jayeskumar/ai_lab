"""Termination analysis for one-rule string rewriting systems 0^p 1^q -> 1^r 0^s (cycle C03).

Three kinds of evidence are produced:

* **loop certificates** -- a derivation u ->+ x u y (self-embedding).  Since
  rewriting is closed under context, such a derivation extends to an infinite
  one; each certificate is re-checked step by step by :func:`check_loop`.
* **matrix-interpretation certificates** (Hofbauer-Waldmann 2006) -- d x d
  matrices over N, one per letter, with M[0][0] >= 1 and M[d-1][d-1] >= 1,
  such that [lhs] >= [rhs] entrywise and [lhs][0][d-1] > [rhs][0][d-1].  The
  top-right entry of the product then strictly decreases along every
  derivation, which proves termination; re-checked by :func:`check_matrix`.
* **bounded evidence** -- finite, acyclic reachable sets from all small words.
"""

from __future__ import annotations

import itertools
from collections import deque

import numpy as np

from systems.rewriting import derivation_extremes, occurrences


def rule(p, q, r, s):
    return "0" * p + "1" * q, "1" * r + "0" * s


# ------------------------------------------------------------------ loops
def check_loop(lhs: str, rhs: str, cert: dict) -> bool:
    """Verify a loop certificate {'start': u, 'steps': [pos, ...]}: u ->+ v with u a factor of v."""
    w = cert["start"]
    if not cert["steps"]:
        return False
    for pos in cert["steps"]:
        if w[pos:pos + len(lhs)] != lhs:
            return False
        w = w[:pos] + rhs + w[pos + len(lhs):]
    return cert["start"] in w and w == cert["end"]


def find_loop_forward_closures(lhs: str, rhs: str, max_len: int = 40, max_pairs: int = 60_000):
    """Breadth-first search over forward closures (u, v), u ->+ v, with right AND left extensions.

    A pair (u, v) where u is a factor of v is a loop.  Returns a certificate or None.
    Each queue item carries the derivation as a list of redex positions in the
    final start word coordinates.
    """
    k = len(lhs)
    start = (lhs, rhs, (0,))
    seen = {(lhs, rhs)}
    q = deque([start])
    pairs = 0
    while q:
        u, v, steps = q.popleft()
        pairs += 1
        if pairs > max_pairs:
            return None
        if u in v and len(steps) >= 1:
            cert = {"start": u, "steps": list(steps), "end": v}
            if check_loop(lhs, rhs, cert):
                return cert
        succ = []
        # (2) rewrite a redex inside v
        for i in occurrences(v, lhs):
            succ.append((u, v[:i] + rhs + v[i + k:], steps + (i,)))
        # (3) right extension: a proper suffix of v is a proper prefix of lhs
        for j in range(1, k):
            if v.endswith(lhs[:j]):
                ext = lhs[j:]
                pos = len(v) - j
                nv = v + ext
                succ.append((u + ext, nv[:pos] + rhs + nv[pos + k:], steps + (pos,)))
        # (4) left extension: a proper prefix of v is a proper suffix of lhs
        for j in range(1, k):
            if v.startswith(lhs[k - j:]):
                ext = lhs[:k - j]
                shift = len(ext)
                nv = ext + v
                new_steps = tuple(x + shift for x in steps) + (0,)
                succ.append((ext + u, rhs + nv[k:], new_steps))
        for (nu, nv, ns) in succ:
            if len(nv) > max_len or len(nu) > max_len:
                continue
            key = (nu, nv)
            if key not in seen:
                seen.add(key)
                q.append((nu, nv, ns))
    return None


# ------------------------------------------------- matrix interpretations
def check_matrix(lhs: str, rhs: str, mats: dict) -> bool:
    """Exact check of a matrix-interpretation certificate (Python integers)."""
    d = len(next(iter(mats.values())))
    for M in mats.values():
        if M[0][0] < 1 or M[d - 1][d - 1] < 1 or any(x < 0 for row in M for x in row):
            return False

    def prod(word):
        P = [[int(i == j) for j in range(d)] for i in range(d)]
        for c in word:
            M = mats[c]
            P = [[sum(P[i][t] * M[t][j] for t in range(d)) for j in range(d)] for i in range(d)]
        return P

    L, R = prod(lhs), prod(rhs)
    return all(L[i][j] >= R[i][j] for i in range(d) for j in range(d)) and L[0][d - 1] > R[0][d - 1]


def _batched_power(A, n):
    out = np.broadcast_to(np.eye(A.shape[-1], dtype=np.int64), A.shape).copy()
    for _ in range(n):
        out = out @ A
    return out


def find_matrix_interpretation(p, q, r, s, d: int, entries, upper_triangular: bool = True):
    """Exhaustive search for a d x d matrix interpretation with entries from ``entries``.

    Returns {'0': M0, '1': M1} (lists) or None.  Vectorised over all candidate
    pairs; the winner is re-checked exactly with :func:`check_matrix`.
    """
    pos = [(i, j) for i in range(d) for j in range(d) if (j >= i or not upper_triangular)]
    cands = []
    for vals in itertools.product(entries, repeat=len(pos)):
        M = np.zeros((d, d), dtype=np.int64)
        for (i, j), v in zip(pos, vals):
            M[i, j] = v
        if M[0, 0] >= 1 and M[d - 1, d - 1] >= 1:
            cands.append(M)
    C = np.array(cands)                       # (n, d, d)
    n = len(C)
    P0, Q0 = _batched_power(C, p), _batched_power(C, s)   # M0^p, M0^s
    P1, Q1 = _batched_power(C, q), _batched_power(C, r)   # M1^q, M1^r
    lhs_l, rhs_r = "0" * p + "1" * q, "1" * r + "0" * s
    for a in range(n):                          # choice of M0
        L = P0[a][None, :, :] @ P1             # (n, d, d): M0^p M1^q for every M1
        R = Q1 @ Q0[a][None, :, :]             # M1^r M0^s
        ok = np.all(L >= R, axis=(1, 2)) & (L[:, 0, d - 1] > R[:, 0, d - 1])
        if ok.any():
            b = int(np.argmax(ok))
            mats = {"0": C[a].tolist(), "1": C[b].tolist()}
            if check_matrix(lhs_l, rhs_r, mats):
                return mats
    return None


# ------------------------------------------------------- bounded evidence
def bounded_evidence(lhs: str, rhs: str, max_word: int, limit: int = 50_000, max_len_factor: int = 8):
    """For all binary words of length <= max_word containing lhs: finite acyclic reachable sets?

    Reachable words longer than ``max_len_factor * max_word`` are reported as "too_long" (inconclusive).
    """
    rules = [(lhs, rhs)]
    stats = {"words": 0, "finite": 0, "cycle": 0, "too_long_or_limit": 0, "max_derivation": {}}
    memo = {}
    for n in range(len(lhs), max_word + 1):
        best = 0
        for t in itertools.product("01", repeat=n):
            w = "".join(t)
            if lhs not in w:
                continue
            stats["words"] += 1
            res = derivation_extremes(w, rules, limit=limit, max_len=max_len_factor * max_word, memo=memo)
            if res is None or (isinstance(res, tuple) and res and res[0] == "too_long"):
                stats["too_long_or_limit"] += 1
            elif res[0] == "cycle":
                stats["cycle"] += 1
            else:
                stats["finite"] += 1
                best = max(best, res[1])
        stats["max_derivation"][n] = best
    return stats


def find_loop_strategies(lhs: str, rhs: str, max_steps: int = 3000, max_len: int = 6000,
                         max_a: int | None = None, max_b: int | None = None):
    """Self-embedding search along deterministic strategies (leftmost / rightmost redex).

    Start words are 0^a 1^b for a <= max_a, b <= max_b (default 3p and 4q*q).  Returns a
    loop certificate (checked by :func:`check_loop`) or None.
    """
    p = lhs.count("0")
    q = lhs.count("1")
    max_a = max_a or 3 * p
    max_b = max_b or max(4 * q * q, 3 * q)
    for a in range(p, max_a + 1):
        for b in range(q, max_b + 1):
            u = "0" * a + "1" * b
            for strategy in ("rightmost", "leftmost"):
                w, steps = u, []
                for _ in range(max_steps):
                    i = w.rfind(lhs) if strategy == "rightmost" else w.find(lhs)
                    if i < 0:
                        break
                    w = w[:i] + rhs + w[i + len(lhs):]
                    steps.append(i)
                    if u in w:
                        cert = {"start": u, "steps": steps, "end": w, "strategy": strategy}
                        if check_loop(lhs, rhs, cert):
                            return cert
                    if len(w) > max_len:
                        break
    return None


def replay(lhs: str, rhs: str, start: str, steps) -> list[str]:
    words = [start]
    for pos in steps:
        w = words[-1]
        assert w[pos:pos + len(lhs)] == lhs
        words.append(w[:pos] + rhs + w[pos + len(lhs):])
    return words


def lift_zeros(cert: dict, p: int, q: int, r: int, k: int) -> dict:
    """Lift a loop of (1, q, r, k) along the morphism 0 -> 0^p to a loop of (p, q, r, k p)."""
    l1, r1 = rule(1, q, r, k)
    psi = lambda w: w.replace("0", "0" * p)
    words = replay(l1, r1, cert["start"], cert["steps"])
    steps = [len(psi(w[:i])) for w, i in zip(words, cert["steps"])]
    return {"start": psi(cert["start"]), "steps": steps, "end": psi(words[-1])}


def mirror(cert: dict, p: int, q: int, r: int, s: int) -> dict:
    """Transport a loop of (p, q, r, s) along w -> complement(reverse(w)) to a loop of (q, p, s, r)."""
    l, rr = rule(p, q, r, s)
    phi = lambda w: w[::-1].translate(str.maketrans("01", "10"))
    words = replay(l, rr, cert["start"], cert["steps"])
    steps = [len(w) - i - len(l) for w, i in zip(words, cert["steps"])]
    return {"start": phi(cert["start"]), "steps": steps, "end": phi(words[-1])}
