"""EXP-C16-02: full-period quasigroups - exhaustive orders <= 5, existence for orders 6..16, products, parity."""

import time
from collections import Counter

import numpy as np

from lab import oeis
from systems.magma_dynamics import (analyze, batch_analyze, batch_pair_next, canonical_codes,
                                    count_universal_cycles, cycle_sequence, first_universal_cycle, generate_group,
                                    group_table, is_latin_table, latin_squares, left_division_table,
                                    orbit_length_from_origin, pair_next, product_table, random_isotope,
                                    random_latin, row_sign_product, table_from_cycle)

META = {
    "id": "EXP-C16-02",
    "cycle": "C16",
    "title": "Quasigroups whose Fibonacci pair map is a single cycle through all n^2 pairs",
    "agent": "Mathematical Skeptic",
    "question": "EXP-C16-01 found no quasigroup of order <= 4 with a full period n^2 (the quasigroup maximum was n^2 - 1). "
                "Is that a law, or a small-number accident?",
    "hypothesis": "H-C16-5 (bold, from the n <= 4 data): no quasigroup of any order has a full-period pair map; the "
                  "maximal period of a quasigroup of order n is n^2 - 1. H-C16-6 (Formal Verifier, parity): a "
                  "full-period table must satisfy prod_b sgn(a -> b*a) = (-1)^((n-1)(n+2)/2); for groups of even "
                  "order this fails for every isotope, so no isotope of a group of even order is full-period.",
    "assumptions": ["all Latin squares of orders 2..5 (2, 12, 576, 161280)", "an independent depth-first count of "
                    "cyclic sequences with all pairs distinct at distances 1 and 2 (orders <= 5)",
                    "orders 6..16: deterministic sampling (seeded) of isotopes of Z_n (odd n) and of random Latin "
                    "squares built from random perfect matchings (all n); every example is re-verified",
                    "groups of even order 4, 6, 8: 2000 random isotopes each"],
    "methodology": "Batch pair-map analysis of all Latin squares of order <= 5; DFS enumeration of universal cycles; "
                   "sampling for larger orders with verification by an independent cycle analysis; direct products "
                   "of examples of coprime orders; row-sign products of all full-period tables and of group isotopes.",
    "falsification": "H-C16-5: one full-period quasigroup. H-C16-6: a full-period table violating the parity, or a "
                     "full-period isotope of a group of even order.",
    "seed": 16,
}


def quaternion_table():
    # elements: index = 4*s + u, s in {0 (+), 1 (-)}, u in {1, i, j, k} -> 0..3
    mul = {(0, 0): (0, 0), (0, 1): (0, 1), (0, 2): (0, 2), (0, 3): (0, 3),
           (1, 0): (0, 1), (1, 1): (1, 0), (1, 2): (0, 3), (1, 3): (1, 2),
           (2, 0): (0, 2), (2, 1): (1, 3), (2, 2): (1, 0), (2, 3): (0, 1),
           (3, 0): (0, 3), (3, 1): (0, 2), (3, 2): (1, 1), (3, 3): (1, 0)}
    T = np.zeros((8, 8), dtype=np.int64)
    for x in range(8):
        for y in range(8):
            sx, ux = divmod(x, 4)
            sy, uy = divmod(y, 4)
            s, u = mul[(ux, uy)]
            T[x, y] = 4 * ((sx + sy + s) % 2) + u
    return T


def cyclic(n):
    x = np.arange(n)
    return (x[:, None] + x[None, :]) % n


