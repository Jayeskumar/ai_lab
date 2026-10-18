"""EXP-C14-02: is a local product associative / commutative up to isomorphism only when it is strictly so?"""

import itertools

import numpy as np

from systems.graph_products import atlas, is_associative, is_commutative, isomorphic, product, show


def simple_invariant(M):
    """Edge count and degree sequence: a certificate of non-isomorphism checkable by hand."""
    return int(M.sum()) // 2, tuple(sorted(np.asarray(M).sum(axis=1).tolist()))

META = {
    "id": "EXP-C14-02",
    "cycle": "C14",
    "title": "Isomorphism-level versus strict associativity and commutativity of local products",
    "agent": "Mathematical Inventor",
    "question": "Can a local product satisfy (G*H)*K = G*(H*K) (or G*H = H*G) up to isomorphism for all graphs "
                "although the canonical map is not an isomorphism?",
    "hypothesis": "H-C14-1 (bold): no - for local products, associativity and commutativity up to isomorphism are "
                  "equivalent to their strict versions; for every one of the 236 non-associative (224 non-commutative) "
                  "products a witness exists among graphs with at most 3 vertices.",
    "assumptions": ["witness search over the 7 graphs with 1-3 vertices (all triples / pairs, ordered by total "
                    "order), escalating to graphs with <= 4 vertices if needed",
                    "isomorphism decided exactly (invariants, then networkx VF2)"],
    "methodology": "For each non-strict code, search the smallest triple (G,H,K) with (G*H)*K not isomorphic to "
                   "G*(H*K), and the smallest pair with G*H not isomorphic to H*G.",
    "falsification": "A non-strict code without any witness (then it would be associative/commutative only up to "
                     "isomorphism, refuting H-C14-1, and would be examined by hand).",
}


def search_assoc(code, graphs):
    triples = sorted(itertools.product(range(len(graphs)), repeat=3),
                     key=lambda t: (graphs[t[0]].shape[0] * graphs[t[1]].shape[0] * graphs[t[2]].shape[0], t))
    for t in triples:
        G, H, K = (graphs[i] for i in t)
        if not isomorphic(product(code, product(code, G, H), K), product(code, G, product(code, H, K))):
            return t
    return None


def search_comm(code, graphs):
    pairs = sorted(itertools.product(range(len(graphs)), repeat=2),
                   key=lambda t: (graphs[t[0]].shape[0] * graphs[t[1]].shape[0], t))
    for t in pairs:
        G, H = (graphs[i] for i in t)
        if not isomorphic(product(code, G, H), product(code, H, G)):
            return t
    return None


def run():
    small = atlas(3)
    larger = atlas(4)
    names = ["K1", "2K1", "K2", "3K1", "K2+K1", "P3", "K3"]
    a_rows, c_rows, a_none, c_none = {}, {}, [], []
    for code in range(256):
        if not is_associative(code):
            w = search_assoc(code, small)
            if w is None:
                w4 = search_assoc(code, larger)
                a_none.append({"code": code, "cells": show(code), "witness_le4": w4})
            else:
                a_rows[code] = [names[i] for i in w]
        if not is_commutative(code):
            w = search_comm(code, small)
            if w is None:
                w4 = search_comm(code, larger)
                c_none.append({"code": code, "cells": show(code), "witness_le4": w4})
            else:
                c_rows[code] = [names[i] for i in w]
    # how many witnesses are certified already by edge count / degree sequence
    small_by_name = dict(zip(names, small))
    cert_a = sum(1 for code, w in a_rows.items() if simple_invariant(
        product(code, product(code, small_by_name[w[0]], small_by_name[w[1]]), small_by_name[w[2]])) !=
        simple_invariant(product(code, small_by_name[w[0]], product(code, small_by_name[w[1]], small_by_name[w[2]]))))
    cert_c = sum(1 for code, w in c_rows.items() if simple_invariant(
        product(code, small_by_name[w[0]], small_by_name[w[1]])) !=
        simple_invariant(product(code, small_by_name[w[1]], small_by_name[w[0]])))
    size_hist = {}
    for w in a_rows.values():
        s = 1
        for nm in w:
            s *= {"K1": 1, "2K1": 2, "K2": 2}.get(nm, 3)
        size_hist[s] = size_hist.get(s, 0) + 1
    return {
        "n_non_associative": 236,
        "assoc_witnesses_found": len(a_rows),
        "assoc_no_witness_le3": a_none,
        "n_non_commutative": 224,
        "comm_witnesses_found": len(c_rows),
        "comm_no_witness_le3": c_none,
        "assoc_witness_order_histogram": dict(sorted(size_hist.items())),
        "assoc_witnesses_certified_by_degree_sequence": cert_a,
        "comm_witnesses_certified_by_degree_sequence": cert_c,
        "assoc_witnesses": {str(k): v for k, v in a_rows.items()},
        "comm_witnesses": {str(k): v for k, v in c_rows.items()},
        "summary": [f"associativity witnesses among graphs <= 3 vertices: {len(a_rows)}/236; without: "
                    f"{[(d['code'], d['cells']) for d in a_none]}",
                    f"commutativity witnesses: {len(c_rows)}/224; without: {[(d['code'], d['cells']) for d in c_none]}",
                    f"witness product orders: {dict(sorted(size_hist.items()))}",
                    f"witnesses certified by edge count/degree sequence alone: assoc {cert_a}/{len(a_rows)}, "
                    f"comm {cert_c}/{len(c_rows)}"],
    }
