"""Skeptic's independent factorisation census for the eight unital associative local products (CLM-C14-08..12).

Own graph generation (all graphs <= 7 vertices, exact canonical forms), own products, own isomorphism classes
(exact canonical forms for <= 8 vertices; invariant buckets + own backtracking isomorphism above).
Totals A000088 / A001349 and the reference A129582 are read from the OEIS cache files (data only).

usage: python3 c14_census.py [codes...]      (default: all eight)
"""
import glob
import itertools
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gtools import Registry, all_graphs, canon_small, cellset, is_connected, prod, find_isomorphism

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
UNITAL = [5, 13, 29, 77, 85, 93, 141, 221]
ORDERS = [4, 6, 8, 9, 10, 12, 14, 15]


def oeis(anum):
    for f in glob.glob(os.path.join(ROOT, 'cache', 'oeis', '*.json')):
        d = json.load(open(f))
        if d.get('query') == f'id:{anum}':
            r = d['response']
            r = r if isinstance(r, list) else r.get('results')
            off = int(str(r[0]['offset']).split(',')[0])
            return {off + i: int(x) for i, x in enumerate(r[0]['data'].split(','))}
    raise KeyError(anum)


def is_comm(code):
    S = cellset(code)
    return all(((r, s) in S) == ((s, r) in S) for r in range(3) for s in range(3) if (r, s) != (0, 0))


def shapes(n, orders):
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


def census(code, graphs, connected_only):
    comm = is_comm(code)
    pool = {n: [G for G in graphs[n] if (not connected_only or is_connected(G))] for n in graphs}
    primes = {}
    for n in range(2, 8):
        if n in (4, 6):
            comp = set()
            for a in range(2, n):
                if n % a:
                    continue
                for X in pool[a]:
                    for Y in pool[n // a]:
                        P = prod(code, X, Y)
                        if connected_only and not is_connected(P):
                            continue
                        comp.add(canon_small(P))
            primes[n] = [G for G in pool[n] if canon_small(G) not in comp]
        else:
            primes[n] = list(pool[n])
    res = {}
    for n in ORDERS:
        reg = Registry()
        facts = {}
        for sh in shapes(n, primes):
            if comm:
                groups = [(d, len(list(g))) for d, g in itertools.groupby(sh)]
                seqs = []
                for combo in itertools.product(*[itertools.combinations_with_replacement(range(len(primes[d])), k)
                                                 for d, k in groups]):
                    seq = []
                    for (d, _), cmb in zip(groups, combo):
                        seq += [(d, i) for i in cmb]
                    seqs.append(tuple(seq))
            else:
                seqs = []
                for perm in sorted(set(itertools.permutations(sh))):
                    for idx in itertools.product(*[range(len(primes[d])) for d in perm]):
                        seqs.append(tuple(zip(perm, idx)))
            for seq in seqs:
                P = primes[seq[0][0]][seq[0][1]]
                for d, i in seq[1:]:
                    P = prod(code, P, primes[d][i])
                if connected_only and not is_connected(P):
                    continue
                key = canon_small(P) if n <= 8 else reg.add(P)
                facts.setdefault(key, []).append(seq)
        several = sum(1 for f in facts.values() if len(f) > 1)
        several_ms = sum(1 for f in facts.values() if len({tuple(sorted(s)) for s in f}) > 1)
        res[n] = {'factorisations': sum(len(f) for f in facts.values()), 'composite_classes': len(facts),
                  'several_factorisations': several, 'several_multisets': several_ms}
    return res, {n: len(v) for n, v in primes.items()}


def main(codes):
    t0 = time.time()
    graphs = all_graphs(7)
    A88, A1349, A129582 = oeis('A000088'), oeis('A001349'), oeis('A129582')
    lab = json.load(open(os.path.join(ROOT, 'results', 'EXP-C14-04.json')))['results']['products']
    lab_by_code = {v['code']: v for v in lab.values()}
    out = {}
    for code in codes:
        r_all, p_all = census(code, graphs, False)
        r_conn, p_conn = census(code, graphs, True)
        primes_all = {n: (p_all[n] if n <= 7 else A88[n] - (r_all[n]['composite_classes'] if n in r_all else 0))
                      for n in range(2, 16)}
        primes_conn = {n: (p_conn[n] if n <= 7 else A1349[n] - (r_conn[n]['composite_classes'] if n in r_conn else 0))
                       for n in range(2, 16)}
        L = lab_by_code[code]
        agree_all = all(L['all_graphs'][str(n)]['composite_classes'] == r_all[n]['composite_classes'] and
                        L['all_graphs'][str(n)]['factorisations'] == r_all[n]['factorisations'] and
                        L['all_graphs'][str(n)]['classes_with_several_factorisations'] == r_all[n]['several_factorisations'] and
                        L['all_graphs'][str(n)]['classes_with_several_factor_multisets'] == r_all[n]['several_multisets']
                        for n in ORDERS)
        agree_conn = all(L['connected'][str(n)]['composite_classes'] == r_conn[n]['composite_classes'] and
                         L['connected'][str(n)]['classes_with_several_factor_multisets'] == r_conn[n]['several_multisets']
                         for n in ORDERS)
        agree_primes = all(int(L['primes_all_graphs'][str(n)]) == primes_all[n] for n in range(2, 16))
        out[code] = {'all': r_all, 'connected': r_conn, 'primes_all_graphs': primes_all,
                     'primes_connected': primes_conn, 'agrees_with_lab_all': agree_all,
                     'agrees_with_lab_connected': agree_conn, 'agrees_with_lab_prime_counts': agree_primes}
        if code in (5, 13):
            out[code]['connected_primes_equal_A129582_n2_15'] = all(primes_conn[n] == A129582[n] for n in range(2, 16))
        print(code, 'all', {n: (v['composite_classes'], v['several_multisets']) for n, v in r_all.items()},
              'conn', {n: (v['composite_classes'], v['several_multisets']) for n, v in r_conn.items()},
              'lab-agree', agree_all, agree_conn, agree_primes, round(time.time() - t0, 1), flush=True)
    out['runtime_s'] = round(time.time() - t0, 1)
    return out


if __name__ == '__main__':
    codes = [int(x) for x in sys.argv[1:]] or UNITAL
    res = main(codes)
    tag = '_'.join(map(str, codes)) if sys.argv[1:] else 'all'
    with open(os.path.join(OUT, f'c14_census_{tag}.json'), 'w') as f:
        json.dump(res, f, indent=1, default=str)
