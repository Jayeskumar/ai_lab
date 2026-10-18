"""Skeptic checks for cycle C14 (local graph products). Own code only (gtools.py); sympy as an algebra library.

usage: python3 c14_checks.py classify|witness|characters|seidel
"""
import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gtools import (CELLS, all_graphs, canon_small, cellset, complement, find_isomorphism, invariant, isomorphic,
                    prod, seidel_plus_I, switch, switching_canon_small, is_connected)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
NAMES = ['EA', 'EN', 'AE', 'AA', 'AN', 'NE', 'NA', 'NN']


def show(code):
    return ' '.join(NAMES[i] for i in range(8) if code >> i & 1) or '-'


def phi(code, r, s):
    if r == 0 and s == 0:
        return 0
    return 1 if (r, s) in cellset(code) else 2


def P3():
    A = np.zeros((3, 3), np.uint8)
    A[0, 1] = A[1, 0] = A[1, 2] = A[2, 1] = 1
    return A


def rand_graph(rng, n, p=0.5):
    A = (rng.random((n, n)) < p).astype(np.uint8)
    A = np.triu(A, 1)
    return (A + A.T).astype(np.uint8)


def code_from_graph_rule(f):
    """Read off the cell set of a product given as a function f(G, H) -> adjacency of G*H on P3 x P3."""
    G = P3()
    M = f(G, G)
    pick = {0: (0, 0), 1: (0, 1), 2: (0, 2)}     # E, A, N in P3
    code = 0
    for i, (r, s) in enumerate(CELLS):
        (g, g2), (h, h2) = pick[r], pick[s]
        if M[g * 3 + h, g2 * 3 + h2]:
            code |= 1 << i
    return code


# ------------------------------------------------------------------ part classify
def part_classify():
    rel_assoc = [c for c in range(256) if all(phi(c, phi(c, a, b), d) == phi(c, a, phi(c, b, d))
                                              for a, b, d in itertools.product(range(3), repeat=3))]
    comm = [c for c in range(256) if all(phi(c, a, b) == phi(c, b, a) for a, b in itertools.product(range(3), repeat=2))]
    G = P3()
    graph_assoc = [c for c in range(256) if np.array_equal(prod(c, prod(c, G, G), G), prod(c, G, prod(c, G, G)))]
    rng = np.random.default_rng(14)
    tests = [tuple(rand_graph(rng, int(rng.integers(1, 5))) for _ in range(3)) for _ in range(60)]
    random_fail_for_assoc = [c for c in rel_assoc if not all(
        np.array_equal(prod(c, prod(c, a, b), d), prod(c, a, prod(c, b, d))) for a, b, d in tests)]

    def swap_ok(c, A, B):
        n, m = A.shape[0], B.shape[0]
        perm = [h * n + g for g in range(n) for h in range(m)]
        return np.array_equal(prod(c, A, B), prod(c, B, A)[np.ix_(perm, perm)])
    graph_comm = [c for c in range(256) if swap_ok(c, G, G) and all(swap_ok(c, t[0], t[1]) for t in tests)]
    # units by isomorphism (graph level): K1 * X ~ X and X * K1 ~ X for all graphs X with <= 4 vertices
    graphs = all_graphs(4)
    K1 = np.zeros((1, 1), np.uint8)
    smalls = [X for n in range(1, 5) for X in graphs[n]]
    unital = [c for c in rel_assoc if all(canon_small(prod(c, K1, X)) == canon_small(X) and
                                          canon_small(prod(c, X, K1)) == canon_small(X) for X in smalls)]
    # symmetry group, defined at graph level
    transpose = {c: code_from_graph_rule(lambda A, B, c=c: prod(c, B, A)[np.ix_(
        [h * A.shape[0] + g for g in range(A.shape[0]) for h in range(B.shape[0])],
        [h * A.shape[0] + g for g in range(A.shape[0]) for h in range(B.shape[0])])]) for c in range(256)}
    conj = {c: code_from_graph_rule(lambda A, B, c=c: complement(prod(c, complement(A), complement(B))))
            for c in range(256)}
    orbits, seen = [], set()
    for c in range(256):
        if c in seen:
            continue
        orb = {c}
        frontier = [c]
        while frontier:
            x = frontier.pop()
            for y in (transpose[x], conj[x]):
                if y not in orb:
                    orb.add(y)
                    frontier.append(y)
        seen |= orb
        orbits.append(sorted(orb))
    assoc_orbits = [o for o in orbits if set(o) <= set(rel_assoc)]
    mixed = [o for o in orbits if set(o) & set(rel_assoc) and not set(o) <= set(rel_assoc)]

    def depends_first(c):
        S = cellset(c)
        return any(((1, s) in S) != ((2, s) in S) for s in range(3))

    def depends_second(c):
        S = cellset(c)
        return any(((r, 1) in S) != ((r, 2) in S) for r in range(3))
    both = [c for c in rel_assoc if depends_first(c) and depends_second(c)]
    res = {
        'relation_level_associative': rel_assoc, 'n_assoc': len(rel_assoc),
        'graph_level_P3_associative': graph_assoc, 'P3_equals_relation_level': graph_assoc == rel_assoc,
        'assoc_codes_failing_random_graph_triples': random_fail_for_assoc,
        'n_symmetric_S': len(comm), 'graph_level_commutative_equals_symmetric': graph_comm == comm,
        'assoc_and_comm': [c for c in rel_assoc if c in comm],
        'two_sided_unit_K1_by_isomorphism': unital, 'unital_named': [show(c) for c in unital],
        'n_orbits': len(orbits), 'assoc_orbits': assoc_orbits, 'orbits_mixing_assoc_and_nonassoc': mixed,
        'assoc_depending_on_both_factors': both, 'of_which_commutative': [c for c in both if c in comm],
        'claimed_list_matches': rel_assoc == [0, 1, 4, 5, 8, 13, 28, 29, 31, 73, 77, 85, 93, 109, 127, 141, 221, 223,
                                              253, 255],
    }
    return res


