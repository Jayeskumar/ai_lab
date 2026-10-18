"""Quasigroup string transformations as mixing primitives, and baseline hashes (cycle C18).

Quasigroups of order 256 are Cayley tables T (uint8, 256 x 256) with every row and column a permutation.
The *e-transformation* with leader l maps a byte string a_0 .. a_{k-1} to b_0 .. b_{k-1}, where
b_0 = T[l, a_0] and b_i = T[b_{i-1}, a_i] (Markovski et al.).  The hash ``QG(T, p, reverse)`` used here:

1. message M = key || (len(key) mod 256) || zero bytes, padded to at least 8 bytes;
2. p forward e-transformations with leaders LEADERS[0..p-1];
3. optionally one more e-transformation applied to the *reversed* string (leader REV_LEADER);
4. output = the last 8 bytes of the result, read as a big-endian 64-bit integer.

Baselines (documented, standard constants): FNV-1a 64-bit; MX64 (per byte h = (h ^ b) * 0x9E3779B97F4A7C15,
h ^= h >> 32, then the splitmix64 finaliser of h ^ len); BLAKE2b with an 8-byte digest (hashlib, a
cryptographic reference); CRC-32 (zlib, a 32-bit GF(2)-affine checksum).

Nothing in this module is a security evaluation; none of these functions should be used where an adversary
chooses the keys.
"""

from __future__ import annotations

import hashlib
import zlib
from functools import lru_cache

import numpy as np

N = 256
LEADERS = (0x5A, 0xC3, 0x17, 0xE8, 0x2D, 0x91, 0x6B, 0xB4)
REV_LEADER = 0x3C
M64 = np.uint64(0xFFFFFFFFFFFFFFFF)


# ------------------------------------------------------------------ nimbers of order 256 (GF(2^8))
@lru_cache(maxsize=None)
def nim_mul(a: int, b: int) -> int:
    """Conway's nim-product, by the Fermat 2-power recursion (independent of the mex tables of C07)."""
    if a < 2 or b < 2:
        return a * b
    m = max(a, b)
    h = 1                      # half-width in bits: the field 2^(2h) must contain a and b
    while (1 << (2 * h)) <= m:
        h *= 2
    F = 1 << h
    a1, a0 = a >> h, a & (F - 1)
    b1, b0 = b >> h, b & (F - 1)
    z = nim_mul(a1, b1)
    hi = z ^ nim_mul(a1, b0) ^ nim_mul(a0, b1)
    lo = nim_mul(a0, b0) ^ nim_mul(z, F >> 1)
    return (hi << h) ^ lo


def nim_product_table() -> np.ndarray:
    return np.array([[nim_mul(a, b) for b in range(N)] for a in range(N)], dtype=np.uint8)


def nim_inverse() -> np.ndarray:
    P = nim_product_table()
    inv = np.zeros(N, dtype=np.uint8)
    for a in range(1, N):
        inv[a] = int(np.nonzero(P[a] == 1)[0][0])
    return inv


# ------------------------------------------------------------------ quasigroups of order 256
def is_quasigroup(T: np.ndarray) -> bool:
    full = np.arange(N)
    return bool(all(np.array_equal(np.sort(T[i]), full) for i in range(N)) and
                all(np.array_equal(np.sort(T[:, j]), full) for j in range(N)))


def random_latin_square(seed: int) -> np.ndarray:
    """Row-by-row completion with random perfect matchings (Hall's theorem guarantees each extension).

    Columns and symbols are randomly relabelled before each Hopcroft-Karp matching, so rows are random-looking;
    the square is NOT uniformly distributed among Latin squares (documented limitation)."""
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import maximum_bipartite_matching
    rng = np.random.default_rng(seed)
    used = np.zeros((N, N), dtype=bool)          # used[c, s]: symbol s already in column c
    T = np.zeros((N, N), dtype=np.uint8)
    for r in range(N):
        pc, ps = rng.permutation(N), rng.permutation(N)
        avail = ~used[np.ix_(pc, ps)]             # relabelled bipartite graph columns x symbols
        match = maximum_bipartite_matching(csr_matrix(avail.astype(np.int8)), perm_type="column")
        if (match < 0).any():
            raise RuntimeError("no perfect matching (impossible for a Latin rectangle)")
        for i in range(N):
            c, s = pc[i], ps[match[i]]
            T[r, c] = s
            used[c, s] = True
    return T


def group_isotope_z256(seed: int) -> np.ndarray:
    """x*y = pi(sigma(x) + tau(y) mod 256) for random permutations pi, sigma, tau."""
    rng = np.random.default_rng(seed)
    pi, sg, ta = rng.permutation(N), rng.permutation(N), rng.permutation(N)
    return pi[(sg[:, None] + ta[None, :]) % N].astype(np.uint8)


