"""Skeptic's own small-graph toolkit (independent of systems/graph_products.py and of networkx).

Graphs are numpy uint8 adjacency matrices (symmetric, zero diagonal).
* canon_small(A): exact canonical form (min upper-triangle code over all permutations), n <= 8.
* all_graphs(nmax): all graphs up to isomorphism, n = 1..nmax (nmax <= 7), by vertex augmentation.
* wl_hash(A): colour-refinement (1-WL) certificate - an isomorphism invariant.
* invariant(A): (n, m, degree sequence, WL hash, rounded adjacency spectrum) - an isomorphism invariant.
* isomorphic(A, B): exact test by individualisation-refinement backtracking (own implementation).
* local products: rel matrix and product by code (bit i <-> cell i in EA EN AE AA AN NE NA NN).
"""
import itertools
import hashlib
import numpy as np

E, A_, N_ = 0, 1, 2
CELLS = [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]   # EA EN AE AA AN NE NA NN


# ------------------------------------------------------------------ local products (own implementation)
def rel(A):
    n = A.shape[0]
    R = np.where(A > 0, A_, N_).astype(np.int8)
    R[np.arange(n), np.arange(n)] = E
    return R


def cellset(code):
    return {CELLS[i] for i in range(8) if code >> i & 1}


def prod(code, G, H):
    """(g,h) ~ (g',h') iff (rel_G(g,g'), rel_H(h,h')) in S; vertex (g,h) -> g*|H| + h."""
    S = cellset(code)
    T = np.zeros((3, 3), dtype=np.uint8)
    for (r, s) in S:
        T[r, s] = 1
    RG, RH = rel(G), rel(H)
    n, m = G.shape[0], H.shape[0]
    P = T[RG[:, None, :, None], RH[None, :, None, :]]
    return P.reshape(n * m, n * m).astype(np.uint8)


def complement(A):
    n = A.shape[0]
    C = (1 - A).astype(np.uint8)
    C[np.arange(n), np.arange(n)] = 0
    return C


def is_connected(A):
    n = A.shape[0]
    if n <= 1:
        return True
    seen = np.zeros(n, bool)
    seen[0] = True
    frontier = [0]
    while frontier:
        nxt = []
        for v in frontier:
            for w in np.nonzero(A[v])[0]:
                if not seen[w]:
                    seen[w] = True
                    nxt.append(int(w))
        frontier = nxt
    return bool(seen.all())


# ------------------------------------------------------------------ exact canonical form for small graphs
_PERMS = {}


def _perms(n):
    if n not in _PERMS:
        _PERMS[n] = np.array(list(itertools.permutations(range(n))), dtype=np.int64)
    return _PERMS[n]


_IU = {}


def canon_small(A):
    """Exact canonical code: minimum over all n! relabellings of the upper-triangle bit string (n <= 8)."""
    n = A.shape[0]
    if n <= 1:
        return (n, 0)
    P = _perms(n)
    if n not in _IU:
        iu = np.triu_indices(n, 1)
        _IU[n] = (iu, (1 << np.arange(len(iu[0]), dtype=np.int64)))
    (iu0, iu1), w = _IU[n]
    # permuted adjacency: B[p][i][j] = A[p[i], p[j]]
    vals = A[P[:, iu0], P[:, iu1]].astype(np.int64)        # (n!, n(n-1)/2)
    codes = vals @ w
    return (n, int(codes.min()))


def from_canon(key):
    n, code = key
    A = np.zeros((n, n), dtype=np.uint8)
    iu = np.triu_indices(n, 1)
    for k in range(len(iu[0])):
        if code >> k & 1:
            A[iu[0][k], iu[1][k]] = A[iu[1][k], iu[0][k]] = 1
    return A


def all_graphs(nmax):
    """Dict n -> list of adjacency matrices, one per isomorphism class (canonical representatives)."""
    out = {1: [np.zeros((1, 1), np.uint8)]}
    for n in range(2, nmax + 1):
        keys = set()
        for G in out[n - 1]:
            for mask in range(1 << (n - 1)):
                H = np.zeros((n, n), np.uint8)
                H[:n - 1, :n - 1] = G
                for j in range(n - 1):
                    if mask >> j & 1:
                        H[n - 1, j] = H[j, n - 1] = 1
                keys.add(canon_small(H))
        out[n] = [from_canon(k) for k in sorted(keys)]
    return out


# ------------------------------------------------------------------ invariants
def _h(x):
    return hashlib.blake2b(repr(x).encode(), digest_size=8).hexdigest()


def wl_colours(A, init=None, rounds=None):
    n = A.shape[0]
    col = [0] * n if init is None else list(init)
    nbrs = [np.nonzero(A[v])[0].tolist() for v in range(n)]
    rounds = n if rounds is None else rounds
    for _ in range(rounds):
        sig = [(col[v], tuple(sorted(col[w] for w in nbrs[v]))) for v in range(n)]
        # relabel signatures canonically (by sorted order of signatures)
        order = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [order[s] for s in sig]
        if len(set(new)) == len(set(col)):
            col = new
            break
        col = new
    return col


def wl_hash(A):
    """Multiset-of-colour-histories certificate (iso-invariant)."""
    n = A.shape[0]
    col = [0] * n
    nbrs = [np.nonzero(A[v])[0].tolist() for v in range(n)]
    hist = []
    for _ in range(min(n, 6) + 1):
        sig = [_h((col[v], tuple(sorted(col[w] for w in nbrs[v])))) for v in range(n)]
        col = sig
        hist.append(tuple(sorted(col)))
    return _h(tuple(hist))