def run():
    rng = np.random.default_rng(META["seed"])
    timings = {}
    # A. exhaustive Latin squares
    t0 = time.perf_counter()
    exhaustive = {}
    full5 = None
    for n in (2, 3, 4, 5):
        L = latin_squares(n)
        r = batch_analyze(batch_pair_next(L))
        full = r["max_period"] == n * n
        par_needed = (-1) ** ((n - 1) * (n + 2) // 2)
        parities = np.array([row_sign_product(T) for T in L])
        exhaustive[str(n)] = {
            "latin_squares": int(len(L)),
            "full_period": int(full.sum()),
            "max_period": int(r["max_period"].max()),
            "max_period_distribution_top": {int(k): int(v) for k, v in
                                            sorted(Counter(r["max_period"].tolist()).items())[-5:]},
            "right_parity": int((parities == par_needed).sum()),
            "full_period_with_wrong_parity": int((full & (parities != par_needed)).sum()),
        }
        if n == 5:
            full5 = L[full]
    codes = canonical_codes(full5)
    D_full = sum(1 for T in full5 if orbit_length_from_origin(left_division_table(T)) == 25 and
                 analyze(pair_next(left_division_table(T)))["max_period"] == 25)
    exhaustive["5"]["iso_classes_of_full_period"] = int(np.unique(codes).size)
    exhaustive["5"]["left_division_parastrophes_full_period"] = int(D_full)
    timings["exhaustive"] = round(time.perf_counter() - t0, 2)
    # B. independent DFS count
    t0 = time.perf_counter()
    dfs = {}
    for n in (2, 3, 4, 5):
        cnt, nodes, complete = count_universal_cycles(n)
        dfs[str(n)] = {"count": int(cnt), "nodes": int(nodes), "complete": bool(complete)}
    agree = all(dfs[k]["count"] == exhaustive[k]["full_period"] and dfs[k]["complete"] for k in dfs)
    timings["dfs"] = round(time.perf_counter() - t0, 2)
    # C. existence for orders 6..16
    t0 = time.perf_counter()
    examples, sampling = {}, {}
    for n in range(6, 17):
        found = None
        stats = {}
        if n % 2 == 1:
            Z = cyclic(n)
            hits = 0
            for _ in range(2000):
                T = random_isotope(Z, rng)
                if orbit_length_from_origin(T) == n * n:
                    hits += 1
                    if found is None:
                        found = ("isotope of Z_n", T)
            stats["cyclic_isotopes"] = {"samples": 2000, "full_period": hits}
        hits = 0
        for _ in range(1500):
            T = random_latin(n, rng)
            if orbit_length_from_origin(T) == n * n:
                hits += 1
                if found is None:
                    found = ("random Latin square", T)
        stats["random_latin"] = {"samples": 1500, "full_period": hits}
        sampling[str(n)] = stats
        if found is not None:
            how, T = found
            an = analyze(pair_next(T))
            examples[str(n)] = {"construction": how, "latin": is_latin_table(T), "max_period": an["max_period"],
                                "n_cycles": an["n_cycles"], "row_sign_product": row_sign_product(T),
                                "cycle": cycle_sequence(T)}
    timings["existence"] = round(time.perf_counter() - t0, 2)
    # small orders 6..8 also by the deterministic DFS (first solution)
    dfs_first = {}
    for n in (6, 7, 8):
        seq, nodes, complete = first_universal_cycle(n)
        T = table_from_cycle(seq)
        dfs_first[str(n)] = {"nodes": int(nodes), "latin": is_latin_table(T),
                             "max_period": analyze(pair_next(T))["max_period"]}
    # D. products of coprime orders
    base = {int(k): table_from_cycle(v["cycle"]) for k, v in examples.items()}
    base[5] = full5[0]
    prods = {}
    for n1, n2 in ((5, 6), (5, 7), (5, 8), (6, 7), (7, 8), (5, 9), (7, 9), (8, 9)):
        P = product_table(base[n1], base[n2])
        an = analyze(pair_next(P))
        prods[f"{n1}x{n2}"] = {"order": n1 * n2, "latin": is_latin_table(P), "max_period": an["max_period"],
                               "full": an["max_period"] == (n1 * n2) ** 2}
    # E. group isotopes of even order
    groups = {"Z4": cyclic(4), "Z2xZ2": product_table(cyclic(2), cyclic(2)), "Z6": cyclic(6),
              "S3": group_table(generate_group([(1, 0, 2), (1, 2, 0)])), "Z8": cyclic(8),
              "Z2xZ4": product_table(cyclic(2), cyclic(4)),
              "Z2^3": product_table(cyclic(2), product_table(cyclic(2), cyclic(2))),
              "D4": group_table(generate_group([(1, 2, 3, 0), (0, 3, 2, 1)])), "Q8": quaternion_table()}
    giso = {}
    for name, G in groups.items():
        n = G.shape[0]
        sg = set()
        full = 0
        for _ in range(2000):
            T = random_isotope(G, rng)
            sg.add(row_sign_product(T))
            full += orbit_length_from_origin(T) == n * n and analyze(pair_next(T))["max_period"] == n * n
        giso[name] = {"order": n, "row_sign_products_seen": sorted(sg), "predicted": (-1) ** (n // 2),
                      "needed_for_full_period": (-1) ** ((n - 1) * (n + 2) // 2), "full_period_isotopes": int(full)}
    # parity of every example found
    parity_ok = all(v["row_sign_product"] == (-1) ** ((int(k) - 1) * (int(k) + 2) // 2) for k, v in examples.items())
    look = oeis.novelty_check([exhaustive[str(n)]["max_period"] for n in (2, 3, 4)] +
                              [25] + [int(k) ** 2 for k in sorted(examples, key=int)])
    return {
        "exhaustive": exhaustive,
        "dfs_counts": dfs,
        "dfs_agrees_with_exhaustive": agree,
        "dfs_first_solutions": dfs_first,
        "sampling": sampling,
        "examples": examples,
        "products": prods,
        "group_isotopes": giso,
        "examples_satisfy_parity": parity_ok,
        "H_C16_5_refuted": exhaustive["5"]["full_period"] > 0,
        "oeis_quasigroup_max_period": {"status": look["status"], "hits": look.get("hits", [])[:3]},
        "timings": timings,
        "summary": [
            "full-period quasigroups (exhaustive): " + ", ".join(
                f"n={n}: {exhaustive[n]['full_period']} of {exhaustive[n]['latin_squares']}" for n in exhaustive),
            f"independent DFS counts agree: {agree} ({ {k: v['count'] for k, v in dfs.items()} })",
            f"order 5: {exhaustive['5']['iso_classes_of_full_period']} isomorphism classes; left-division parastrophes "
            f"full-period: {exhaustive['5']['left_division_parastrophes_full_period']}",
            "examples found and verified for n = " + ", ".join(sorted(examples, key=int)) +
            "; all satisfy the parity condition: " + str(parity_ok),
            "coprime products full-period: " + ", ".join(f"{k}: {v['full']}" for k, v in prods.items()),
            "even-order group isotopes: " + ", ".join(
                f"{k}: signs {v['row_sign_products_seen']} (needed {v['needed_for_full_period']}), full "
                f"{v['full_period_isotopes']}" for k, v in giso.items()),
        ],
    }