def nim_inverse_quasigroup() -> np.ndarray:
    """x*y = (x XOR y)^(-1) in the nimber field of order 256 (0 -> 0): an isotope of (GF(2)^8, XOR)."""
    inv = nim_inverse()
    x = np.arange(N)
    return inv[x[:, None] ^ x[None, :]].astype(np.uint8)


def affine_z256(a: int, b: int, c: int) -> np.ndarray:
    assert a % 2 == 1 and b % 2 == 1
    x = np.arange(N)
    return ((a * x[:, None] + b * x[None, :] + c) % N).astype(np.uint8)


def xor_quasigroup() -> np.ndarray:
    x = np.arange(N)
    return (x[:, None] ^ x[None, :]).astype(np.uint8)


def anchored_right_permutable(seed: int) -> np.ndarray:
    """C06 Theorem 4 with c a permutation: x*y = x + c(y) mod 256, c(0) = 1 (an anchored quasigroup)."""
    rng = np.random.default_rng(seed)
    rest = rng.permutation([v for v in range(N) if v != 1])
    c = np.empty(N, dtype=np.int64)
    c[0] = 1
    c[1:] = rest
    x = np.arange(N)
    return ((x[:, None] + c[None, :]) % N).astype(np.uint8)


def anchored_left_permutable_xor() -> np.ndarray:
    """C06 Theorem 7 with the group (GF(2)^8, XOR): x*y = (x + 1 mod 256) XOR y (an anchored quasigroup)."""
    x = np.arange(N)
    return (((x[:, None] + 1) % N) ^ x[None, :]).astype(np.uint8)


def is_t_function(T: np.ndarray) -> bool:
    """Does bit j of x*y depend only on bits 0..j of x and y (for every j)?"""
    x = np.arange(N)
    for j in range(8):
        m = (1 << (j + 1)) - 1
        low = T.astype(np.int64) & m
        # entries must agree whenever (x mod 2^(j+1), y mod 2^(j+1)) agree
        ref = low[np.ix_(x & m, x & m)]
        if not np.array_equal(low, ref):
            return False
    return True


def is_gf2_affine(T: np.ndarray) -> bool:
    """Is (x, y) -> x*y affine over GF(2) on 16 input bits, i.e. T[x,y] ^ T[0,0] = T[x,0] ^ T[0,y] ^ T[0,0]^...?"""
    t = T.astype(np.int64)
    c = t[0, 0]
    lin_x = t[:, 0] ^ c
    lin_y = t[0, :] ^ c
    pred = lin_x[:, None] ^ lin_y[None, :] ^ c
    if not np.array_equal(t, pred):
        return False
    # each part must itself be GF(2)-linear (after removing the constant)
    for v in (lin_x, lin_y):
        for a in range(N):
            if not np.array_equal(v[a ^ np.arange(N)], v[a] ^ v[np.arange(N)]):
                return False
    return True


# ------------------------------------------------------------------ e-transformations and the QG hash
def e_transform(T: np.ndarray, X: np.ndarray, leader: int) -> np.ndarray:
    """Row-wise e-transformation of a batch X (n_keys x L, uint8)."""
    out = np.empty_like(X)
    prev = np.full(X.shape[0], leader, dtype=np.uint8)
    for i in range(X.shape[1]):
        prev = T[prev, X[:, i]]
        out[:, i] = prev
    return out


def d_transform(T: np.ndarray, Y: np.ndarray, leader: int) -> np.ndarray:
    """Inverse of e_transform: a_i = b_{i-1} \\ b_i (left division)."""
    left_div = np.empty((N, N), dtype=np.uint8)          # left_div[u, v] = the a with T[u, a] = v
    for u in range(N):
        left_div[u, T[u]] = np.arange(N, dtype=np.uint8)
    out = np.empty_like(Y)
    prev = np.full(Y.shape[0], leader, dtype=np.uint8)
    for i in range(Y.shape[1]):
        out[:, i] = left_div[prev, Y[:, i]]
        prev = Y[:, i]
    return out


def encode(keys: list[bytes]) -> dict[int, tuple[np.ndarray, np.ndarray]]:
    """Group keys by message length; message = key || len mod 256 || zero padding to >= 8 bytes."""
    groups: dict[int, list[int]] = {}
    for idx, k in enumerate(keys):
        groups.setdefault(len(k), []).append(idx)
    out = {}
    for L, idxs in groups.items():
        mlen = max(L + 1, 8)
        X = np.zeros((len(idxs), mlen), dtype=np.uint8)
        if L:
            X[:, :L] = np.frombuffer(b"".join(keys[i] for i in idxs), dtype=np.uint8).reshape(len(idxs), L)
        X[:, L] = L % 256
        out[L] = (np.array(idxs), X)
    return out


