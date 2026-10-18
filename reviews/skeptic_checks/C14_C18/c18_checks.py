"""Skeptic checks for cycle C18 (quasigroup hashes). Own implementations of every hash and quasigroup
(nim-multiplication from Conway's mex definition, nim_mex.c); hashlib for BLAKE2b; scipy only as a matching solver.
Leaders differ from the lab's on purpose (the claims do not depend on them).

usage: python3 c18_checks.py structure|tailbound|avalanche|noise|distribution
"""
import hashlib
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
LEAD = (0x11, 0x99, 0x37, 0xE1, 0x05, 0x6D, 0xAB, 0x42)
REVL = 0x7E


# ------------------------------------------------------------------ quasigroups (own)
def nim_table():
    return np.fromfile(os.path.join(OUT, 'nim256_mex.bin'), dtype=np.uint8).reshape(256, 256)


def niminv_qg():
    P = nim_table().astype(np.int64)
    inv = np.zeros(256, np.int64)
    for a in range(1, 256):
        inv[a] = int(np.nonzero(P[a] == 1)[0][0])
    x = np.arange(256)
    return inv[x[:, None] ^ x[None, :]].astype(np.uint8)


def random_latin(seed):
    """Own row-by-row construction: each row is a perfect matching column -> unused symbol, found by scipy's
    Hopcroft-Karp on a randomly permuted bipartite graph (not uniform)."""
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import maximum_bipartite_matching
    rng = np.random.default_rng(seed)
    used = np.zeros((256, 256), bool)
    T = np.zeros((256, 256), np.uint8)
    for r in range(256):
        cperm, sperm = rng.permutation(256), rng.permutation(256)
        G = csr_matrix((~used[np.ix_(cperm, sperm)]).astype(np.int8))
        m = maximum_bipartite_matching(G, perm_type='column')
        assert (m >= 0).all()
        for i in range(256):
            c, s = cperm[i], sperm[m[i]]
            T[r, c] = s
            used[c, s] = True
    return T


def iso_z256(seed):
    rng = np.random.default_rng(seed)
    a, b, c = rng.permutation(256), rng.permutation(256), rng.permutation(256)
    return a[(b[:, None] + c[None, :]) % 256].astype(np.uint8)


def arp(seed):
    rng = np.random.default_rng(seed)
    c = np.concatenate([[1], rng.permutation([v for v in range(256) if v != 1])])
    x = np.arange(256)
    return ((x[:, None] + c[None, :]) % 256).astype(np.uint8)


def aff():
    x = np.arange(256)
    return ((77 * x[:, None] + 141 * x[None, :] + 5) % 256).astype(np.uint8)


def xorq():
    x = np.arange(256)
    return (x[:, None] ^ x[None, :]).astype(np.uint8)


def is_latin(T):
    r = np.arange(256)
    return bool((np.sort(T, 1) == r).all() and (np.sort(T, 0) == r[:, None]).all())


# ------------------------------------------------------------------ hashes (own)
def message(X):
    n, L = X.shape
    M = np.zeros((n, max(L + 1, 8)), np.uint8)
    M[:, :L] = X
    M[:, L] = L % 256
    return M


def etr(T, M, leader):
    out = np.empty_like(M)
    s = np.full(M.shape[0], leader, np.uint8)
    for i in range(M.shape[1]):
        s = T[s, M[:, i]]
        out[:, i] = s
    return out


def tail64(Y):
    h = np.zeros(Y.shape[0], np.uint64)
    for j in range(8):
        h = (h << np.uint64(8)) | Y[:, -8 + j].astype(np.uint64)
    return h


def qg(T, X, passes, rev):
    Y = message(X)
    for p in range(passes):
        Y = etr(T, Y, LEAD[p])
    if rev:
        Y = etr(T, np.ascontiguousarray(Y[:, ::-1]), REVL)
    return tail64(Y)


def qc(T, X, depth=8, final=8):
    n, L = X.shape
    M = np.zeros((n, L + 1 + final), np.uint8)
    M[:, :L] = X
    M[:, L] = L % 256
    s = [np.full(n, LEAD[j % 8], np.uint8) for j in range(depth)]
    for i in range(M.shape[1]):
        x = M[:, i]
        for j in range(depth):
            s[j] = T[s[j], x]
            x = s[j]
    h = np.zeros(n, np.uint64)
    for j in range(depth):
        h = (h << np.uint64(8)) | s[j].astype(np.uint64)
    return h