# ------------------------------------------------------------------ part witness
def degseq_cert(A):
    return int(A.sum()) // 2, tuple(sorted(A.sum(axis=0).tolist()))


def exact_noniso(A, B):
    if degseq_cert(A) != degseq_cert(B):
        return True
    if A.shape[0] <= 8:
        return canon_small(A) != canon_small(B)
    return not isomorphic(A, B)


def part_witness():
    g = all_graphs(3)
    small = [X for n in (1, 2, 3) for X in g[n]]
    rel_assoc = set(c for c in range(256) if all(phi(c, phi(c, a, b), d) == phi(c, a, phi(c, b, d))
                                                 for a, b, d in itertools.product(range(3), repeat=3)))
    comm = set(c for c in range(256) if all(phi(c, a, b) == phi(c, b, a) for a, b in itertools.product(range(3), repeat=2)))
    triples = sorted(itertools.product(range(len(small)), repeat=3),
                     key=lambda t: (np.prod([small[i].shape[0] for i in t]), t))
    pairs = sorted(itertools.product(range(len(small)), repeat=2),
                   key=lambda t: (np.prod([small[i].shape[0] for i in t]), t))
    hist, uncertified_min, no_witness, any_cert_missing = {}, [], [], []
    for c in range(256):
        if c in rel_assoc:
            continue
        minorder, cert_at_min, any_cert = None, False, False
        for t in triples:
            o = int(np.prod([small[i].shape[0] for i in t]))
            if minorder is not None and o > minorder and any_cert:
                break
            X, Y, Z = (small[i] for i in t)
            L = prod(c, prod(c, X, Y), Z)
            R = prod(c, X, prod(c, Y, Z))
            if degseq_cert(L) != degseq_cert(R):
                any_cert = True
                if minorder is None:
                    minorder = o
                if o == minorder:
                    cert_at_min = True
            elif minorder is None and exact_noniso(L, R):
                minorder = o
        if minorder is None:
            no_witness.append(c)
            continue
        hist[minorder] = hist.get(minorder, 0) + 1
        if not cert_at_min:
            uncertified_min.append(c)
        if not any_cert:
            any_cert_missing.append(c)
    chist, c_uncert, c_none = {}, [], []
    for c in range(256):
        if c in comm:
            continue
        found = None
        for t in pairs:
            X, Y = small[t[0]], small[t[1]]
            L, R = prod(c, X, Y), prod(c, Y, X)
            if degseq_cert(L) != degseq_cert(R):
                found = (int(X.shape[0] * Y.shape[0]), True)
                break
            if exact_noniso(L, R):
                found = (int(X.shape[0] * Y.shape[0]), False)
                break
        if found is None:
            c_none.append(c)
        else:
            chist[found[0]] = chist.get(found[0], 0) + 1
            if not found[1]:
                c_uncert.append(c)
    return {'n_non_assoc': 256 - len(rel_assoc), 'assoc_min_witness_order_hist': dict(sorted(hist.items())),
            'assoc_codes_without_witness_le3': no_witness,
            'assoc_codes_whose_minimal_witness_is_not_degree_certified': uncertified_min,
            'assoc_codes_without_any_degree_certified_witness': any_cert_missing,
            'n_non_comm': 256 - len(comm), 'comm_first_witness_order_hist': dict(sorted(chist.items())),
            'comm_codes_without_witness': c_none, 'comm_first_witness_not_degree_certified': c_uncert}


