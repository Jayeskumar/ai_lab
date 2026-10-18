"""EXP-C14-06: Skeptic's independent re-implementation and re-check of the C14 claims."""

import itertools
import random

META = {
    "id": "EXP-C14-06",
    "cycle": "C14",
    "title": "Independent re-verification of the C14 claims (pure Python, no shared library code)",
    "agent": "Mathematical Skeptic",
    "question": "Do the classification, the non-isomorphism witnesses, the XOR identities and the explicit "
                "non-unique factorisations survive an implementation that shares no code with systems/graph_products.py?",
    "hypothesis": "All C14 computational claims are reproduced; any disagreement is a bug in one implementation.",
    "assumptions": ["graphs as Python sets of frozenset edges on range(n); products built from the definition",
                    "isomorphism of small graphs by exhaustive permutation search (n <= 8); the bipartite formula "
                    "checked edge by edge (sign-vector description) for a, b, c, d <= 4"],
    "methodology": "Re-implement local products from the definition; recount associative/commutative codes with "
                   "random and P3 triples; re-check the 236/224 witnesses' degree sequences (witness list read from "
                   "EXP-C14-02); verify K2+K2+K2 = K2+K_{1,3} (XOR) by an explicit isomorphism; verify "
                   "K_{a,b} xor K_{c,d} = K_{ac+bd, ad+bc}; verify the Seidel identity exactly in integers for all "
                   "pairs of graphs with <= 3 vertices; verify K2 xor X = K2 xor (X switched) on 200 random cases.",
    "falsification": "Any mismatch.",
    "seed": 1406,
}

E, A, N = 0, 1, 2
CELLS = [(a, b) for a in range(3) for b in range(3) if (a, b) != (0, 0)]


def rel(G, x, y):
    if x == y:
        return E
    return A if frozenset((x, y)) in G[1] else N


def prod(code, G, H):
    S = {c for i, c in enumerate(CELLS) if code >> i & 1}
    n, m = G[0], H[0]
    V = [(g, h) for g in range(n) for h in range(m)]
    idx = {v: i for i, v in enumerate(V)}
    edges = set()
    for (g, h), (g2, h2) in itertools.combinations(V, 2):
        if (rel(G, g, g2), rel(H, h, h2)) in S:
            edges.add(frozenset((idx[(g, h)], idx[(g2, h2)])))
    return (n * m, edges)


def graph(n, edges):
    return (n, {frozenset(e) for e in edges})


def degseq(G):
    d = [0] * G[0]
    for e in G[1]:
        for v in e:
            d[v] += 1
    return len(G[1]), tuple(sorted(d))


def iso_bruteforce(G, H):
    if G[0] != H[0] or degseq(G) != degseq(H):
        return None
    n = G[0]
    for p in itertools.permutations(range(n)):
        if all(frozenset((p[a], p[b])) in H[1] for a, b in map(tuple, G[1])):
            return p
    return None


def assoc_graph(code, G, H, K):
    # canonical map ((g,h),k) -> (g,(h,k)) is the identity on indices g|H||K| + h|K| + k
    return prod(code, prod(code, G, H), K)[1] == prod(code, G, prod(code, H, K))[1]


def comp_bip(a, b):
    n = a + b
    return graph(n, [(i, j) for i in range(a) for j in range(a, n)])


def seidel_int(G):
    n = G[0]
    return [[0 if i == j else (-1 if frozenset((i, j)) in G[1] else 1) for j in range(n)] for i in range(n)]


def switch(G, Z):
    n = G[0]
    edges = set()
    for i, j in itertools.combinations(range(n), 2):
        e = frozenset((i, j)) in G[1]
        if (i in Z) != (j in Z):
            e = not e
        if e:
            edges.add(frozenset((i, j)))
    return (n, edges)


