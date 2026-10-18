"""Re-time the EXP-C14-07 comparison at nm = 1600 (own code): eigvalsh of the 1600x1600 Seidel+I matrix of a
symmetric-difference product versus the factor route (two 40x40 eigvalsh + outer product + sort). Median of 5."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gtools import prod
rng = np.random.default_rng(1407)
def rg(n):
    A = (rng.random((n, n)) < 0.5).astype(np.uint8); A = np.triu(A, 1); return A + A.T
G, H = rg(40), rg(40)
P = prod(85, G, H)
M = lambda A: np.ones(A.shape) - 2 * A.astype(float)
def med(f, k=5):
    ts = []
    for _ in range(k):
        t0 = time.perf_counter(); out = f(); ts.append(time.perf_counter() - t0)
    return out, float(np.median(ts))
d, td = med(lambda: np.sort(np.linalg.eigvalsh(M(P))))
f, tf = med(lambda: np.sort(np.outer(np.linalg.eigvalsh(M(G)), np.linalg.eigvalsh(M(H))).ravel()))
res = {'direct_s': round(td, 4), 'factor_s': round(tf, 6), 'speedup': round(td / tf, 1),
       'orders_of_magnitude': round(float(np.log10(td / tf)), 2), 'max_abs_err': float(np.abs(d - f).max())}
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'c14_spectra_timing.json'), 'w'), indent=1)
print(res)
