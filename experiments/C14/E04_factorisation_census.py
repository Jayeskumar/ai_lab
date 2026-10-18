"""EXP-C14-04: prime graphs and (non-)unique factorisation for the eight unital associative local products."""

import itertools

import networkx as nx
import numpy as np

from lab import oeis
from systems.graph_products import (IsoRegistry, atlas, complement, disjoint_union, empty, is_commutative,
                                    is_connected, isomorphic, name_of, product, show, K)

META = {
    "id": "EXP-C14-04",
    "cycle": "C14",
    "title": "Prime factorisation census for the eight associative local products with unit K1 (orders <= 15)",
    "agent": "Mathematical Explorer",
    "question": "For each associative local product with two-sided unit K1, which graphs of order <= 15 are "
                "composite, how many primes are there of each order, and where does unique factorisation fail?",
    "hypothesis": "H-C14-3 (bold, Inventor): each of the six commutative unital associative products has unique "
                  "prime factorisation on connected graphs (Cartesian: Sabidussi-Vizing; strong: Doerfler-Imrich/"
                  "McKenzie) or, for the complement-duals, on co-connected graphs. H-C14-7: Cartesian-prime and "
                  "strong-prime connected graphs are equinumerous in every order (forced by unique factorisation "
                  "and the common count of connected graphs).",
    "assumptions": ["all graphs with <= 7 vertices (networkx atlas) as candidate factors; composites of order "
                    "n <= 15 are exactly the products of primes of orders whose product is n (n in 4,6,8,9,10,12,14,15)",
                    "graph counts A000088 / A001349 taken from the OEIS (cached) to turn composite counts into "
                    "prime counts", "isomorphism decided exactly (invariants + VF2)"],
    "methodology": "For each product: find the composite graphs of orders 4 and 6 among the atlas graphs, take the "
                   "rest as primes, enumerate all prime factorisations (multisets for commutative products, sequences "
                   "otherwise) of every order <= 15, classify the products up to isomorphism, and record classes with "
                   "more than one factorisation; repeat inside the class of connected graphs; verify the classical "
                   "63-vertex Cartesian counterexample (K1+K2+Q2)(K1+Q3) = (K1+Q2+Q4)(K1+K2).",
    "falsification": "A connected (resp. co-connected) graph with two different factorisations into connected "
                     "(resp. co-connected) primes for one of the six commutative unital products.",
}

UNITAL = [5, 13, 29, 77, 85, 93, 141, 221]
ORDERS = [4, 6, 8, 9, 10, 12, 14, 15]


def oeis_data(anum):
    rec = oeis._query(f"id:{anum}")
    r = rec["response"]
    r = r if isinstance(r, list) else r.get("results")
    off = int(str(r[0].get("offset", "0")).split(",")[0])
    return {off + i: int(x) for i, x in enumerate(r[0]["data"].split(","))}