# ------------------------------------------------------------------ part characters
def part_characters():
    import sympy as sp
    cE, cA, cN = sp.symbols('cE cA cN')
    G = P3()

    def Msym(A):
        n = A.shape[0]
        return sp.Matrix(n, n, lambda i, j: cE if i == j else (cA if A[i, j] else cN))
    MG = Msym(G)
    out_mult, out_add = {}, {}
    for c in range(256):
        P = prod(c, G, G)
        lhs = Msym(P)
        # multiplicative: M(G*H) = M(G) (x) M(H) on G = H = P3 (all 9 blocks non-zero)
        rhs = sp.kronecker_product(MG, MG)
        eqs = set(sp.expand(x) for x in (lhs - rhs) if sp.expand(x) != 0)
        sols = sp.solve(list(eqs), [cE, cA, cN], dict=True)
        good = []
        for s in sols:
            v = [sp.simplify(s.get(x, x)) for x in (cE, cA, cN)]
            if sp.simplify(v[1] - v[2]) != 0:
                good.append(tuple(str(x) for x in v))
        if good:
            out_mult[c] = good
        rhs_a = sp.kronecker_product(MG, sp.eye(3)) + sp.kronecker_product(sp.eye(3), MG)
        eqs = set(sp.expand(x) for x in (lhs - rhs_a) if sp.expand(x) != 0)
        sols = sp.solve(list(eqs), [cE, cA, cN], dict=True)
        good = []
        for s in sols:
            v = [sp.simplify(s.get(x, x)) for x in (cE, cA, cN)]
            if sp.simplify(v[1] - v[2]) != 0:
                good.append(tuple(str(x) for x in v))
        if good:
            out_add[c] = good
    # numeric verification on random graphs (orders 1..6), parameter t = 1.7 where free
    rng = np.random.default_rng(141)
    pairs = [(rand_graph(rng, int(rng.integers(1, 7))), rand_graph(rng, int(rng.integers(1, 7)))) for _ in range(40)]

    def Mnum(A, cvec):
        n = A.shape[0]
        I = np.eye(n)
        return cvec[0] * I + cvec[1] * A + cvec[2] * (np.ones((n, n)) - I - A)
    fails = []
    for kind, table in (('mult', out_mult), ('add', out_add)):
        for c, sols in table.items():
            for s in sols:
                cvec = [float(sp.sympify(x).subs({cE: 1.7, cA: 1.7, cN: 1.7})) for x in s]
                for X, Y in pairs:
                    L = Mnum(prod(c, X, Y), cvec)
                    if kind == 'mult':
                        R = np.kron(Mnum(X, cvec), Mnum(Y, cvec))
                    else:
                        R = np.kron(Mnum(X, cvec), np.eye(Y.shape[0])) + np.kron(np.eye(X.shape[0]), Mnum(Y, cvec))
                    if not np.allclose(L, R):
                        fails.append((kind, c, s))
                        break
    comm_assoc = [0, 5, 8, 13, 85, 93, 127, 141, 221, 255]
    return {'multiplicative': {show(c): v for c, v in out_mult.items()},
            'multiplicative_codes': sorted(out_mult), 'additive': {show(c): v for c, v in out_add.items()},
            'additive_codes': sorted(out_add), 'numeric_failures_random_pairs': fails,
            'comm_assoc_without_character': [c for c in comm_assoc if c not in out_mult and c not in out_add],
            'comm_assoc_with_both_kinds': [c for c in comm_assoc if c in out_mult and c in out_add],
            'characters_on_non_comm_assoc_codes': [c for c in set(out_mult) | set(out_add) if c not in comm_assoc]}