def invariant(A):
    M = A.astype(np.float64)
    ev = np.linalg.eigvalsh(M) if A.shape[0] else np.array([])
    deg = tuple(sorted(A.sum(axis=1).tolist()))
    tri = int(np.trace(M @ M @ M) / 6 + 0.5) if A.shape[0] else 0
    return (A.shape[0], int(A.sum()) // 2, deg, tri, wl_hash(A), tuple(np.round(ev, 6) + 0.0))


# ------------------------------------------------------------------ exact isomorphism (individualisation-refinement)
def _refine(A, B, ca, cb):
    """Joint colour refinement of two graphs; returns refined colourings or None if they become incompatible."""
    n = A.shape[0]
    na = [np.nonzero(A[v])[0].tolist() for v in range(n)]
    nb = [np.nonzero(B[v])[0].tolist() for v in range(n)]
    while True:
        sa = [(ca[v], tuple(sorted(ca[w] for w in na[v]))) for v in range(n)]
        sb = [(cb[v], tuple(sorted(cb[w] for w in nb[v]))) for v in range(n)]
        if sorted(sa) != sorted(sb):
            return None
        order = {s: i for i, s in enumerate(sorted(set(sa)))}
        new_a = [order[s] for s in sa]
        new_b = [order[s] for s in sb]
        if len(set(new_a)) == len(set(ca)):
            return new_a, new_b
        ca, cb = new_a, new_b


def find_isomorphism(A, B):
    """Return a permutation f (list) with B[f[i], f[j]] = A[i, j], or None."""
    n = A.shape[0]
    if B.shape[0] != n or A.sum() != B.sum():
        return None
    if sorted(A.sum(0).tolist()) != sorted(B.sum(0).tolist()):
        return None
    r = _refine(A, B, [0] * n, [0] * n)
    if r is None:
        return None

    def rec(ca, cb):
        if len(set(ca)) == n:
            f = [0] * n
            pos_b = {c: v for v, c in enumerate(cb)}
            for v in range(n):
                f[v] = pos_b[ca[v]]
            fa = np.array(f)
            if np.array_equal(B[np.ix_(fa, fa)], A):
                return f
            return None
        # smallest non-singleton cell
        counts = {}
        for c in ca:
            counts[c] = counts.get(c, 0) + 1
        c0 = min((k for k, v in counts.items() if v > 1), key=lambda k: (counts[k], k))
        v = ca.index(c0)
        big = max(ca) + 1
        for w in [u for u in range(n) if cb[u] == c0]:
            ca2 = list(ca)
            cb2 = list(cb)
            ca2[v] = big
            cb2[w] = big
            rr = _refine(A, B, ca2, cb2)
            if rr is None:
                continue
            res = rec(*rr)
            if res is not None:
                return res
        return None

    return rec(*r)


def isomorphic(A, B):
    return find_isomorphism(A, B) is not None


class Registry:
    """Isomorphism classes: bucket by invariant, exact test inside buckets (own backtracking)."""

    def __init__(self):
        self.buckets = {}
        self.n_classes = 0
        self.exact_tests = 0

    def add(self, A):
        key = invariant(A)
        lst = self.buckets.setdefault(key, [])
        for B, cid in lst:
            self.exact_tests += 1
            if isomorphic(A, B):
                return cid
        cid = self.n_classes
        self.n_classes += 1
        lst.append((A, cid))
        return cid


# ------------------------------------------------------------------ Seidel matrices and switching (own)
def seidel_plus_I(A):
    n = A.shape[0]
    return (np.ones((n, n), dtype=np.int64) - 2 * A.astype(np.int64))


def switch(A, Z):
    G = A.copy()
    n = G.shape[0]
    inZ = np.zeros(n, bool)
    inZ[list(Z)] = True
    cross = inZ[:, None] != inZ[None, :]
    G[cross] = 1 - G[cross]
    np.fill_diagonal(G, 0)
    return G


def isolate(A, v):
    """Switch so that v is isolated, return the graph on the other vertices (the descendant)."""
    G = switch(A, np.nonzero(A[v])[0].tolist())
    keep = [i for i in range(A.shape[0]) if i != v]
    return G[np.ix_(keep, keep)]


def switching_canon_small(A):
    """Exact canonical form of the switching class for n <= 9 (descendants have <= 8 vertices)."""
    n = A.shape[0]
    if n <= 2:
        return (n, 0)
    return min(canon_small(isolate(A, v)) for v in range(n))


def switching_invariant(A):
    """Multiset over vertices of the rounded adjacency spectrum of the descendant (a switching invariant)."""
    n = A.shape[0]
    out = []
    for v in range(n):
        D = isolate(A, v).astype(np.float64)
        out.append(tuple(np.round(np.linalg.eigvalsh(D), 5) + 0.0))
    return tuple(sorted(out))


def switching_equivalent(A, B):
    """Exact: A ~ B iff descendant(A, 0) is isomorphic to descendant(B, v) for some v."""
    n = A.shape[0]
    if B.shape[0] != n:
        return False
    if n <= 2:
        return True
    d0 = isolate(A, 0)
    return any(isomorphic(d0, isolate(B, v)) for v in range(n))