def factor_shapes(n, orders):
    """Non-decreasing tuples of prime orders (each >= 2, each in `orders`) with product n and length >= 2."""
    out = []

    def rec(rem, start, acc):
        if rem == 1:
            if len(acc) >= 2:
                out.append(tuple(acc))
            return
        for d in range(start, rem + 1):
            if rem % d == 0 and d in orders:
                rec(rem // d, d, acc + [d])
    rec(n, 2, [])
    return out


def census(code, graphs, connected_only=False):
    comm = is_commutative(code)
    pool = [G for G in graphs if (is_connected(G) or not connected_only)]
    by_order = {}
    for i, G in enumerate(pool):
        by_order.setdefault(G.shape[0], []).append(i)
    # composites among the pool (orders 4 and 6 only can be composite below 8)
    reg_small = {n: IsoRegistry() for n in (4, 6)}
    ids_small = {n: [reg_small[n].add(pool[i]) for i in by_order.get(n, [])] for n in (4, 6)}
    composite_small = {4: set(), 6: set()}
    for n, splits in ((4, [(2, 2)]), (6, [(2, 3), (3, 2)])):
        for a, b in splits:
            for i in by_order.get(a, []):
                for j in by_order.get(b, []):
                    P = product(code, pool[i], pool[j])
                    if connected_only and not is_connected(P):
                        continue
                    cid = reg_small[n].find(P)
                    if cid is not None:
                        composite_small[n].add(cid)
    primes = {}
    for n, idx in by_order.items():
        if n == 1:
            continue
        if n in (4, 6):
            primes[n] = [i for k, i in enumerate(idx) if ids_small[n][k] not in composite_small[n]]
        else:
            primes[n] = list(idx)
    res = {}
    for n in ORDERS:
        reg = IsoRegistry()
        facts = {}
        for shape in factor_shapes(n, primes):
            if comm:
                groups = itertools.groupby(shape)
                iters = [itertools.combinations_with_replacement(primes[d], len(list(g))) for d, g in groups]
                seqs = (sum(c, ()) for c in itertools.product(*iters))
            else:
                seqs = itertools.chain.from_iterable(
                    itertools.product(*[primes[d] for d in perm]) for perm in set(itertools.permutations(shape)))
            for seq in seqs:
                P = pool[seq[0]]
                for i in seq[1:]:
                    P = product(code, P, pool[i])
                if connected_only and not is_connected(P):
                    continue
                cid = reg.add(P)
                facts.setdefault(cid, []).append(seq)
        multi = {cid: f for cid, f in facts.items() if len(f) > 1}
        multi_multiset = {cid: f for cid, f in facts.items() if len({tuple(sorted(s)) for s in f}) > 1}
        res[n] = {"factorisations": sum(len(f) for f in facts.values()), "composite_classes": len(facts),
                  "classes_with_several_factorisations": len(multi),
                  "classes_with_several_factor_multisets": len(multi_multiset),
                  "example": describe(pool, next(iter(multi_multiset.values()))) if multi_multiset else
                  (describe(pool, next(iter(multi.values()))) if multi else None)}
    prime_small = {n: len(v) for n, v in sorted(primes.items())}
    return res, prime_small


def g6(G):
    return nx.to_graph6_bytes(nx.from_numpy_array(G), header=False).decode().strip()


def describe(pool, seqs):
    return [[g6(pool[i]) for i in s] for s in seqs[:3]]


def cube(code, k):
    G = K(1)
    for _ in range(k):
        G = product(code, G, K(2))
    return G


def known_counterexample():
    """(K1 + K2 + Q2)(K1 + Q3) = (K1 + Q2 + Q4)(K1 + K2) for the Cartesian (5) and strong (13) products."""
    out = {}
    for code in (5, 13):
        Q = {k: cube(code, k) for k in range(5)}
        a = disjoint_union(disjoint_union(Q[0], Q[1]), Q[2])
        b = disjoint_union(Q[0], Q[3])
        c = disjoint_union(disjoint_union(Q[0], Q[2]), Q[4])
        d = disjoint_union(Q[0], Q[1])
        out[name_of(code)] = {"order": int(a.shape[0] * b.shape[0]),
                              "isomorphic": isomorphic(product(code, a, b), product(code, c, d))}
    return out


def run():
    graphs = atlas(7)
    g_all = oeis_data("A000088")
    g_conn = oeis_data("A001349")
    out = {}
    for code in UNITAL:
        label = name_of(code) or show(code)
        res_all, prime_small_all = census(code, graphs)
        res_conn, prime_small_conn = census(code, graphs, connected_only=True)
        primes_all = {}
        for n in range(2, 16):
            if n <= 7:
                primes_all[n] = prime_small_all[n]
            else:
                primes_all[n] = g_all[n] - (res_all[n]["composite_classes"] if n in res_all else 0)
        out[label] = {"code": code, "all_graphs": res_all, "connected": res_conn,
                      "primes_all_graphs": {n: primes_all[n] for n in sorted(primes_all)},
                      "primes_connected_le7": prime_small_conn}
    # connected primes for the Cartesian and strong products from the census, n <= 15
    conn_primes = {}
    for code in (5, 13):
        label = name_of(code)
        res = out[label]["connected"]
        cp = {}
        for n in range(2, 16):
            comp = res[n]["composite_classes"] if n in res else 0
            cp[n] = g_conn[n] - comp
        conn_primes[label] = cp
    # OEIS checks
    checks = {}
    for label, cp in conn_primes.items():
        seq = [cp[n] for n in range(2, 16)]
        checks[f"{label} connected primes n=2..15"] = {"terms": seq, **oeis.novelty_check(seq[:12])}
    for label in out:
        seq = [out[label]["primes_all_graphs"][n] for n in range(2, 12)]
        checks[f"{label} primes (all graphs) n=2..11"] = {"terms": seq, **oeis.novelty_check(seq)}
    nonunique = {label: {n: r["classes_with_several_factor_multisets"] for n, r in v["all_graphs"].items()
                         if r["classes_with_several_factor_multisets"]} for label, v in out.items()}
    nonunique_conn = {label: {n: r["classes_with_several_factor_multisets"] for n, r in v["connected"].items()
                              if r["classes_with_several_factor_multisets"]} for label, v in out.items()}
    ordered_nonunique = {label: {n: r["classes_with_several_factorisations"] for n, r in v["all_graphs"].items()
                                 if r["classes_with_several_factorisations"]} for label, v in out.items()}
    ce = known_counterexample()
    return {
        "products": out,
        "connected_primes_cartesian_strong": conn_primes,
        "cartesian_equals_strong_connected_prime_counts": conn_primes["cartesian"] == conn_primes["strong"],
        "nonunique_multiset_all_graphs": nonunique,
        "nonunique_multiset_connected": nonunique_conn,
        "nonunique_ordered_all_graphs": ordered_nonunique,
        "known_63_vertex_counterexample": ce,
        "oeis": {k: {kk: v[kk] for kk in ("terms", "status", "hits") if kk in v} for k, v in checks.items()},
        "summary": [f"orders with non-unique factorisation (multisets of primes, all graphs): {nonunique}",
                    f"... inside connected graphs: {nonunique_conn}",
                    f"Cartesian connected primes n=2..15: {[conn_primes['cartesian'][n] for n in range(2, 16)]}; "
                    f"equal to strong: {conn_primes['cartesian'] == conn_primes['strong']}",
                    f"63-vertex counterexample verified: {ce}",
                    "OEIS: " + "; ".join(f"{k}: {v['status']}" for k, v in checks.items())],
    }
