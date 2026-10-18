"""EXP-C16-01: Fibonacci pair maps of all magmas of order 2 and 3 and of all row-permutation magmas of order 4."""

import time
from collections import Counter

import numpy as np

from lab import oeis
from systems.magma_dynamics import (all_magmas, batch_analyze, batch_pair_next, canonical_codes, de_bruijn_count,
                                    row_permutation_magmas)

META = {
    "id": "EXP-C16-01",
    "cycle": "C16",
    "title": "Cycle structure of the Fibonacci pair map (a, b) -> (b, b*a) for all small magmas",
    "agent": "Mathematical Explorer",
    "question": "How long can the sequence x_{k+1} = x_k * x_{k-1} cycle in an n-element magma, when is the pair map a "
                "permutation, and which magmas attain the longest periods?",
    "hypothesis": "H-C16-1 (bold, Inventor): as for Pisano periods, where (0, 0) is fixed, the maximal period on an "
                  "n-element magma is at most n^2 - 1, and the maximum is attained only by quasigroups. H-C16-2 "
                  "(Formal Verifier): the pair map is a permutation iff every left translation a -> b*a is a "
                  "bijection, so exactly (n!)^n tables give permutations. H-C16-3 (Formal Verifier, after the "
                  "n = 2 data): the tables with a single cycle through all n^2 states correspond to de Bruijn cycles "
                  "of order 2, (n!)^n / n^2 of them (1, 24, 20736 for n = 2, 3, 4).",
    "assumptions": ["all 16 tables of order 2 and all 19683 of order 3; for order 4 only the (4!)^4 = 331776 tables "
                    "whose rows are permutations (the only candidates for a full cycle by H-C16-2)",
                    "isomorphism classes by brute-force canonical codes (n <= 3; full-period tables for n = 4)",
                    "the mirror recurrence x_{k+1} = x_{k-1} * x_k is the forward recurrence of the transposed table; "
                    "checked on the order-3 census"],
    "methodology": "Batch functional-graph analysis (orbit doubling, periods, transients) of the pair maps; count "
                   "permutation pair maps and full-period tables; test the quasigroup property of the full-period "
                   "tables; distributions of the maximal period; OEIS check of the counts.",
    "falsification": "H-C16-1: a table with a period n^2, or a non-quasigroup attaining the maximum. H-C16-2: a "
                     "permutation pair map with a non-bijective left translation or vice versa, or a count different "
                     "from (n!)^n. H-C16-3: a full-period count different from (n!)^n / n^2.",
}


def is_latin(tables):
    n = tables.shape[1]
    srt_rows = np.sort(tables, axis=2)
    srt_cols = np.sort(tables, axis=1)
    target = np.arange(n)
    return (srt_rows == target).all(axis=(1, 2)) & (srt_cols == target[:, None]).all(axis=(1, 2))


def rows_are_perms(tables):
    n = tables.shape[1]
    return (np.sort(tables, axis=2) == np.arange(n)).all(axis=(1, 2))


def census(tables, label, iso=True):
    n = tables.shape[1]
    t0 = time.perf_counter()
    r = batch_analyze(batch_pair_next(tables))
    latin = is_latin(tables)
    rp = rows_are_perms(tables)
    full = r["max_period"] == n * n
    out = {
        "label": label,
        "n": n,
        "tables": int(len(tables)),
        "max_period_distribution": {int(k): int(v) for k, v in sorted(Counter(r["max_period"].tolist()).items())},
        "max_period_overall": int(r["max_period"].max()),
        "permutation_pair_maps": int(r["is_permutation"].sum()),
        "criterion_violations": int((r["is_permutation"] != rp).sum()),
        "full_period_tables": int(full.sum()),
        "full_period_quasigroups": int((full & latin).sum()),
        "max_period_among_quasigroups": int(r["max_period"][latin].max()) if latin.any() else None,
        "quasigroups": int(latin.sum()),
        "max_transient": int(r["max_transient"].max()),
        "seconds": round(time.perf_counter() - t0, 2),
    }
    if iso:
        codes = canonical_codes(tables)
        out["iso_classes"] = int(np.unique(codes).size)
        out["iso_classes_full_period"] = int(np.unique(codes[full]).size)
        out["iso_classes_by_max_period"] = {int(k): int(np.unique(codes[r["max_period"] == k]).size)
                                            for k in sorted(set(r["max_period"].tolist()))}
    elif full.any():
        codes = canonical_codes(tables[full])
        out["iso_classes_full_period"] = int(np.unique(codes).size)
    out["full_period_examples"] = [t.tolist() for t in tables[full][:3]]
    return out, r