def fnv1a(X):
    h = np.full(X.shape[0], 0xCBF29CE484222325, np.uint64)
    with np.errstate(over='ignore'):
        for i in range(X.shape[1]):
            h = (h ^ X[:, i].astype(np.uint64)) * np.uint64(0x100000001B3)
    return h


def mx64(X):
    h = np.zeros(X.shape[0], np.uint64)
    with np.errstate(over='ignore'):
        for i in range(X.shape[1]):
            h = (h ^ X[:, i].astype(np.uint64)) * np.uint64(0x9E3779B97F4A7C15)
            h ^= h >> np.uint64(32)
        z = h ^ np.uint64(X.shape[1])
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        return z ^ (z >> np.uint64(31))


def blake(X):
    return np.array([int.from_bytes(hashlib.blake2b(bytes(r), digest_size=8).digest(), 'big') for r in X], np.uint64)


def bits(h):
    return ((h[:, None] >> np.arange(64, dtype=np.uint64)[None, :]) & np.uint64(1)).astype(np.uint8)


def avalanche(fn, X):
    base = fn(X)
    L = X.shape[1]
    P = np.zeros((8 * L, 64))
    bic = 0.0
    for i in range(8 * L):
        Xf = X.copy()
        Xf[:, i // 8] ^= np.uint8(1 << (i % 8))
        d = bits(base ^ fn(Xf)).astype(np.float64)
        P[i] = d.mean(0)
        sd = d.std(0)
        ok = sd > 0
        if (~ok).sum() >= 2:
            bic = 1.0
        if ok.sum() >= 2:
            C = np.corrcoef(d[:, ok].T)
            bic = max(bic, float(np.abs(C[~np.eye(C.shape[0], dtype=bool)]).max()))
    bias = np.abs(P - 0.5)
    i, j = np.unravel_index(int(bias.argmax()), bias.shape)
    return {'mean_bias': round(float(bias.mean()), 4), 'max_bias': round(float(bias.max()), 4),
            'argmax_cell(input_bit,output_bit)': [int(i), int(j)], 'cells_gt_0.07': int((bias > 0.07).sum()),
            'cells_gt_0.1': int((bias > 0.1).sum()), 'deterministic': int(((P == 0) | (P == 1)).sum()),
            'bic_max': round(bic, 4)}


def chi2_z(h, m, mode):
    b = (h & np.uint64(m - 1)) if mode == 'mask' else (h % np.uint64(m))
    c = np.bincount(b.astype(np.int64), minlength=m)
    e = len(h) / m
    chi = float(((c - e) ** 2).sum() / e)
    return round((chi - (m - 1)) / np.sqrt(2 * (m - 1)), 2)


def bucket_ratio(h, bitsn=16):
    n = len(h)
    m = 1 << bitsn
    occ = np.unique((h & np.uint64(m - 1)).astype(np.int64)).size
    exp = n - m * (1 - (1 - 1 / m) ** n)
    return round((n - occ) / exp, 4)


# ------------------------------------------------------------------ parts
def part_structure():
    Q = {'NIMINV': niminv_qg(), 'AFF': aff(), 'XOR': xorq(), 'ARP': arp(7), 'ISO': iso_z256(8)}
    P = nim_table()
    out = {'nim_mex_field_checks': {
        'commutative': bool((P == P.T).all()),
        'distributive_over_xor_sample': bool(all(int(P[a, b ^ c]) == int(P[a, b]) ^ int(P[a, c])
                                                 for a, b, c in np.random.default_rng(0).integers(0, 256, (5000, 3)))),
        'nonzero_closed_and_invertible': bool(all((P[a, 1:] != 0).all() and np.unique(P[a, 1:]).size == 255
                                                  for a in range(1, 256)))},
           'latin': {k: is_latin(v) for k, v in Q.items()}}
    rng = np.random.default_rng(181)
    X = rng.integers(0, 256, (2000, 16), dtype=np.uint8)
    # Theorem 4 (T-function, AFF): flipping bit r of an input byte never changes output bits < r of any output byte
    viol = 0
    for r in range(8):
        for pos in range(16):
            Xf = X.copy()
            Xf[:, pos] ^= np.uint8(1 << r)
            d = qg(Q['AFF'], X, 2, True) ^ qg(Q['AFF'], Xf, 2, True)
            low_mask = np.uint64(sum(((1 << r) - 1) << (8 * k) for k in range(8)))
            viol += int(((d & low_mask) != 0).sum())
    out['tfunction_AFF_violations'] = viol
    # Theorem 5 (XOR): one input difference gives one output difference for all keys
    D = np.zeros(16, np.uint8)
    D[3] = 0x5A
    d = qg(Q['XOR'], X, 2, True) ^ qg(Q['XOR'], X ^ D, 2, True)
    out['xor_distinct_output_differences'] = int(np.unique(d).size)
    # Theorem 6: ARP 1-pass tail hash anagram-blind (permute bytes 0..8 of 16-byte keys: message tail = positions 9..16)
    Xp = X.copy()
    for k in range(len(Xp)):
        Xp[k, :9] = Xp[k, rng.permutation(9)]
    changed = int((Xp != X).any(1).sum())
    out['arp_1pass_unchanged_under_prefix_permutation'] = int((qg(Q['ARP'], X, 1, False) == qg(Q['ARP'], Xp, 1, False)).sum())
    out['arp_keys_actually_changed'] = changed
    # Theorem 6 consequence: ARP p2+rev, change a byte at position >= 8: all 8 output bytes shift by one constant (mod 256)
    Xc = X.copy()
    Xc[:, 12] ^= np.uint8(0x21)
    h1, h2 = qg(Q['ARP'], X, 2, True), qg(Q['ARP'], Xc, 2, True)
    b1 = np.stack([(h1 >> np.uint64(8 * k)) & np.uint64(255) for k in range(8)], 1).astype(np.int64)
    b2 = np.stack([(h2 >> np.uint64(8 * k)) & np.uint64(255) for k in range(8)], 1).astype(np.int64)
    diffs = (b2 - b1) % 256
    out['arp_p2rev_common_additive_shift_fraction'] = float((diffs == diffs[:, :1]).all(1).mean())
    return out


def near_duplicates(rng, families=16):
    keys = []
    for _ in range(families):
        base = rng.integers(0, 256, 16, dtype=np.uint8)
        for pos in range(16):
            for v in range(256):
                if v != base[pos]:
                    k = base.copy()
                    k[pos] = v
                    keys.append(k)
    return np.array(keys, np.uint8)


def part_tailbound():
    Q = {'LS': random_latin(2026), 'ISO': iso_z256(9), 'NIMINV': niminv_qg(), 'ARP': arp(10)}
    out = {'latin': {k: is_latin(v) for k, v in Q.items()}}
    rng = np.random.default_rng(1818)
    res = {}
    for name, T in Q.items():
        rv, f1, f2 = [], [], []
        for _ in range(20):
            X = rng.integers(0, 256, (4096, 16), dtype=np.uint8)
            X[:, :7] = rng.integers(0, 256, 7, dtype=np.uint8)
            rv.append(int(np.unique(qg(T, X, 2, True)).size))
            Y = rng.integers(0, 256, (4096, 16), dtype=np.uint8)
            Y[:, 10:] = rng.integers(0, 256, 6, dtype=np.uint8)
            f1.append(int(np.unique(qg(T, Y, 1, False)).size))
            f2.append(int(np.unique(qg(T, Y, 2, False)).size))
        res[name] = {'rev_p2_distinct_per_family(min,max)': [min(rv), max(rv)],
                     'fwd_p1_distinct(min,max)': [min(f1), max(f1)], 'fwd_p2_distinct(min,max)': [min(f2), max(f2)]}
    out['families_4096_keys'] = res
    # near-duplicate key set (16 bases x 4080 single substitutions): full 64-bit collisions
    K = near_duplicates(np.random.default_rng(31))
    col = {}
    for name, T in Q.items():
        for (p, r) in ((1, False), (2, False), (1, True), (2, True), (4, True)):
            h = qg(T, K, p, r)
            col[f'{name} p{p}{"+rev" if r else ""}'] = int(len(h) - np.unique(h).size)
        col[f'QC-{name} d8'] = int(len(K) - np.unique(qc(T, K)).size)
    out['near_duplicates_full_collisions'] = col
    out['predicted_rev'] = 16 * (9 * 255 - 256)
    out['predicted_fwd1_with_255_refinement'] = 16 * (10 * 255 - 255)
    return out


def part_avalanche():
    Q = {'LS': random_latin(2026), 'NIMINV': niminv_qg(), 'ARP': arp(10), 'ISO': iso_z256(9)}
    X = np.random.default_rng(424242).integers(0, 256, (2000, 16), dtype=np.uint8)   # NEW keys (not the lab's)
    fns = {'QG-LS p2+rev': lambda Z: qg(Q['LS'], Z, 2, True), 'QG-NIMINV p2+rev': lambda Z: qg(Q['NIMINV'], Z, 2, True),
           'QG-ARP p2+rev': lambda Z: qg(Q['ARP'], Z, 2, True), 'QG-LS p1': lambda Z: qg(Q['LS'], Z, 1, False),
           'QG-ARP p1': lambda Z: qg(Q['ARP'], Z, 1, False),
           'QC-LS d8': lambda Z: qc(Q['LS'], Z), 'QC-ISO d8': lambda Z: qc(Q['ISO'], Z),
           'QC-NIMINV d8': lambda Z: qc(Q['NIMINV'], Z), 'QC-ARP d8': lambda Z: qc(Q['ARP'], Z),
           'MX64': mx64, 'BLAKE2b-64': blake, 'FNV-1a-64': fnv1a}
    out = {}
    for k, f in fns.items():
        t0 = time.time()
        out[k] = avalanche(f, X)
        print(k, out[k], round(time.time() - t0, 1), flush=True)
    return out


def part_noise():
    """Null distribution of max bias and BIC max for an ideal 64-bit function (BLAKE2b) with 2000 keys x 128 bits."""
    out = []
    for s in range(12):
        X = np.random.default_rng(9000 + s).integers(0, 256, (2000, 16), dtype=np.uint8)
        a = avalanche(blake, X)
        out.append({'max_bias': a['max_bias'], 'bic_max': a['bic_max'], 'mean_bias': a['mean_bias']})
        print(s, out[-1], flush=True)
    mb = np.array([o['max_bias'] for o in out])
    bm = np.array([o['bic_max'] for o in out])
    return {'replicates': out, 'max_bias_mean': round(float(mb.mean()), 4), 'max_bias_max': float(mb.max()),
            'bic_max_mean': round(float(bm.mean()), 4), 'bic_max_max': float(bm.max())}


def part_distribution():
    seq = [str(i).encode() for i in range(65536)]
    by_len = {}
    for i, k in enumerate(seq):
        by_len.setdefault(len(k), []).append(i)
    h_f = np.zeros(65536, np.uint64)
    h_m = np.zeros(65536, np.uint64)
    for L, idx in by_len.items():
        X = np.frombuffer(b''.join(seq[i] for i in idx), np.uint8).reshape(len(idx), L)
        h_f[idx] = fnv1a(X)
        h_m[idx] = mx64(X)
    rng = np.random.default_rng(5)
    out = {'FNV-1a sequential': {'z1024': chi2_z(h_f, 1024, 'mask'), 'z1021': chi2_z(h_f, 1021, 'mod'),
                                 'bucket_collision_ratio_2^16': bucket_ratio(h_f)},
           'MX64 sequential': {'z1024': chi2_z(h_m, 1024, 'mask'), 'z1021': chi2_z(h_m, 1021, 'mod'),
                               'bucket_collision_ratio_2^16': bucket_ratio(h_m)}}
    # ideal reference: uniformly random 64-bit values
    zs = [chi2_z(rng.integers(0, 2 ** 63, 65536, dtype=np.uint64), 1024, 'mask') for _ in range(200)]
    out['ideal_z1024_sd_over_200'] = round(float(np.std(zs)), 3)
    return out


if __name__ == '__main__':
    part = sys.argv[1]
    t0 = time.time()
    res = {'structure': part_structure, 'tailbound': part_tailbound, 'avalanche': part_avalanche,
           'noise': part_noise, 'distribution': part_distribution}[part]()
    res['runtime_s'] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, f'c18_{part}.json'), 'w') as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps(res, default=str)[:4000])
