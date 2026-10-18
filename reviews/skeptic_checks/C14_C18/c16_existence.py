"""Extend CLM-C16-10 (full-period quasigroups exist for every n >= 5): own random Latin squares (row-by-row random
perfect matchings via scipy's Hopcroft-Karp on randomly permuted bipartite graphs), orders 17..26, until a
full-period one is found; every hit is re-verified (Latin, single cycle of length n^2, parity)."""
import json, os, sys, time
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c16_checks import cycle_lengths, is_latin, row_sign_product

def rand_latin(n, rng):
    used = np.zeros((n, n), bool); T = np.zeros((n, n), np.int64)
    for r in range(n):
        cp, sp = rng.permutation(n), rng.permutation(n)
        m = maximum_bipartite_matching(csr_matrix((~used[np.ix_(cp, sp)]).astype(np.int8)), perm_type='column')
        for i in range(n):
            T[r, cp[i]] = sp[m[i]]; used[cp[i], sp[m[i]]] = True
    return T

def orbit00(T):
    n = T.shape[0]; a = b = 0
    for k in range(1, n * n + 1):
        a, b = b, int(T[b, a])
        if a == 0 and b == 0:
            return k
    return None

rng = np.random.default_rng(2610)
out = {}
t0 = time.time()
for n in range(17, 27):
    tries = 0
    while True:
        tries += 1
        T = rand_latin(n, rng)
        if orbit00(T) == n * n:
            cl = cycle_lengths(T)
            out[n] = {'samples_until_hit': tries, 'latin': is_latin(T), 'single_cycle': cl == [n * n],
                      'parity_ok': row_sign_product(T) == (-1) ** ((n - 1) * (n + 2) // 2), 'table': T.tolist()}
            break
        if tries > 20000:
            out[n] = {'samples_until_hit': None}
            break
    print(n, {k: v for k, v in out[n].items() if k != 'table'}, round(time.time() - t0, 1), flush=True)
json.dump({str(k): v for k, v in out.items()}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'c16_existence.json'), 'w'))