def run():
    import json
    from lab.paths import RESULTS
    rng = random.Random(META["seed"])
    P3 = graph(3, [(0, 1), (1, 2)])
    small = [graph(1, []), graph(2, []), graph(2, [(0, 1)]), graph(3, []), graph(3, [(0, 1)]), P3,
             graph(3, [(0, 1), (1, 2), (0, 2)])]
    names = ["K1", "2K1", "K2", "3K1", "K2+K1", "P3", "K3"]
    rand = [graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.5])
            for n in (rng.randint(1, 3) for _ in range(30))]
    assoc = [c for c in range(256) if assoc_graph(c, P3, P3, P3) and
             all(assoc_graph(c, *rng.sample(rand, 3)) for _ in range(10))]
    comm = []
    for c in assoc:
        ok = True
        for G, H in [(P3, P3)] + [tuple(rng.sample(rand, 2)) for _ in range(10)]:
            n, m = G[0], H[0]
            GH, HG = prod(c, G, H), prod(c, H, G)
            perm = [h * n + g for g in range(n) for h in range(m)]
            if {frozenset(perm[v] for v in e) for e in GH[1]} != HG[1]:
                ok = False
        if ok:
            comm.append(c)
    # witnesses from EXP-C14-02
    w = json.loads((RESULTS / "EXP-C14-02.json").read_text())["results"]
    by = dict(zip(names, small))
    bad_a = [c for c, t in w["assoc_witnesses"].items()
             if degseq(prod(int(c), prod(int(c), by[t[0]], by[t[1]]), by[t[2]])) ==
             degseq(prod(int(c), by[t[0]], prod(int(c), by[t[1]], by[t[2]])))]
    bad_c = [c for c, t in w["comm_witnesses"].items()
             if degseq(prod(int(c), by[t[0]], by[t[1]])) == degseq(prod(int(c), by[t[1]], by[t[0]]))]
    XOR = 85
    K2 = graph(2, [(0, 1)])
    claw = graph(4, [(0, 3), (1, 3), (2, 3)])
    lhs = prod(XOR, prod(XOR, K2, K2), K2)
    rhs = prod(XOR, K2, claw)
    iso8 = iso_bruteforce(lhs, rhs)
    c4_a = prod(XOR, K2, K2)
    c4_b = prod(XOR, K2, graph(2, []))
    iso4 = iso_bruteforce(c4_a, c4_b)
    bip_fail = []
    for a, b, c, d in itertools.product(range(5), repeat=4):
        if a + b == 0 or c + d == 0:
            continue
        P = prod(XOR, comp_bip(a, b), comp_bip(c, d))
        # exact check: (g,h) ~ (g',h') iff the sign products differ, and ac + bd vertices have sign +1
        m = c + d
        sign = [(1 if v // m < a else -1) * (1 if v % m < c else -1) for v in range(P[0])]
        expected = {frozenset((u, v)) for u, v in itertools.combinations(range(P[0]), 2) if sign[u] != sign[v]}
        if P[1] != expected or sign.count(1) != a * c + b * d:
            bip_fail.append((a, b, c, d))
    # Seidel identity S(G xor H) + I = (S(G) + I) (x) (S(H) + I), exactly in integers
    seid_fail = 0
    for G in small:
        for H in small:
            SP = seidel_int(prod(XOR, G, H))
            SG, SH = seidel_int(G), seidel_int(H)
            m = H[0]
            for i in range(G[0] * m):
                for j in range(G[0] * m):
                    lhs_ij = SP[i][j] + (i == j)
                    rhs_ij = (SG[i // m][j // m] + (i // m == j // m)) * (SH[i % m][j % m] + (i % m == j % m))
                    seid_fail += lhs_ij != rhs_ij
    # switching absorbed by K2
    absorb_fail = 0
    for _ in range(200):
        n = rng.randint(2, 4)
        X = graph(n, [e for e in itertools.combinations(range(n), 2) if rng.random() < 0.5])
        Z = {v for v in range(n) if rng.random() < 0.5}
        absorb_fail += iso_bruteforce(prod(XOR, K2, X), prod(XOR, K2, switch(X, Z))) is None
    return {
        "associative_codes": assoc,
        "n_associative": len(assoc),
        "commutative_associative_codes": comm,
        "witness_failures_assoc": bad_a,
        "witness_failures_comm": bad_c,
        "xor_K2K2K2_iso_K2_claw": iso8 is not None,
        "xor_C4_two_factorisations": iso4 is not None,
        "bipartite_formula_failures": bip_fail,
        "seidel_identity_entry_failures": seid_fail,
        "k2_switching_absorption_failures": absorb_fail,
        "summary": [f"independent recount: {len(assoc)} associative, {len(comm)} commutative",
                    f"witness re-checks failing: assoc {len(bad_a)}, comm {len(bad_c)}",
                    f"K2 xor K2 xor K2 = K2 xor K_1,3: {iso8 is not None}; K2 xor K2 = K2 xor 2K1: {iso4 is not None}",
                    f"K_ab xor K_cd = K_(ac+bd, ad+bc) failures: {len(bip_fail)}; Seidel identity entry failures: "
                    f"{seid_fail}; K2-absorption failures: {absorb_fail}/200"],
    }
