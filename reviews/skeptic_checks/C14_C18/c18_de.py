"""CLM-C18-01: own d-transformation inverts own e-transformation (forward and reversed passes) for 5 quasigroups."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c18_checks import niminv_qg, random_latin, iso_z256, arp, aff, xorq, etr
def dtr(T, Y, leader):
    ld = np.zeros((256, 256), np.uint8)
    for u in range(256):
        ld[u, T[u]] = np.arange(256, dtype=np.uint8)
    out = np.empty_like(Y); prev = np.full(Y.shape[0], leader, np.uint8)
    for i in range(Y.shape[1]):
        out[:, i] = ld[prev, Y[:, i]]; prev = Y[:, i]
    return out
rng = np.random.default_rng(77)
res = {}
for name, T in {'LS': random_latin(5), 'ISO': iso_z256(6), 'NIMINV': niminv_qg(), 'ARP': arp(7), 'AFF': aff(), 'XOR': xorq()}.items():
    X = rng.integers(0, 256, (3000, 23), dtype=np.uint8)
    Y = etr(T, etr(T, X, 0x11)[:, ::-1].copy(), 0x99)          # forward, then reversed pass
    Z = dtr(T, dtr(T, Y, 0x99)[:, ::-1].copy(), 0x11)
    res[name] = int((Z != X).any(1).sum())
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'c18_de.json'), 'w'))
print('strings not recovered:', res)
