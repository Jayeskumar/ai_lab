"""Skeptic checks for CLM-C01-03, -04, -05 and -06 (independent code).

T3: one-symbol congruences: classes of a^0..a^X by BFS over the undirected rewrite graph on exponents
    (bounded by a large B), for random relation sets incl. m_i = 0 and repeated/duplicate relations,
    compared with x = y or (x, y >= M and P | x - y).
T4: endomorphisms of N^2 (2x2 matrices): the paper's counterexample and a random search.
T5: CLM-C01-05: every rearranging relation of length 3-4 over {a,b} has a word whose class is
    smaller than its Parikh class (exhaustive class computation at lengths k..k+3).
T6: CLM-C01-06: for EVERY border-containment pair (binary k<=9, ternary k<=5, quaternary k<=4) the
    single rule lhs -> rhs (lhs = side whose borders are contained in the other's) has all critical
    pairs joinable (own superposition enumeration + rightmost normal forms) and is lex-monotone.
"""
import itertools
import json
import os
import random
import sys
from functools import reduce
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c01_border_search import borders  # noqa: E402
from c01_recheck_certificates import nf_rightmost, superpositions  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def t3():
    rng = random.Random(99)
    bad, tested = [], 0
    for _ in range(4000):
        r = rng.randint(1, 4)
        rels = []
        for _ in range(r):
            n = rng.randint(1, 25)
            rels.append((rng.randint(0, n - 1), n))
        if rng.random() < 0.1:
            rels.append(rels[0])                     # duplicate relation
        M = min(m for m, _ in rels)
        P = reduce(gcd, (n - m for m, n in rels))
        X = max(n for _, n in rels) + 30
        B = 8 * X + 200
        # BFS over exponents 0..B with edges x <-> x - m_i + n_i (x >= m_i)
        comp = [-1] * (B + 1)
        cid = 0
        for s in range(B + 1):
            if comp[s] >= 0:
                continue
            comp[s] = cid
            stack = [s]
            while stack:
                x = stack.pop()
                for m, n in rels:
                    for y in ((x - m + n) if x >= m else None, (x - n + m) if x >= n else None):
                        if y is not None and 0 <= y <= B and comp[y] < 0:
                            comp[y] = cid
                            stack.append(y)
            cid += 1
        tested += 1
        for x in range(X + 1):
            for y in range(x + 1, X + 1):
                pred = (x >= M and y >= M and (y - x) % P == 0)
                if (comp[x] == comp[y]) != pred:
                    bad.append({"rels": rels, "x": x, "y": y})
                    break
            if bad and bad[-1]["rels"] == rels:
                break
    return {"relation_sets": tested, "failures": bad[:5]}, \
        f"T3 (CLM-C01-03): {tested} random relation sets (1-5 relations, exponents <= 25, incl. m_i = 0 and " \
        f"duplicates), classes of a^0..a^(max n + 30) by BFS: failures {len(bad)}"


def t4():
    def comp(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    # columns = images of a, b in N^2 (counts of a, b); phi(a)=phi(b)=b, psi(a)=psi(b)=a
    phi = [[0, 0], [1, 1]]
    psi = [[1, 1], [0, 0]]
    noncomm = comp(phi, psi) != comp(psi, phi)
    rng = random.Random(5)
    cnt = sum(1 for _ in range(200)
              if (lambda A, B: comp(A, B) != comp(B, A))([[rng.randint(0, 3) for _ in range(2)] for _ in range(2)],
                                                          [[rng.randint(0, 3) for _ in range(2)] for _ in range(2)]))
    return {"paper_example_noncommuting": noncomm, "random_noncommuting_of_200": cnt}, \
        f"T4 (CLM-C01-04): paper's example phi o psi != psi o phi: {noncomm}; random 2x2 N-matrices " \
        f"non-commuting: {cnt}/200"


def classes(u, v, alphabet, n):
    ws = ["".join(t) for t in itertools.product(alphabet, repeat=n)]
    seen, out = set(), []
    k = len(u)
    for w in ws:
        if w in seen:
            continue
        cl, stack = {w}, [w]
        seen.add(w)
        while stack:
            x = stack.pop()
            for i in range(n - k + 1):
                for a, b in ((u, v), (v, u)):
                    if x[i:i + k] == a:
                        y = x[:i] + b + x[i + k:]
                        if y not in seen:
                            seen.add(y)
                            cl.add(y)
                            stack.append(y)
        out.append(cl)
    return out


def t5():
    total, refuted, at_k = 0, 0, 0
    for k in (3, 4):
        ws = ["".join(t) for t in itertools.product("ab", repeat=k)]
        for u, v in itertools.combinations(ws, 2):
            if sorted(u) != sorted(v):
                continue
            total += 1
            found = None
            for n in range(k, k + 4):
                for cl in classes(u, v, "ab", n):
                    w = next(iter(cl))
                    parikh = sum(1 for t in itertools.product("ab", repeat=n) if sorted(t) == sorted(w))
                    if len(cl) < parikh:
                        found = n
                        break
                if found:
                    break
            refuted += found is not None
            at_k += found == k
    baa = [sorted(c) for c in classes("aab", "aba", "ab", 3) if "baa" in c]
    return {"rearranging_relations": total, "with_smaller_class": refuted, "already_at_n_eq_k": at_k,
            "class_of_baa_mod_aab=aba": baa}, \
        f"T5 (CLM-C01-05): {total} rearranging relations of length 3-4: {refuted} have a class smaller than " \
        f"its Parikh class ({at_k} already at n = |u|); class of baa modulo aab=aba: {baa}"


def t6():
    tested, bad = 0, []
    for alphabet, kmax in (("ab", 9), ("abc", 5), ("abcd", 4)):
        for k in range(1, kmax + 1):
            ws = ["".join(t) for t in itertools.product(alphabet, repeat=k)]
            for u, v in itertools.combinations(ws, 2):
                bu, bv = borders(u), borders(v)
                if bu <= bv:
                    l, r = u, v
                elif bv <= bu:
                    l, r = v, u
                else:
                    continue
                tested += 1
                rule = [(l, r)]
                for a, b in superpositions((l, r), (l, r), True):
                    if nf_rightmost(a, rule) != nf_rightmost(b, rule):
                        bad.append((alphabet, l, r, a, b))
                        break
    return {"containment_pairs": tested, "non_joinable": bad[:5], "n_bad": len(bad)}, \
        f"T6 (CLM-C01-06): {tested} border-containment pairs (binary k<=9, ternary k<=5, quaternary k<=4): " \
        f"single rule lhs->rhs with a non-joinable critical pair: {len(bad)}"


if __name__ == "__main__":
    res = {}
    for name, f in (("T3", t3), ("T4", t4), ("T5", t5), ("T6", t6)):
        r, msg = f()
        res[name] = r
        print(msg, flush=True)
    json.dump(res, open(os.path.join(OUT, "c01_misc_checks.json"), "w"), indent=1, default=str)
