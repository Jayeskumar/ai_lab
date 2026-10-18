"""EXP-C06-04: are anchored spectra explained by affine models x*y = x + a*y + 1 (mod N)?"""

import itertools
import time

import numpy as np

from systems.magma import MagmaSAT, fill, n_leaves, parse, satisfies, shapes, to_str

META = {
    "id": "EXP-C06-04",
    "cycle": "C06",
    "title": "Affine anchored models and the arithmetic of anchored spectra",
    "agent": "Mathematical Explorer",
    "question": "For the 382 laws of EXP-C06-03, does the anchored spectrum coincide with the set of N for which "
                "some affine table x*y = x + a*y + 1 (mod N) satisfies the law? Are all anchored models of the "
                "restricted-spectrum laws affine?",
    "hypothesis": "H-C06-3 (bold): apart from left-distributivity, every law of the family has anchored spectrum "
                  "equal to its affine spectrum for N <= 6. H-C06-4 (derived by hand): the anchored models of "
                  "(xy)z = x(y(zz)) are exactly x*y = x + a*y + 1 with a^2 + a = 1 (mod N); predicted counts "
                  "1 (N=1), 1 (N=5), 2 (N=11), 0 for other N <= 12. H-C06-5 (derived by hand): (xy)z = x((yz)z) "
                  "has exactly one anchored model for odd N and none for even N.",
    "assumptions": ["affine spectrum computed for N <= 40 by direct evaluation",
                    "SAT spectra for N <= 6 for all laws; model enumeration (limit 1000) for N <= 9 for the "
                    "restricted laws; N = 10..12 solved for selected laws",
                    "conflict budget 2,000,000; UNKNOWN recorded"],
    "methodology": "Evaluate every affine table for every a in Z_N; compare with SAT; enumerate all anchored models of "
                   "restricted laws and test each for affinity (T[x][y] - x - 1 = a*y for a single a).",
    "falsification": "A law (other than LD) whose SAT spectrum differs from its affine spectrum; a non-affine model of "
                     "(xy)z = x(y(zz)) or (xy)z = x((yz)z); a model count different from the predicted root count.",
}

LHS = ["x(yz)", "(xy)z"]
VARS = ["x", "y", "z"]
LD = "x(yz) = (xy)(xz)"
GOLDEN = "(xy)z = x(y(zz))"
ODD = "(xy)z = x((yz)z)"


def anchor(n):
    return lambda S: [[S.v[x, 0, (x + 1) % n]] for x in range(n)]


def laws():
    out = []
    rhs = []
    for k in (2, 3):
        for sh in shapes(k):
            for lab in itertools.product(VARS, repeat=n_leaves(sh)):
                if set(lab) == set(VARS):
                    rhs.append(fill(sh, lab))
    for l in LHS:
        lt = parse(l)
        for t in rhs:
            if t != lt:
                out.append((f"{l} = {to_str(t)}", (lt, t)))
    return out


def affine_table(N, a):
    x = np.arange(N).reshape(-1, 1)
    y = np.arange(N).reshape(1, -1)
    return (x + a * y + 1) % N


def affine_solutions(law, N):
    return [a for a in range(N) if satisfies(affine_table(N, a), law)]


def is_affine(T):
    N = T.shape[0]
    if N == 1:
        return True, 0
    a = int((T[0, 1] - 1) % N)
    return bool(np.array_equal(T, affine_table(N, a))), a


def roots_golden(N):
    return [a for a in range(N) if (a * a + a - 1) % N == 0]


def run():
    t0 = time.perf_counter()
    L = laws()
    rows = {}
    for name, law in L:
        aff = {N: len(affine_solutions(law, N)) for N in range(1, 41)}
        sat = {}
        for N in range(1, 7):
            st, _ = MagmaSAT(N, [law], extra=anchor(N)).solve(conf_budget=2_000_000)
            sat[N] = st
        rows[name] = {"affine_counts": aff, "sat": sat,
                      "affine_spec_le6": [N for N in range(1, 7) if aff[N] > 0],
                      "sat_spec_le6": [N for N in range(1, 7) if sat[N] == "SAT"]}
    mismatches = [n for n, r in rows.items() if r["affine_spec_le6"] != r["sat_spec_le6"]]
    restricted = [n for n, r in rows.items() if r["sat_spec_le6"] not in ([1], list(range(1, 7)))]
    # enumerate and test affinity for restricted laws
    lawd = dict(L)
    detail = {}
    for name in restricted + [GOLDEN, ODD]:
        if name in detail:
            continue
        per = {}
        for N in range(1, 10):
            tables, complete = MagmaSAT(N, [lawd[name]], extra=anchor(N)).enumerate(limit=1000)
            aff_flags = [is_affine(T) for T in tables]
            per[N] = {"models": len(tables), "complete": complete,
                      "affine_models": sum(1 for f, _ in aff_flags if f),
                      "affine_a": sorted(a for f, a in aff_flags if f),
                      "non_affine_example": next((T.tolist() for T, (f, _) in zip(tables, aff_flags) if not f), None)
                      if N <= 4 else None}
        detail[name] = per
    # larger N for the two hand-derived laws
    extra = {}
    for name in (GOLDEN, ODD):
        ex = {}
        for N in (10, 11, 12):
            tables, complete = MagmaSAT(N, [lawd[name]], extra=anchor(N)).enumerate(limit=50)
            ex[N] = {"models": len(tables), "complete": complete,
                     "all_affine": all(is_affine(T)[0] for T in tables),
                     "a_values": sorted(is_affine(T)[1] for T in tables)}
        extra[name] = ex
    golden_pred = {N: len(roots_golden(N)) for N in range(1, 13)}
    golden_obs = {N: (detail[GOLDEN][N]["models"] if N <= 9 else extra[GOLDEN][N]["models"]) for N in range(1, 13)}
    odd_obs = {N: (detail[ODD][N]["models"] if N <= 9 else extra[ODD][N]["models"]) for N in range(1, 13)}
    non_affine = {n: {N: d["models"] - d["affine_models"] for N, d in per.items() if d["models"] != d["affine_models"]}
                  for n, per in detail.items()}
    non_affine = {n: v for n, v in non_affine.items() if v}
    return {
        "n_laws": len(rows),
        "spectrum_mismatch_affine_vs_sat_le6": mismatches,
        "restricted_laws": restricted,
        "restricted_detail": detail,
        "laws_with_non_affine_models": non_affine,
        "golden": {"predicted_counts": golden_pred, "observed_counts": golden_obs,
                   "agree": golden_pred == golden_obs, "N10_12": extra[GOLDEN]},
        "odd": {"observed_counts": odd_obs, "N10_12": extra[ODD],
                "agree": all(odd_obs[N] == (1 if N % 2 else 0) for N in odd_obs)},
        "golden_affine_spectrum_le40": [N for N in range(1, 41) if rows[GOLDEN]["affine_counts"][N] > 0],
        "odd_affine_spectrum_le40": [N for N in range(1, 41) if rows[ODD]["affine_counts"][N] > 0],
        "rows": rows,
        "timings": {"total_s": round(time.perf_counter() - t0, 1)},
        "summary": [f"{len(rows)} laws; affine vs SAT spectrum (N<=6) mismatches: {len(mismatches)} {mismatches}",
                    f"restricted laws: {len(restricted)}; laws with non-affine anchored models (N<=9): "
                    f"{ {n: v for n, v in non_affine.items()} }",
                    f"golden law counts predicted {golden_pred} observed {golden_obs}",
                    f"odd law counts {odd_obs}"],
    }
