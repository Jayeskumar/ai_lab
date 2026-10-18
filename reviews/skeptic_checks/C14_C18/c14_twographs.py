"""Skeptic check of CLM-C14-13 (two-graphs factor uniquely under the symmetric-difference / Kronecker product).

1. Own switching classes for n <= 8 (exact canonical forms via descendants), compared with A002854.
2. Composite and prime classes of order <= 8.
3. Exact re-check of the lab's orders 4..16.
4. Extension: every multiset of prime classes (each of order <= 8) with product order N <= NMAX is screened by the
   multiset of eigenvalues of S + I (which is multiplicative). Two different multisets can only give the same class if
   these spectra coincide; coincidences are then separated by a finer switching invariant (spectra of all
   descendants) and, if still equal, decided exactly (descendant isomorphism with own backtracking).

usage: python3 c14_twographs.py NMAX
"""
import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gtools import (all_graphs, canon_small, from_canon, isolate, prod, switching_canon_small, switching_equivalent,
                    switching_invariant)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
XOR = 85


def spec(A):
    n = A.shape[0]
    M = np.ones((n, n)) - 2 * A.astype(np.float64)
    return np.sort(np.linalg.eigvalsh(M))


def key_of(vals, nd=5):
    return tuple(np.round(np.sort(vals), nd) + 0.0)


def main(NMAX):
    t0 = time.time()
    g = all_graphs(7)
    classes = {1: [np.zeros((1, 1), np.uint8)]}
    for n in range(2, 8):
        reps = {}
        for A in g[n]:
            k = switching_canon_small(A)
            reps.setdefault(k, A)
        classes[n] = [reps[k] for k in sorted(reps)]
    reps = {}
    for A7 in g[7]:
        A = np.zeros((8, 8), np.uint8)
        A[1:, 1:] = A7
        k = switching_canon_small(A)
        reps.setdefault(k, A)
    classes[8] = [reps[k] for k in sorted(reps)]
    counts = {n: len(v) for n, v in classes.items()}
    print('class counts', counts, round(time.time() - t0, 1), flush=True)
    ckey = {n: [switching_canon_small(A) for A in classes[n]] for n in classes}
    composite = {}
    for n in (4, 6, 8):
        comp = set()
        for a in range(2, n):
            if n % a or n // a < 2:
                continue
            for X in classes[a]:
                for Y in classes[n // a]:
                    comp.add(switching_canon_small(prod(XOR, X, Y)))
        composite[n] = comp
    primes = {n: [A for A, k in zip(classes[n], ckey[n]) if not (n in composite and k in composite[n])]
              for n in range(2, 9)}
    pcount = {n: len(v) for n, v in primes.items()}
    print('prime counts', pcount, round(time.time() - t0, 1), flush=True)
    # exact integer power sums p_k = tr((S+I)^k), k = 1..NMAX; they are multiplicative under the Kronecker product
    def powsums(A):
        n = A.shape[0]
        M = [[1 - 2 * int(A[i, j]) if i != j else 1 for j in range(n)] for i in range(n)]
        P = [row[:] for row in M]
        out = []
        for k in range(1, NMAX + 1):
            out.append(sum(P[i][i] for i in range(n)))
            P = [[sum(P[i][l] * M[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        return out
    psum = {n: [powsums(A) for A in primes[n]] for n in primes}

    # enumerate multisets of primes with product order N <= NMAX
    items = [(n, i) for n in range(2, 9) for i in range(len(primes[n]))]

    def multisets(N, start):
        """multisets (non-decreasing in items order) of items whose orders multiply to N"""
        if N == 1:
            yield ()
            return
        for idx in range(start, len(items)):
            n, i = items[idx]
            if N % n == 0:
                for rest in multisets(N // n, idx):
                    yield (items[idx],) + rest

    report = {'class_counts_n1_8': counts, 'prime_counts_n2_8': pcount, 'orders': {}}
    total_ms, total_candidates, total_exact = 0, 0, 0
    collisions = []
    for N in range(4, NMAX + 1):
        ms = [m for m in multisets(N, 0) if len(m) >= 2]
        if not ms:
            continue
        buckets = {}
        for m in ms:
            v = [1] * N
            for (n, i) in m:
                v = [a * b for a, b in zip(v, psum[n][i][:N])]
            buckets.setdefault(tuple(v), []).append(m)
        cand_groups = [b for b in buckets.values() if len(b) > 1]
        n_exact = 0
        for grp in cand_groups:
            # build the product graphs and separate by the descendant-spectra invariant
            graphs = []
            for m in grp:
                P = primes[m[0][0]][m[0][1]]
                for (n, i) in m[1:]:
                    P = prod(XOR, P, primes[n][i])
                graphs.append(P)
            if N <= 9:
                keys = [switching_canon_small(P) for P in graphs]
                byk = {}
                for k, m in zip(keys, grp):
                    byk.setdefault(k, []).append(m)
                for k, lst in byk.items():
                    if len(lst) > 1:
                        collisions.append((N, lst))
                continue
            sub = {0: list(zip(graphs, grp))} if len(grp) <= 6 else {}
            if len(grp) > 6:   # many candidates: separate by the (float) descendant-spectra invariant first
                for P, m in zip(graphs, grp):
                    sub.setdefault(switching_invariant(P), []).append((P, m))
            for lst in sub.values():
                if len(lst) < 2:
                    continue
                # exact pairwise decisions
                for a in range(len(lst)):
                    for b in range(a + 1, len(lst)):
                        n_exact += 1
                        if switching_equivalent(lst[a][0], lst[b][0]):
                            collisions.append((N, [lst[a][1], lst[b][1]]))
        report['orders'][N] = {'multisets': len(ms), 'spectral_classes': len(buckets),
                               'spectral_coincidence_groups': len(cand_groups),
                               'multisets_in_coincidence_groups': sum(len(b) for b in cand_groups),
                               'exact_tests': n_exact}
        total_ms += len(ms)
        total_candidates += sum(len(b) for b in cand_groups)
        total_exact += n_exact
        if cand_groups or N % 8 == 0:
            print(N, report['orders'][N], 'collisions so far', len(collisions), round(time.time() - t0, 1), flush=True)
    report['total_multisets'] = total_ms
    report['total_in_coincidence_groups'] = total_candidates
    report['total_exact_tests'] = total_exact
    report['collisions'] = [(N, [[list(x) for x in m] for m in lst]) for N, lst in collisions]
    report['runtime_s'] = round(time.time() - t0, 1)
    return report


if __name__ == '__main__':
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    rep = main(NMAX)
    with open(os.path.join(OUT, f'c14_twographs_{NMAX}.json'), 'w') as f:
        json.dump(rep, f, indent=1, default=str)
    print('collisions:', rep['collisions'][:5], 'multisets', rep['total_multisets'], 'runtime', rep['runtime_s'])
