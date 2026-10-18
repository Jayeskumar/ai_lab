"""EXP-C15-03: algebraic fast-forward (affine and commutative-semigroup magmas) against direct simulation."""

import time

import numpy as np

from systems.magma_ca import (FUSE, affine_fast_forward, commutative_semigroup_fast_forward, direct,
                              fuse_fast_forward)

META = {
    "id": "EXP-C15-03",
    "cycle": "C15",
    "title": "Fast-forwarding magma automata: polynomial powers, exponent arithmetic and burn times vs simulation",
    "agent": "Application Researcher",
    "question": "How much faster than direct simulation are the exact fast-forward algorithms for affine magmas "
                "(operator powers modulo S^L - 1), commutative semigroups (binomial exponents) and the fuse magma "
                "(burn times), and where do they not pay off?",
    "hypothesis": "H-C15-6: each fast-forward is exact, and for cyclic rows of length L = 1024 it beats direct "
                  "numpy simulation by more than 100x at t = 10^5, while losing for t below a few hundred steps.",
    "assumptions": ["cyclic rows; seeded random initial rows", "direct simulation measured up to t = 10^5 "
                    "(L <= 1024) and t = 10^4 (L = 4096); larger t only for the fast-forward algorithms",
                    "timings depend on the (shared, loaded) machine: only orders of magnitude are meaningful; they are "
                    "stored under 'timings', which the result hash ignores"],
    "methodology": "For each magma and (L, t), compute the row at time t by the fast-forward algorithm and, where "
                   "measured, by direct simulation; record agreement and wall-clock times (best of 3 for the "
                   "fast-forward, 1 run for direct).",
    "falsification": "Any disagreement with direct simulation; a speedup below 100x at L = 1024, t = 10^5.",
    "seed": 15,
}

MAGMAS = {
    "xor Z2 (a=b=1)": ("affine", (1, 1, 0, 2)),
    "x+y Z3": ("affine", (1, 1, 0, 3)),
    "x+2y+1 Z3": ("affine", (1, 2, 1, 3)),
    "2x+2y Z3": ("affine", (2, 2, 0, 3)),
    "golden law model N=5 (x+1+2y)": ("affine", (1, 2, 1, 5)),
    "mult mod 3": ("comm", np.array([[0, 0, 0], [0, 1, 2], [0, 2, 1]], dtype=np.int8)),
    "min (chain semilattice)": ("comm", np.minimum.outer(np.arange(3), np.arange(3)).astype(np.int8)),
    "GF(4) multiplication": ("comm", np.array([[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]], dtype=np.int8)),
    "fuse": ("fuse", None),
}


def table_of(kind, spec):
    if kind == "affine":
        a, b, c, n = spec
        X, Y = np.arange(n)[:, None], np.arange(n)[None, :]
        return ((a * X + b * Y + c) % n).astype(np.int8), n
    if kind == "comm":
        return spec, spec.shape[0]
    return FUSE, 3


def ff(kind, spec, T, row, t):
    if kind == "affine":
        a, b, c, n = spec
        return affine_fast_forward(a, b, c, n, row, t)
    if kind == "comm":
        return commutative_semigroup_fast_forward(T, row, t)
    return fuse_fast_forward(row, t)


def best_time(fn, reps=3):
    best, out = None, None
    for _ in range(reps):
        t0 = time.perf_counter()
        out = fn()
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    return out, best


def run():
    rng = np.random.default_rng(META["seed"])
    agree, checked, cases, timings = 0, 0, [], {}
    for name, (kind, spec) in MAGMAS.items():
        T, n = table_of(kind, spec)
        for L in (256, 1024, 4096):
            row = rng.integers(0, n, L).astype(np.int8)
            for t in (100, 1000, 10_000, 100_000, 10 ** 9):
                out_ff, t_ff = best_time(lambda: ff(kind, spec, T, row, t))
                direct_ok = (L <= 1024 and t <= 100_000) or (L == 4096 and t <= 10_000)
                rec = {"magma": name, "L": L, "t": t}
                if direct_ok:
                    t0 = time.perf_counter()
                    out_d = direct(T, row, t)
                    t_d = time.perf_counter() - t0
                    ok = bool(np.array_equal(np.asarray(out_ff) % n, out_d))
                    agree += ok
                    checked += 1
                    rec["agrees_with_direct"] = ok
                    timings[f"{name}|L={L}|t={t}"] = {"ff_s": round(t_ff, 6), "direct_s": round(t_d, 5),
                                                      "speedup": round(t_d / t_ff, 1)}
                else:
                    timings[f"{name}|L={L}|t={t}"] = {"ff_s": round(t_ff, 6)}
                cases.append(rec)
    return {
        "cases": cases,
        "checked_against_direct": checked,
        "agreements": agree,
        "timings": timings,
        "summary": [f"{agree}/{checked} fast-forward results agree with direct simulation "
                    f"({len(MAGMAS)} magmas, L in {{256, 1024, 4096}}, t up to 10^5; t = 10^9 by fast-forward only)"],
    }