def _tail64(Y: np.ndarray) -> np.ndarray:
    t = Y[:, -8:].astype(np.uint64)
    h = np.zeros(Y.shape[0], dtype=np.uint64)
    for j in range(8):
        h = (h << np.uint64(8)) | t[:, j]
    return h


def qg_hash_batch(T: np.ndarray, keys: list[bytes], passes: int, reverse: bool) -> np.ndarray:
    out = np.zeros(len(keys), dtype=np.uint64)
    for _, (idxs, X) in encode(keys).items():
        Y = X
        for p in range(passes):
            Y = e_transform(T, Y, LEADERS[p])
        if reverse:
            Y = e_transform(T, Y[:, ::-1].copy(), REV_LEADER)
        out[idxs] = _tail64(Y)
    return out


def qg_hash_fixed(T: np.ndarray, X: np.ndarray, passes: int, reverse: bool) -> np.ndarray:
    """Same as qg_hash_batch for a batch of equal-length keys given as a uint8 array (n x L)."""
    L = X.shape[1]
    M = np.zeros((X.shape[0], max(L + 1, 8)), dtype=np.uint8)
    M[:, :L] = X
    M[:, L] = L % 256
    Y = M
    for p in range(passes):
        Y = e_transform(T, Y, LEADERS[p])
    if reverse:
        Y = e_transform(T, Y[:, ::-1].copy(), REV_LEADER)
    return _tail64(Y)


# ------------------------------------------------------------------ baselines
FNV_OFFSET = np.uint64(0xCBF29CE484222325)
FNV_PRIME = np.uint64(0x100000001B3)
GOLDEN = np.uint64(0x9E3779B97F4A7C15)


def _fmix64(z: np.ndarray) -> np.ndarray:
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return z ^ (z >> np.uint64(31))


def fnv1a64_fixed(X: np.ndarray) -> np.ndarray:
    h = np.full(X.shape[0], FNV_OFFSET, dtype=np.uint64)
    with np.errstate(over="ignore"):
        for i in range(X.shape[1]):
            h = (h ^ X[:, i].astype(np.uint64)) * FNV_PRIME
    return h


def mx64_fixed(X: np.ndarray) -> np.ndarray:
    h = np.zeros(X.shape[0], dtype=np.uint64)
    with np.errstate(over="ignore"):
        for i in range(X.shape[1]):
            h = (h ^ X[:, i].astype(np.uint64)) * GOLDEN
            h = h ^ (h >> np.uint64(32))
        return _fmix64(h ^ np.uint64(X.shape[1]))


def _by_length(keys, fixed_fn):
    out = np.zeros(len(keys), dtype=np.uint64)
    groups: dict[int, list[int]] = {}
    for idx, k in enumerate(keys):
        groups.setdefault(len(k), []).append(idx)
    for L, idxs in groups.items():
        X = (np.frombuffer(b"".join(keys[i] for i in idxs), dtype=np.uint8).reshape(len(idxs), L)
             if L else np.zeros((len(idxs), 0), dtype=np.uint8))
        out[np.array(idxs)] = fixed_fn(X)
    return out


def fnv1a64_batch(keys):
    return _by_length(keys, fnv1a64_fixed)


def mx64_batch(keys):
    return _by_length(keys, mx64_fixed)


def blake2b64_batch(keys):
    return np.array([int.from_bytes(hashlib.blake2b(k, digest_size=8).digest(), "big") for k in keys],
                    dtype=np.uint64)


def crc32_batch(keys):
    return np.array([zlib.crc32(k) for k in keys], dtype=np.uint64)


def rows_to_keys(X: np.ndarray) -> list[bytes]:
    return [bytes(r) for r in X]


# ------------------------------------------------------------------ the hash zoo used in the experiments
def quasigroups(seed: int = 18) -> dict[str, np.ndarray]:
    return {
        "LS": random_latin_square(seed),
        "ISO": group_isotope_z256(seed + 1),
        "NIMINV": nim_inverse_quasigroup(),
        "AFF": affine_z256(77, 141, 5),
        "XOR": xor_quasigroup(),
        "ARP": anchored_right_permutable(seed + 2),
        "ALP": anchored_left_permutable_xor(),
    }


