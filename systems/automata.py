"""Finite automata for factor-avoiding languages and exact counting.

``avoid_dfa`` builds the Aho-Corasick automaton of a finite set of forbidden
factors; its live states recognise exactly the words that avoid every pattern.
The number of accepted words of length n satisfies a linear recurrence of
order <= (number of live states) by Cayley-Hamilton, which is what makes the
finite-prefix comparisons in the proofs rigorous.
"""

from __future__ import annotations

from collections import deque


def avoid_dfa(patterns, alphabet: str):
    """Return (delta, start, n_states) for words avoiding all ``patterns``.

    ``delta[state][letter]`` is the next live state, or None if the letter
    completes an occurrence of a forbidden pattern.
    """
    goto = [{}]
    out = [False]
    for p in patterns:
        s = 0
        for ch in p:
            if ch not in goto[s]:
                goto.append({})
                out.append(False)
                goto[s][ch] = len(goto) - 1
            s = goto[s][ch]
        out[s] = True
    fail = [0] * len(goto)
    q = deque()
    for ch, s in goto[0].items():
        q.append(s)
    while q:
        r = q.popleft()
        for ch, s in goto[r].items():
            q.append(s)
            f = fail[r]
            while f and ch not in goto[f]:
                f = fail[f]
            fail[s] = goto[f][ch] if ch in goto[f] and goto[f][ch] != s else 0
            out[s] = out[s] or out[fail[s]]
    n = len(goto)

    def step(s, ch):
        while s and ch not in goto[s]:
            s = fail[s]
        return goto[s].get(ch, 0)

    live = [i for i in range(n) if not out[i]]
    index = {s: i for i, s in enumerate(live)}
    delta = []
    for s in live:
        row = {}
        for ch in alphabet:
            t = step(s, ch)
            row[ch] = None if out[t] else index[t]
        delta.append(row)
    return delta, index[0], len(live)


def count_accepted(delta, start: int, n_max: int) -> list[int]:
    """Number of accepted words of each length 0..n_max (every live state accepts)."""
    vec = [0] * len(delta)
    vec[start] = 1
    counts = [1]
    for _ in range(n_max):
        nxt = [0] * len(delta)
        for s, c in enumerate(vec):
            if c:
                for t in delta[s].values():
                    if t is not None:
                        nxt[t] += c
        vec = nxt
        counts.append(sum(vec))
    return counts
