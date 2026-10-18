"""EXP-C14-01: the 256 local graph products - associativity, commutativity, units, distributivity."""

import random

import numpy as np

from systems.graph_products import (CELLS, NAMED_CODES, assoc_defects, conjugate, has_left_unit, has_right_unit,
                                    is_associative, is_commutative, left_distributive, name_of, path, product,
                                    right_distributive, show, transpose)

META = {
    "id": "EXP-C14-01",
    "cycle": "C14",
    "title": "Exhaustive classification of the 256 local graph products",
    "agent": "Mathematical Explorer",
    "question": "Which of the 256 local products of simple graphs are (strictly) associative, commutative, unital "
                "and distributive over disjoint union?",
    "hypothesis": "H-C14-2 (from the Historian's recollection of Imrich-Izbicki 1975): exactly 20 local products are "
                  "associative, 10 of them commutative. H-C14-R (reduction lemma, to be proved): the canonical map "
                  "((g,h),k) -> (g,(h,k)) is an isomorphism for all G, H, K iff the relation-level identity "
                  "phi(phi(r1,r2),r3) = phi(r1,phi(r2,r3)) holds on the 26 triples != (E,E,E), and P3*P3*P3 "
                  "already detects every failure.",
    "assumptions": ["simple graphs (no loops); a product is a subset of the 8 cells (r1,r2) != (E,E)",
                    "strict notions (identity-like canonical maps); isomorphism-level notions in EXP-C14-02",
                    "random test graphs: 40 seeded triples of orders 1..4 per product"],
    "methodology": "Relation-level check of the 26 triples for every code; independent brute-force check on actual "
                   "graphs (P3^3 and random triples: adjacency matrices of (G*H)*K and G*(H*K) compared entrywise, "
                   "the canonical map being the identity on the index g|H||K| + h|K| + k); orbits under transposition "
                   "and complement-conjugation.",
    "falsification": "A code where the relation-level verdict and the graph-level verdict disagree, or a count "
                     "different from 20/10.",
    "seed": 14,
}


def rand_graph(rng, n):
    G = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.5:
                G[i, j] = G[j, i] = 1
    return G


def graph_assoc(code, G, H, K):
    return np.array_equal(product(code, product(code, G, H), K), product(code, G, product(code, H, K)))


def graph_comm(code, G, H):
    n, m = G.shape[0], H.shape[0]
    P, Q = product(code, G, H), product(code, H, G)
    perm = [h * n + g for g in range(n) for h in range(m)]  # (g,h) -> index of (h,g) in H*G
    return np.array_equal(P, Q[np.ix_(perm, perm)])


def run():
    rng = random.Random(META["seed"])
    tests = [tuple(rand_graph(rng, rng.randint(1, 4)) for _ in range(3)) for _ in range(40)]
    P3 = path(3)
    rows = []
    disagreements = []
    random_detected = 0
    for code in range(256):
        rel_assoc = is_associative(code)
        p3 = graph_assoc(code, P3, P3, P3)
        rnd = all(graph_assoc(code, *t) for t in tests)
        rel_comm = is_commutative(code)
        g_comm = graph_comm(code, P3, P3) and all(graph_comm(code, t[0], t[1]) for t in tests)
        if rel_assoc != p3:  # reduction lemma: P3^3 detects exactly the relation-level failures
            disagreements.append(("assoc-P3", code))
        if rel_assoc and not rnd:  # a relation-level associative code must pass every graph test
            disagreements.append(("assoc-random", code))
        random_detected += (not rel_assoc) and (not rnd)
        if rel_comm != g_comm:
            disagreements.append(("comm", code))
        rows.append({"code": code, "cells": show(code), "name": name_of(code), "associative": rel_assoc,
                     "n_defects": len(assoc_defects(code)), "commutative": rel_comm,
                     "left_unit": has_left_unit(code), "right_unit": has_right_unit(code),
                     "left_distributive": left_distributive(code), "right_distributive": right_distributive(code)})
    assoc = [r for r in rows if r["associative"]]
    # orbits under the Klein group <transpose, conjugate>
    orbits, seen = [], set()
    for code in range(256):
        if code in seen:
            continue
        orb = sorted({code, transpose(code), conjugate(code), transpose(conjugate(code))})
        seen.update(orb)
        orbits.append(orb)
    assoc_codes = {r["code"] for r in assoc}
    orbit_closed = all((set(o) <= assoc_codes) or not (set(o) & assoc_codes) for o in orbits)
    assoc_orbits = [o for o in orbits if set(o) <= assoc_codes]
    unital = [r["code"] for r in assoc if r["left_unit"] and r["right_unit"]]
    defect_hist = {}
    for r in rows:
        defect_hist[r["n_defects"]] = defect_hist.get(r["n_defects"], 0) + 1
    table = [{k: r[k] for k in ("code", "cells", "name", "commutative", "left_unit", "right_unit",
                                "left_distributive", "right_distributive")} for r in assoc]
    return {
        "n_products": 256,
        "n_associative": len(assoc),
        "n_associative_commutative": sum(r["commutative"] for r in assoc),
        "n_commutative_total": sum(r["commutative"] for r in rows),
        "associative_table": table,
        "two_sided_unit": unital,
        "two_sided_unit_named": [name_of(c) or show(c) for c in unital],
        "associative_and_both_distributive": [r["code"] for r in assoc if r["left_distributive"] and
                                              r["right_distributive"]],
        "n_orbits": len(orbits),
        "associative_orbits": assoc_orbits,
        "associativity_orbit_invariant": orbit_closed,
        "defect_histogram": dict(sorted(defect_hist.items())),
        "relation_vs_graph_disagreements": disagreements,
        "non_associative_detected_by_random_triples": random_detected,
        "named_products": {k: {"code": v, "associative": is_associative(v), "commutative": is_commutative(v)}
                           for k, v in NAMED_CODES.items()},
        "summary": [f"{len(assoc)} associative products, {sum(r['commutative'] for r in assoc)} of them commutative "
                    f"({sum(r['commutative'] for r in rows)} commutative in total)",
                    f"two-sided unit K1: {[name_of(c) or show(c) for c in unital]}",
                    f"relation-level vs graph-level disagreements: {len(disagreements)}",
                    f"{len(orbits)} orbits under <transpose, conjugate>; associativity orbit-invariant: {orbit_closed}"],
    }
