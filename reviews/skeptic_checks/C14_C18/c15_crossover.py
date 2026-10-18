"""Timing check of the claim that the lab's affine and fuse fast-forwards 'never lose' to direct simulation.
This times the LAB's implementations (systems/magma_ca.py) because the claim is about them; both sides are
measured the same way (median of 7 runs), unlike EXP-C15-03 (best of 3 for the fast-forward, 1 run for direct)."""
import json, os, sys, time
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, ROOT)
from systems.magma_ca import FUSE, affine_fast_forward, direct, fuse_fast_forward

def med(f, k=7):
    ts = []
    for _ in range(k):
        t0 = time.perf_counter(); f(); ts.append(time.perf_counter() - t0)
    return float(np.median(ts))

rng = np.random.default_rng(3)
out = {}
for L in (256, 1024, 4096):
    row3 = rng.integers(0, 3, L).astype(np.int8)
    T = ((np.arange(3)[:, None] + np.arange(3)[None, :]) % 3).astype(np.int8)
    for t in (1, 5, 10, 20, 50, 100):
        d_aff = med(lambda: direct(T, row3, t))
        f_aff = med(lambda: affine_fast_forward(1, 1, 0, 3, row3, t))
        d_fuse = med(lambda: direct(FUSE, row3, t))
        f_fuse = med(lambda: fuse_fast_forward(row3, t))
        out[f'L={L} t={t}'] = {'affine_speedup': round(d_aff / f_aff, 2), 'fuse_speedup': round(d_fuse / f_fuse, 2)}
        print(L, t, out[f'L={L} t={t}'], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'out', 'c15_crossover.json'), 'w'), indent=1)