# ------------------------------------------------------------------ part seidel
def kab(a, b):
    n = a + b
    A = np.zeros((n, n), np.uint8)
    A[:a, a:] = 1
    A[a:, :a] = 1
    return A


def complete_bipartite_parts(A):
    """If A is complete bipartite K_{p,q} (edgeless allowed: K_{n,0}) return sorted (p, q); else None."""
    n = A.shape[0]
    if A.sum() == 0:
        return (0, n)
    # two-colour by BFS from vertex 0 of each component; complete bipartite => connected unless edgeless
    col = -np.ones(n, int)
    col[0] = 0
    stack = [0]
    while stack:
        v = stack.pop()
        for w in np.nonzero(A[v])[0]:
            if col[w] < 0:
                col[w] = 1 - col[v]
                stack.append(int(w))
    if (col < 0).any():
        return None
    p = int((col == 0).sum())
    q = n - p
    expected = (col[:, None] != col[None, :]).astype(np.uint8)
    return tuple(sorted((p, q))) if np.array_equal(A, expected) else None


def part_seidel():
    XOR = 85
    g = all_graphs(4)
    graphs = [X for n in range(1, 5) for X in g[n]]
    # exact identity S(G xor H) + I = (S(G)+I) (x) (S(H)+I) in integers, all pairs <= 4 vertices + random <= 9
    fails = 0
    rng = np.random.default_rng(1406)
    pairs = [(X, Y) for X in graphs for Y in graphs] + [(rand_graph(rng, int(rng.integers(1, 10))),
                                                          rand_graph(rng, int(rng.integers(1, 10)))) for _ in range(300)]
    for X, Y in pairs:
        if not np.array_equal(seidel_plus_I(prod(XOR, X, Y)), np.kron(seidel_plus_I(X), seidel_plus_I(Y))):
            fails += 1
    # Theorem 7(a)
    bip_fail = []
    for a, b, c, d in itertools.product(range(0, 6), repeat=4):
        if a + b == 0 or c + d == 0:
            continue
        P = prod(XOR, kab(a, b), kab(c, d))
        parts = complete_bipartite_parts(P)
        want = tuple(sorted((a * c + b * d, a * d + b * c)))
        if parts != want:
            bip_fail.append((a, b, c, d, parts, want))
    # Theorem 7(b): explicit isomorphism Pi for K_{a,a} xor X -> K_{a,a} xor X^Z
    absorb_fail = 0
    for _ in range(300):
        a = int(rng.integers(1, 4))
        n = int(rng.integers(1, 8))
        X = rand_graph(rng, n)
        Z = [v for v in range(n) if rng.random() < 0.5]
        K = kab(a, a)
        L = prod(XOR, K, X)
        R = prod(XOR, K, switch(X, Z))
        sigma = list(range(a, 2 * a)) + list(range(a))
        Pi = [(sigma[gv] if x in Z else gv) * n + x for gv in range(2 * a) for x in range(n)]
        Pi = np.array(Pi)
        # vertex (g,x) of R maps to Pi((g,x)) of L: R[u,v] = L[Pi[u], Pi[v]]
        if not np.array_equal(R, L[np.ix_(Pi, Pi)]):
            absorb_fail += 1
    # Theorem 7(c): K2 xor X ~ K2 xor Y iff X, Y switching equivalent; all graphs <= 6 vertices
    g6 = all_graphs(6)
    K2 = kab(1, 1)
    viol_c, tested_classes = [], {}
    for n in range(1, 7):
        by_class = {}
        for X in g6[n]:
            by_class.setdefault(switching_canon_small(X), []).append(X)
        # invariant of K2 xor X must be constant on classes (if-part) and separate classes (only-if part)
        inv_of_class = {}
        for key, members in by_class.items():
            invs = set()
            for X in members:
                invs.add(invariant(prod(XOR, K2, X)))
            if len(invs) != 1:
                # different invariants inside a class would contradict the 'if' part
                viol_c.append(('if-part', n, len(members)))
            inv_of_class[key] = invs
        keys = list(by_class)
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                if inv_of_class[keys[i]] & inv_of_class[keys[j]]:
                    X, Y = by_class[keys[i]][0], by_class[keys[j]][0]
                    if isomorphic(prod(XOR, K2, X), prod(XOR, K2, Y)):
                        viol_c.append(('only-if', n))
        tested_classes[n] = len(by_class)
    # Theorem 8: K2 xor K2 xor K2 and K2 xor K_{1,3}; C4 = K2 xor K2 = K2 xor 2K1; 3K1 xor K23 = K12 xor K14
    K13 = kab(1, 3)
    t8 = {'K2^3 parts': complete_bipartite_parts(prod(XOR, prod(XOR, K2, K2), K2)),
          'K2 xor K13 parts': complete_bipartite_parts(prod(XOR, K2, K13)),
          'iso K2^3 ~ K2xK13': isomorphic(prod(XOR, prod(XOR, K2, K2), K2), prod(XOR, K2, K13)),
          'K2xK2 parts': complete_bipartite_parts(prod(XOR, K2, K2)),
          'K2x2K1 parts': complete_bipartite_parts(prod(XOR, K2, kab(2, 0))),
          '3K1 x K23 parts': complete_bipartite_parts(prod(XOR, kab(3, 0), kab(2, 3))),
          'K12 x K14 parts': complete_bipartite_parts(prod(XOR, kab(1, 2), kab(1, 4))),
          'K13 connected': is_connected(K13)}
    # primality of K13 under xor: products of two order-2 graphs
    order2 = [kab(1, 1), kab(2, 0)]
    prods4 = {canon_small(prod(XOR, a, b)) for a in order2 for b in order2}
    t8['K13 prime (not a product of two order-2 graphs)'] = canon_small(K13) not in prods4
    t8['products of order-2 graphs'] = sorted(prods4)
    return {'seidel_identity_pairs': len(pairs), 'seidel_identity_failures': fails,
            'bipartite_rule_failures': bip_fail[:10], 'n_bipartite_cases': sum(1 for a, b, c, d in itertools.product(range(6), repeat=4) if a + b and c + d),
            'absorption_failures_of_explicit_Pi': absorb_fail, 'thm7c_violations': viol_c,
            'thm7c_switching_classes_tested': tested_classes, 'theorem8': t8}


if __name__ == '__main__':
    part = sys.argv[1]
    t0 = time.time()
    res = {'classify': part_classify, 'witness': part_witness, 'characters': part_characters,
           'seidel': part_seidel}[part]()
    res['runtime_s'] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, f'c14_{part}.json'), 'w') as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps(res, default=str)[:6000])
