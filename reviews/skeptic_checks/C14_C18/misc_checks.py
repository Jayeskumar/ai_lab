"""Small extra checks: CLM-C14-11 example, the classical 63-vertex Cartesian/strong collision (EXP-C14-04),
and the CLM-C16-17 facts (lowest-bit period 3, low-byte non-uniformity of x_{k+1} = x_k + x_{k-1} + 1 mod 2^32)."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gtools import prod, isomorphic, canon_small
out = {}
def du(*Gs):
    n = sum(G.shape[0] for G in Gs); A = np.zeros((n, n), np.uint8); i = 0
    for G in Gs:
        k = G.shape[0]; A[i:i + k, i:i + k] = G; i += k
    return A
K = lambda n: (np.ones((n, n), np.uint8) - np.eye(n, dtype=np.uint8))
E = lambda n: np.zeros((n, n), np.uint8)
C4 = np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]], np.uint8)
LEX = 29
L = prod(LEX, E(2), du(C4, E(1)))
R = prod(LEX, du(K(2), K(2), E(1)), E(2))
T = du(C4, C4, E(2))
out['C14-11: 2K1[C4+K1] ~ 2C4+2K1'] = isomorphic(L, T)
out['C14-11: (2K2+K1)[2K1] ~ 2C4+2K1'] = isomorphic(R, T)
def cube(code, k):
    G = E(1)
    for _ in range(k):
        G = prod(code, G, K(2))
    return G
for code, name in ((5, 'cartesian'), (13, 'strong')):
    Q = {k: cube(code, k) for k in range(5)}
    a = du(Q[0], Q[1], Q[2]); b = du(Q[0], Q[3]); c = du(Q[0], Q[2], Q[4]); d = du(Q[0], Q[1])
    out[f'63-vertex collision {name}'] = isomorphic(prod(code, a, b), prod(code, c, d))
M = (1 << 32) - 1
a, b = 12345, 67890
lows, bits0 = np.zeros(1 << 18, np.int64), []
for i in range(1 << 18):
    a, b = b, (a + b + 1) & M
    lows[i] = b & 255
    bits0.append(b & 1)
counts = np.bincount(lows, minlength=256)
out['C16-17: lowest bit period'] = next(p for p in range(1, 50) if bits0[p:p + 1000] == bits0[:1000])
out['C16-17: low-byte chi2 (df 255, 2^18 outputs)'] = float(((counts - counts.mean()) ** 2 / counts.mean()).sum())
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'misc_checks.json'), 'w'), indent=1)
print(out)