def run():
    timings = {}
    res = {}
    t0 = time.perf_counter()
    for n in (2, 3):
        res[str(n)], r = census(all_magmas(n), f"all magmas of order {n}")
    timings["orders_2_3"] = round(time.perf_counter() - t0, 2)
    # mirror recurrence = forward recurrence of the transpose: compare distributions on order 3
    T3 = all_magmas(3)
    rm = batch_analyze(batch_pair_next(T3, mirror=True))
    rf = batch_analyze(batch_pair_next(np.transpose(T3, (0, 2, 1))))
    mirror_ok = bool((rm["max_period"] == rf["max_period"]).all() and (rm["n_cycles"] == rf["n_cycles"]).all())
    t0 = time.perf_counter()
    res["4"], r4 = census(row_permutation_magmas(4), "row-permutation magmas of order 4", iso=False)
    timings["order_4"] = round(time.perf_counter() - t0, 2)
    predicted = {str(n): {"permutations": __import__("math").factorial(n) ** n, "full": de_bruijn_count(n)}
                 for n in (2, 3, 4)}
    checks = {n: {"permutation_count_ok": res[n]["permutation_pair_maps"] == predicted[n]["permutations"],
                  "full_period_count_ok": res[n]["full_period_tables"] == predicted[n]["full"]}
              for n in ("2", "3")}
    checks["4"] = {"permutation_count_ok": res["4"]["permutation_pair_maps"] == predicted["4"]["permutations"],
                   "full_period_count_ok": res["4"]["full_period_tables"] == predicted["4"]["full"]}
    h1_refuted = any(res[n]["max_period_overall"] == int(n) ** 2 for n in res)
    nonquasi_full = {n: res[n]["full_period_tables"] - res[n]["full_period_quasigroups"] for n in res}
    look = oeis.novelty_check([res[n]["full_period_quasigroups"] for n in ("2", "3", "4")])
    dist3 = res["3"]["max_period_distribution"]
    look_dist = oeis.novelty_check([dist3.get(k, 0) for k in range(1, 10)])
    return {
        "census": res,
        "predicted": predicted,
        "checks": checks,
        "mirror_equals_transpose_forward": mirror_ok,
        "H_C16_1_refuted": h1_refuted,
        "full_period_non_quasigroups": nonquasi_full,
        "oeis_full_period_quasigroups": {"terms": [res[n]["full_period_quasigroups"] for n in ("2", "3", "4")],
                                         "status": look["status"], "hits": look.get("hits", [])[:3]},
        "oeis_order3_max_period_distribution": {"status": look_dist["status"], "hits": look_dist.get("hits", [])[:3]},
        "timings": timings,
        "summary": [
            "max period over all tables: " + ", ".join(f"n={n}: {res[n]['max_period_overall']}" for n in res),
            "permutation pair maps (predicted (n!)^n): " + ", ".join(
                f"n={n}: {res[n]['permutation_pair_maps']} ({predicted[n]['permutations']}), criterion violations "
                f"{res[n]['criterion_violations']}" for n in res),
            "full-period tables (predicted (n!)^n/n^2): " + ", ".join(
                f"n={n}: {res[n]['full_period_tables']} ({predicted[n]['full']}), of which quasigroups "
                f"{res[n]['full_period_quasigroups']}" for n in res),
            f"max period among quasigroups: " + ", ".join(f"n={n}: {res[n]['max_period_among_quasigroups']}"
                                                         for n in res),
            f"order 3: {res['3']['iso_classes']} isomorphism classes, max-period distribution {dist3}",
            f"mirror dynamics = forward dynamics of the transpose (order 3): {mirror_ok}",
        ],
    }