VARIANTS = [  # (name, quasigroup key, passes, reverse)
    ("QG-LS p1", "LS", 1, False), ("QG-LS p1+rev", "LS", 1, True),
    ("QG-LS p2", "LS", 2, False), ("QG-LS p2+rev", "LS", 2, True),
    ("QG-LS p4+rev", "LS", 4, True),
    ("QG-ISO p2+rev", "ISO", 2, True),
    ("QG-NIMINV p1+rev", "NIMINV", 1, True), ("QG-NIMINV p2+rev", "NIMINV", 2, True),
    ("QG-AFF p2+rev", "AFF", 2, True), ("QG-XOR p2+rev", "XOR", 2, True),
    ("QG-ARP p1", "ARP", 1, False), ("QG-ARP p2+rev", "ARP", 2, True),
    ("QG-ALP p2+rev", "ALP", 2, True),
]
BASELINES = ["FNV-1a-64", "MX64", "BLAKE2b-64", "CRC32"]
OUT_BITS = {"CRC32": 32}


def hash_keys(name: str, keys: list[bytes], qgs: dict) -> np.ndarray:
    if name == "FNV-1a-64":
        return fnv1a64_batch(keys)
    if name == "MX64":
        return mx64_batch(keys)
    if name == "BLAKE2b-64":
        return blake2b64_batch(keys)
    if name == "CRC32":
        return crc32_batch(keys)
    v = next(v for v in VARIANTS if v[0] == name)
    return qg_hash_batch(qgs[v[1]], keys, v[2], v[3])


def hash_fixed(name: str, X: np.ndarray, qgs: dict) -> np.ndarray:
    if name == "FNV-1a-64":
        return fnv1a64_fixed(X)
    if name == "MX64":
        return mx64_fixed(X)
    if name in ("BLAKE2b-64", "CRC32"):
        return hash_keys(name, rows_to_keys(X), qgs)
    v = next(v for v in VARIANTS if v[0] == name)
    return qg_hash_fixed(qgs[v[1]], X, v[2], v[3])


# ------------------------------------------------------------------ metrics
def bits_of(h: np.ndarray, nbits: int) -> np.ndarray:
    return ((h[:, None] >> np.arange(nbits, dtype=np.uint64)[None, :]) & np.uint64(1)).astype(np.uint8)


def avalanche(name: str, X: np.ndarray, qgs: dict) -> dict:
    """Flip every input bit of every key; p[i, j] = P(output bit j changes | input bit i flipped)."""
    nb = OUT_BITS.get(name, 64)
    base = hash_fixed(name, X, qgs)
    L = X.shape[1]
    P = np.zeros((8 * L, nb))
    bic_max, bic_sum, bic_cnt = 0.0, 0.0, 0
    for i in range(8 * L):
        Xf = X.copy()
        Xf[:, i // 8] ^= np.uint8(1 << (i % 8))
        d = bits_of(base ^ hash_fixed(name, Xf, qgs), nb).astype(np.float64)
        P[i] = d.mean(axis=0)
        sd = d.std(axis=0)
        ok = sd > 0
        if ok.sum() >= 2:
            C = np.corrcoef(d[:, ok].T)
            off = np.abs(C[~np.eye(C.shape[0], dtype=bool)])
            bic_max = max(bic_max, float(off.max()))
            bic_sum += float(off.sum())
            bic_cnt += off.size
        if (~ok).sum() >= 2:      # constant change indicators: perfectly dependent
            bic_max = 1.0
    bias = np.abs(P - 0.5)
    return {"mean_flip_rate": round(float(P.mean()), 4), "mean_bias": round(float(bias.mean()), 4),
            "max_bias": round(float(bias.max()), 4), "cells_bias_gt_0.1": int((bias > 0.1).sum()),
            "deterministic_cells": int(((P == 0) | (P == 1)).sum()), "cells": int(P.size),
            "bic_max_abs_corr": round(bic_max, 4),
            "bic_mean_abs_corr": round(bic_sum / bic_cnt, 4) if bic_cnt else None}


def chi2_z(h: np.ndarray, m: int, mode: str) -> float:
    b = (h & np.uint64(m - 1)) if mode == "mask" else (h % np.uint64(m))
    counts = np.bincount(b.astype(np.int64), minlength=m)
    e = len(h) / m
    chi2 = float(((counts - e) ** 2).sum() / e)
    return round((chi2 - (m - 1)) / np.sqrt(2 * (m - 1)), 2)


def collisions(h: np.ndarray, m_bits: int = 16) -> dict:
    n = len(h)
    m = 1 << m_bits
    b = (h & np.uint64(m - 1)).astype(np.int64)
    occupied = np.unique(b).size
    expected_occupied = m * (1 - (1 - 1 / m) ** n)
    return {"bucket_collisions": int(n - occupied), "expected": round(n - expected_occupied, 1),
            "ratio": round((n - occupied) / (n - expected_occupied), 4),
            "full_64bit_collisions": int(n - np.unique(h).size)}
