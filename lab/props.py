"""Property profiler for binary operations (Phase 3 of the research plan).

Two entry points:

* :func:`profile_table` -- exhaustive checks for a finite Cayley table
  ``T`` (``T[a, b] = a*b`` on ``{0..n-1}``); results are *proofs by
  exhaustion* for that finite structure.
* :func:`profile_function` -- checks for an operation on an infinite domain,
  evaluated on a finite sample.  A failure gives a genuine counterexample;
  success is only *computational support* on the sampled window.

Each property is reported as ``{"holds": bool, "counterexample": ...}``.
"""

from __future__ import annotations

import itertools

import numpy as np


def _cex(mask, *arrays):
    idx = np.argwhere(~mask)
    if len(idx) == 0:
        return None
    return tuple(int(i) for i in idx[0])


def associative(T):
    n = T.shape[0]
    ar = np.arange(n)
    left = T[T[:, :, None], ar[None, None, :]]      # (a*b)*c
    right = T[ar[:, None, None], T[None, :, :]]     # a*(b*c)
    ok = left == right
    return {"holds": bool(ok.all()), "counterexample": _cex(ok)}


def commutative(T):
    ok = T == T.T
    return {"holds": bool(ok.all()), "counterexample": _cex(ok)}


def idempotent(T):
    ok = np.diagonal(T) == np.arange(T.shape[0])
    return {"holds": bool(ok.all()), "counterexample": _cex(ok)}


def identity(T):
    n = T.shape[0]
    ar = np.arange(n)
    for e in range(n):
        if (T[e, :] == ar).all() and (T[:, e] == ar).all():
            return {"holds": True, "element": e}
    left = [e for e in range(n) if (T[e, :] == ar).all()]
    right = [e for e in range(n) if (T[:, e] == ar).all()]
    return {"holds": False, "left_identities": left, "right_identities": right}


def inverses(T, e):
    if e is None:
        return {"holds": False, "reason": "no identity"}
    n = T.shape[0]
    missing = [a for a in range(n) if not any(T[a, b] == e and T[b, a] == e for b in range(n))]
    return {"holds": not missing, "elements_without_inverse": missing[:10]}


def latin(T):
    """Quasigroup test: every row and column is a permutation."""
    n = T.shape[0]
    rows = all(len(set(T[a, :].tolist())) == n for a in range(n))
    cols = all(len(set(T[:, b].tolist())) == n for b in range(n))
    return {"holds": rows and cols, "rows_bijective": rows, "cols_bijective": cols}


def distributes_over(T, S):
    """Left and right distributivity of * (T) over + (S)."""
    n = T.shape[0]
    ar = np.arange(n)
    a, b, c = ar[:, None, None], ar[None, :, None], ar[None, None, :]
    left = T[a, S[b, c]] == S[T[a, b], T[a, c]]
    right = T[S[a, b], c] == S[T[a, c], T[b, c]]
    return {"left": {"holds": bool(left.all()), "counterexample": _cex(left)},
            "right": {"holds": bool(right.all()), "counterexample": _cex(right)}}


def left_self_distributive(T):
    n = T.shape[0]
    ar = np.arange(n)
    a, b, c = ar[:, None, None], ar[None, :, None], ar[None, None, :]
    ok = T[a, T[b, c]] == T[T[a, b], T[a, c]]
    return {"holds": bool(ok.all()), "counterexample": _cex(ok)}


def profile_table(T) -> dict:
    T = np.asarray(T, dtype=np.int64)
    n = T.shape[0]
    assert T.shape == (n, n) and T.min() >= 0 and T.max() < n, "table must be closed on {0..n-1}"
    idn = identity(T)
    return {
        "size": n,
        "closure": {"holds": True},
        "associative": associative(T),
        "commutative": commutative(T),
        "idempotent": idempotent(T),
        "identity": idn,
        "inverses": inverses(T, idn.get("element")),
        "latin_square (quasigroup)": latin(T),
        "left_self_distributive": left_self_distributive(T),
    }


def profile_function(op, sample, closure_set=None, identity_candidates=(), max_report=5) -> dict:
    """Evaluate properties of ``op`` on all pairs/triples from ``sample``."""
    sample = list(sample)
    res = {"sample_size": len(sample)}
    tab = {(a, b): op(a, b) for a in sample for b in sample}
    if closure_set is not None:
        bad = [(a, b, v) for (a, b), v in tab.items() if v not in closure_set]
        res["closure"] = {"holds": not bad, "counterexample": bad[:max_report]}
    bad = [(a, b) for a in sample for b in sample if tab[(a, b)] != tab[(b, a)]]
    res["commutative"] = {"holds": not bad, "counterexample": bad[:max_report]}
    bad = []
    for a, b, c in itertools.product(sample, repeat=3):
        if op(tab[(a, b)], c) != op(a, tab[(b, c)]):
            bad.append((a, b, c))
            if len(bad) >= max_report:
                break
    res["associative"] = {"holds": not bad, "counterexample": bad}
    bad = [a for a in sample if tab[(a, a)] != a]
    res["idempotent"] = {"holds": not bad, "counterexample": bad[:max_report]}
    ids = [e for e in identity_candidates if all(op(e, a) == a and op(a, e) == a for a in sample)]
    res["identity"] = {"holds": bool(ids), "elements": ids}
    return res
