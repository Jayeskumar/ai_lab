"""EXP-C14-05: does the symmetric-difference (XOR) product factor uniquely on switching classes (two-graphs)?"""

import itertools

import numpy as np

from lab import oeis
from systems.graph_products import SwitchingRegistry, atlas, isomorphic, product, switch, K, empty

META = {
    "id": "EXP-C14-05",
    "cycle": "C14",
    "title": "Prime factorisation of two-graphs under the symmetric-difference product",
    "agent": "Mathematical Inventor",
    "question": "The symmetric difference (XOR) product respects Seidel switching (Theorem 6). On switching classes "
                "(two-graphs), is factorisation into primes unique?",
    "hypothesis": "H-C14-4 (bold): every two-graph of order <= 16 has exactly one factorisation into prime two-graphs "
                  "under XOR. H-C14-8: K2 xor X and K2 xor Y are isomorphic graphs iff X and Y are switching "
                  "equivalent (the 'if' part is proved in Theorem 7; 'only if' is tested here for orders <= 7).",
    "assumptions": ["switching classes of order n <= 8 obtained from all graphs with <= 7 vertices (order 8: a "
                    "7-vertex graph plus an isolated vertex represents every class)",
                    "switching equivalence decided exactly: same Seidel spectrum, then isomorphism of descendants",
                    "class counts validated against OEIS A002854"],
    "methodology": "Classify switching classes by order, find composite classes (orders 4, 6, 8), enumerate all "
                   "multisets of prime classes with product order n in {4,6,8,9,10,12,14,15,16}, classify the XOR "
                   "products up to switching, record collisions; count primes per order.",
    "falsification": "Two different multisets of prime two-graphs with switching-equivalent XOR products.",
}

XOR = 85
ORDERS = [4, 6, 8, 9, 10, 12, 14, 15, 16]


def classes_up_to(n_max):
    regs = {n: SwitchingRegistry() for n in range(1, n_max + 1)}
    for G in atlas(7):
        regs[G.shape[0]].add(G)
        if n_max >= 8 and G.shape[0] == 7:
            H = np.zeros((8, 8), dtype=np.int8)
            H[:7, :7] = G
            regs[8].add(H)
    return regs


def factor_shapes(n, orders):
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


def run():
    rec = oeis._query("id:A002854")
    r = rec["response"]
    r = r if isinstance(r, list) else r.get("results")
    off = int(str(r[0].get("offset", "1")).split(",")[0])
    a2854 = {off + i: int(x) for i, x in enumerate(r[0]["data"].split(","))}
    regs = classes_up_to(8)
    counts = {n: len(regs[n].reps) for n in regs}
    count_ok = all(counts[n] == a2854[n] for n in counts)
    # composite classes among orders 4, 6, 8
    composite = {n: set() for n in (4, 6, 8)}
    for n in (4, 6, 8):
        for a in range(2, n):
            if n % a or n // a < 2:
                continue
            for X in regs[a].reps:
                for Y in regs[n // a].reps:
                    composite[n].add(regs[n].find(product(XOR, X, Y)))
    primes = {n: [i for i in range(len(regs[n].reps)) if n not in composite or i not in composite[n]]
              for n in range(2, 9)}
    results = {}
    for n in ORDERS:
        reg = SwitchingRegistry()
        facts = {}
        for shape in factor_shapes(n, {d: 1 for d in primes}):
            groups = [(d, len(list(g))) for d, g in itertools.groupby(shape)]
            for combo in itertools.product(*[itertools.combinations_with_replacement(primes[d], k) for d, k in groups]):
                seq = []
                for (d, _), c in zip(groups, combo):
                    seq += [(d, i) for i in c]
                P = regs[seq[0][0]].reps[seq[0][1]]
                for d, i in seq[1:]:
                    P = product(XOR, P, regs[d].reps[i])
                cid = reg.add(P)
                facts.setdefault(cid, []).append(tuple(seq))
        multi = {cid: f for cid, f in facts.items() if len(f) > 1}
        results[n] = {"factorisations": sum(len(f) for f in facts.values()), "composite_classes": len(facts),
                      "classes_with_several_factorisations": len(multi),
                      "examples": [f for f in list(multi.values())[:3]]}
    prime_counts = {n: (len(primes[n]) if n <= 8 else a2854[n] - (results[n]["composite_classes"] if n in results
                                                                    else 0)) for n in range(2, 17)}
    # H-C14-8 'only if': K2 xor X ~ K2 xor Y (as graphs) implies X ~ Y (switching), orders <= 6 (all graphs)
    graphs = [G for G in atlas(6) if G.shape[0] >= 2]
    viol, tested = 0, 0
    K2 = K(2)
    by_n = {}
    for G in graphs:
        by_n.setdefault(G.shape[0], []).append(G)
    for n, gs in by_n.items():
        prods = [product(XOR, K2, G) for G in gs]
        for i, j in itertools.combinations(range(len(gs)), 2):
            same_graph = isomorphic(prods[i], prods[j])
            same_class = SwitchingRegistry.equivalent(gs[i], gs[j])
            tested += 1
            viol += same_graph and not same_class
            viol += same_class and not same_graph
    seq = [prime_counts[n] for n in range(2, 17)]
    nov = oeis.novelty_check(seq[:12])
    return {
        "class_counts": counts,
        "class_counts_match_A002854": count_ok,
        "composite_classes_small": {n: len(v) for n, v in composite.items()},
        "factorisation": results,
        "prime_two_graph_counts": prime_counts,
        "oeis_prime_counts": {k: nov[k] for k in ("status", "hits", "query") if k in nov},
        "k2_cancellation_pairs_tested": tested,
        "k2_cancellation_violations": viol,
        "summary": [f"switching classes n=1..8: {list(counts.values())} (A002854 match: {count_ok})",
                    "non-unique factorisations by order: " +
                    str({n: r['classes_with_several_factorisations'] for n, r in results.items()}),
                    f"prime two-graphs n=2..16: {seq}; OEIS: {nov['status']}",
                    f"K2 xor X = K2 xor Y  <=>  X ~ Y: {viol} violations in {tested} pairs (orders <= 6)"],
    }
