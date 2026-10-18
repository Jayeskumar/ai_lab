"""EXP-C13-09: independent cross-checks of the C13 theorems (Skeptic)."""

import itertools
import time
from math import gcd

import numpy as np

from systems.anchored import affine_roots, affine_spectrum, affine_system, factorize
from systems.magma import MagmaSAT, fill, parse, shapes, to_str

META = {
    "id": "EXP-C13-09",
    "cycle": "C13",
    "title": "Skeptic cross-checks: cube-law models, six-leaf W-family, arithmetic identifications to N = 1000",
    "agent": "Mathematical Skeptic",
    "question": "Do the explicit models of Theorem 5 really satisfy the law for N = 3..60? Does Theorem 3 hold for the "
                "42 six-leaf terms W? Are the affine spectra of CLM-C13-11 equal to the stated arithmetic sets beyond "
                "the OEIS window (N <= 1000), checked against their direct definitions?",
    "hypothesis": "All three checks pass with 0 discrepancies.",
    "assumptions": ["(a) direct numpy evaluation, no SAT; N = 2 exhaustively over all 4 free entries",
                    "(b) SAT enumeration (limit 100) for N = 1..6",
                    "(c) direct definitions: existence of t with t^2 = -1, 2, 3 or t^4 = -1 (mod N); prime-factor "
                    "conditions; compared with the affine spectrum of the example law"],
    "methodology": "Independent code paths from those of EXP-C13-01..08 wherever possible.",
    "falsification": "Any discrepancy.",
}


def cube_op(N):
    T = np.zeros((N, N), dtype=np.int64)
    for x in range(N):
        for y in range(N):
            if y == 0:
                T[x, y] = (x + 1) % N
            elif x == 0:
                T[x, y] = 2 % N if y == 1 else 0
            else:
                T[x, y] = x if y == x else 0
    return T


def check_cube(N):
    T = cube_op(N)
    x = np.arange(N)
    return bool(np.all(T[x, T[x, T[x, x]]] == x)) and bool(np.all(T[:, 0] == (x + 1) % N))


def n2_has_model():
    for e in itertools.product(range(2), repeat=2):  # entries 0*1, 1*1
        T = np.array([[1, e[0]], [0, e[1]]])
        x = np.arange(2)
        if np.all(T[x, T[x, T[x, x]]] == x):
            return True
    return False


def is_square_mod(c, N):
    return any((t * t - c) % N == 0 for t in range(N))


def prime_factors_all(N, pred):
    return all(pred(p) for p in factorize(N)) if N > 1 else True


DEFS = {
    "x(xx) = y(xy)": lambda N: is_square_mod(-1, N),                        # A008784
    "(xx)(xy) = (yy)(yx)": lambda N: is_square_mod(2, N),                   # A057126
    "x = x((xx)x)": lambda N: N % 2 == 1,                                    # odd numbers
    "((xx)x)x = ((yy)y)y": lambda N: N % 3 != 0,                             # A001651
    "x(xy) = y(yx)": lambda N: any((a * a - a - 1) % N == 0 for a in range(N)),  # golden, A089270
    "x((xy)y) = y((xx)x)": lambda N: prime_factors_all(N, lambda p: p % 8 in (1, 7)),  # A058529
}


def run():
    t0 = time.perf_counter()
    cube = {"N2_model_exists": n2_has_model(), "bad_N_3_60": [N for N in range(3, 61) if not check_cube(N)]}
    # (b) six-leaf W
    W6 = [fill(sh, ["z"] * 6) for sh in shapes(5)]
    mism = []
    for W in W6:
        law = ((("x", "y"), "z"), ("x", ("y", W)))
        sysm = affine_system(law)
        for N in range(1, 7):
            tables, complete = MagmaSAT(N, [law], extra=lambda S, n=N: [[S.v[x, 0, (x + 1) % n]] for x in range(n)]
                                        ).enumerate(limit=100)
            roots = affine_roots(sysm, N)
            aff = [(T == (np.arange(N).reshape(-1, 1) + a * np.arange(N).reshape(1, -1) + 1) % N).all()
                   for T, a in zip(tables, [int((T[0, 1] - 1) % N) if N > 1 else 0 for T in tables])]
            if not complete or len(tables) != len(roots) or not all(aff):
                mism.append({"W": to_str(W), "N": N, "models": len(tables), "roots": len(roots)})
    # (c) identifications
    ident = {}
    for L, pred in DEFS.items():
        a, b = L.split(" = ")
        spec = set(affine_spectrum(affine_system((parse(a), parse(b))), 1000))
        direct = {N for N in range(1, 1001) if pred(N)}
        ident[L] = {"agree": spec == direct, "only_affine": sorted(spec - direct)[:5],
                    "only_direct": sorted(direct - spec)[:5]}
    ok = (not cube["N2_model_exists"]) and not cube["bad_N_3_60"] and not mism and all(v["agree"]
                                                                                    for v in ident.values())
    return {"cube": cube, "w6_terms": len(W6), "w6_mismatches": mism, "identifications": ident, "all_ok": ok,
            "timings": {"total_s": round(time.perf_counter() - t0, 1)},
            "summary": [f"cube law: model at N=2: {cube['N2_model_exists']}; failing explicit models N=3..60: "
                        f"{cube['bad_N_3_60']}",
                        f"W-family, {len(W6)} six-leaf terms, N <= 6: mismatches {len(mism)}",
                        "identifications to N=1000: " + ", ".join(f"{k}: {v['agree']}" for k, v in ident.items()),
                        f"all checks passed: {ok}"]}
