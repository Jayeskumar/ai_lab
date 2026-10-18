"""Sanity check of the exact switching-equivalence test used in c14_twographs.py (must return True on equivalent pairs)."""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from gtools import switch, switching_equivalent, prod, all_graphs, isomorphic
rng = np.random.default_rng(5)
res = {'random_equivalent_true': 0, 'random_trials': 0, 'product_equivalent_true': 0, 'product_trials': 0, 'nonequiv_false': 0, 'nonequiv_trials': 0}
t0 = time.time()
for _ in range(30):
    n = int(rng.integers(20, 65))
    A = (rng.random((n, n)) < 0.5).astype(np.uint8); A = np.triu(A, 1); A = A + A.T
    Z = [v for v in range(n) if rng.random() < 0.5]; p = rng.permutation(n)
    B = switch(A, Z)[np.ix_(p, p)]
    res['random_trials'] += 1; res['random_equivalent_true'] += switching_equivalent(A, B)
g = all_graphs(7)
for _ in range(30):
    X = g[7][int(rng.integers(len(g[7])))]; Y = g[int(rng.integers(5, 8))][0]
    Y = g[Y.shape[0]][int(rng.integers(len(g[Y.shape[0]])))]
    P = prod(85, X, Y); n = P.shape[0]
    Z = [v for v in range(n) if rng.random() < 0.5]; p = rng.permutation(n)
    Q = switch(P, Z)[np.ix_(p, p)]
    res['product_trials'] += 1; res['product_equivalent_true'] += switching_equivalent(P, Q)
    # a non-equivalent partner: flip one edge (changes the two-graph unless lucky)
    R = Q.copy(); R[0, 1] = R[1, 0] = 1 - R[0, 1]
    res['nonequiv_trials'] += 1; res['nonequiv_false'] += (not switching_equivalent(P, R))
res['runtime_s'] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'sanity_switching.json'), 'w'), indent=1)
print(res)
