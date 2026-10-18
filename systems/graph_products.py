"""System D: graphs as quantities -- the 256 local graph products.

A *local product* of simple graphs G and H has vertex set V(G) x V(H); whether
two distinct vertices (g, h) and (g', h') are adjacent depends only on the pair
of relations (rel_G(g, g'), rel_H(h, h')), where each relation is

    E (equal), A (adjacent) or N (distinct and non-adjacent).

Excluding the diagonal cell (E, E), a product is a subset S of the 8 cells
below, encoded as an integer ``code`` in 0..255 (bit i <-> CELLS[i] in S).

Graphs are handled as numpy 0/1 adjacency matrices (symmetric, zero
diagonal).  Isomorphism questions are answered exactly with networkx (VF2)
after bucketing by invariants (``IsoRegistry``).
"""

from __future__ import annotations

import itertools

import networkx as nx
import numpy as np

E, A, N = 0, 1, 2
REL = "EAN"
CELLS = [(a, b) for a in range(3) for b in range(3) if (a, b) != (E, E)]
TRIPLES = [t for t in itertools.product(range(3), repeat=3) if t != (E, E, E)]

NAMED = {
    "empty": [],
    "complete": CELLS,
    "cartesian": [(E, A), (A, E)],
    "direct": [(A, A)],
    "strong": [(E, A), (A, E), (A, A)],
    "lexicographic": [(E, A), (A, E), (A, A), (A, N)],
    "co-normal": [(E, A), (A, E), (A, A), (A, N), (N, A)],
    "symmetric difference": [(E, A), (A, E), (A, N), (N, A)],
    "modular": [(A, A), (N, N)],
    "rejection": [(E, N), (N, E), (N, N)],
    "homomorphic": [(E, A), (E, N), (A, E), (A, N)],
}


def code_of(cells) -> int:
    return sum(1 << CELLS.index(tuple(c)) for c in cells)


NAMED_CODES = {name: code_of(c) for name, c in NAMED.items()}


def cells_of(code: int) -> list[tuple[int, int]]:
    return [c for i, c in enumerate(CELLS) if code >> i & 1]


def show(code: int) -> str:
    """Cells of a product, e.g. 'EA AE' for the Cartesian product."""
    return " ".join(REL[a] + REL[b] for a, b in cells_of(code)) or "-"


def name_of(code: int) -> str | None:
    for k, v in NAMED_CODES.items():
        if v == code:
            return k
    return None


def table(code: int) -> np.ndarray:
    """3x3 0/1 lookup table T[r1, r2] (T[E, E] = 0)."""
    T = np.zeros((3, 3), dtype=np.int8)
    for a, b in cells_of(code):
        T[a, b] = 1
    return T


# ------------------------------------------------------------------ symmetries of the product space
def transpose(code: int) -> int:
    """Product with the factors' roles exchanged: G *' H = swap(H * G)."""
    return code_of([(b, a) for a, b in cells_of(code)])


def swap_an(code: int, first: bool = True, second: bool = True) -> int:
    """Replace a factor by its complement: exchange A and N in the chosen coordinates."""
    sw = {E: E, A: N, N: A}
    return code_of([(sw[a] if first else a, sw[b] if second else b) for a, b in cells_of(code)])


def complement_product(code: int) -> int:
    """G *' H = complement of G * H."""
    return code ^ 0xFF


def conjugate(code: int) -> int:
    """Complement-conjugate: G *' H = complement(complement(G) * complement(H))."""
    return complement_product(swap_an(code))


# ------------------------------------------------------------------ the finite (relation-level) calculus
def phi(code: int, r1: int, r2: int) -> int:
    """Relation of (g, h), (g', h') in G * H, given r1 = rel_G(g, g'), r2 = rel_H(h, h')."""
    if r1 == E and r2 == E:
        return E
    return A if (code >> CELLS.index((r1, r2))) & 1 else N


def adj(code: int, r1: int, r2: int) -> bool:
    return phi(code, r1, r2) == A


def assoc_defects(code: int) -> list[tuple[int, int, int]]:
    """Triples t != (E,E,E) on which (x*y)*z and x*(y*z) disagree (empty iff strictly associative)."""
    return [t for t in TRIPLES if adj(code, phi(code, t[0], t[1]), t[2]) != adj(code, t[0], phi(code, t[1], t[2]))]


def is_associative(code: int) -> bool:
    return not assoc_defects(code)


def is_commutative(code: int) -> bool:
    return code == transpose(code)


def has_left_unit(code: int) -> bool:
    """K1 * G = G via (u, g) -> g for all G."""
    S = set(cells_of(code))
    return (E, A) in S and (E, N) not in S


def has_right_unit(code: int) -> bool:
    S = set(cells_of(code))
    return (A, E) in S and (N, E) not in S


def right_distributive(code: int) -> bool:
    """(G + G') * H = G*H + G'*H strictly: no cell (N, .) in S."""
    return all(a != N for a, _ in cells_of(code))


def left_distributive(code: int) -> bool:
    """G * (H + H') = G*H + G*H' strictly: no cell (., N) in S."""
    return all(b != N for _, b in cells_of(code))


# ------------------------------------------------------------------ graphs as adjacency matrices
def rel_matrix(adjm: np.ndarray) -> np.ndarray:
    n = adjm.shape[0]
    R = np.where(adjm > 0, A, N).astype(np.int8)
    R[np.arange(n), np.arange(n)] = E
    return R


def product(code: int, G: np.ndarray, H: np.ndarray) -> np.ndarray:
    """Adjacency matrix of G * H, vertices ordered (g, h) -> g * |H| + h."""
    T = table(code)
    RG, RH = rel_matrix(G), rel_matrix(H)
    n, m = G.shape[0], H.shape[0]
    P = T[RG[:, None, :, None], RH[None, :, None, :]]  # axes g, h, g', h'
    return P.reshape(n * m, n * m).astype(np.int8)


def from_nx(g: nx.Graph) -> np.ndarray:
    nodes = sorted(g.nodes())
    return nx.to_numpy_array(g, nodelist=nodes, dtype=np.int8)


def to_nx(adjm: np.ndarray) -> nx.Graph:
    return nx.from_numpy_array(np.asarray(adjm))


def complement(adjm: np.ndarray) -> np.ndarray:
    n = adjm.shape[0]
    C = 1 - adjm
    C[np.arange(n), np.arange(n)] = 0
    return C.astype(np.int8)


def disjoint_union(G: np.ndarray, H: np.ndarray) -> np.ndarray:
    n, m = G.shape[0], H.shape[0]
    U = np.zeros((n + m, n + m), dtype=np.int8)
    U[:n, :n] = G
    U[n:, n:] = H
    return U


def K(n: int) -> np.ndarray:
    return complement(np.zeros((n, n), dtype=np.int8))


def empty(n: int) -> np.ndarray:
    return np.zeros((n, n), dtype=np.int8)


def path(n: int) -> np.ndarray:
    P = np.zeros((n, n), dtype=np.int8)
    for i in range(n - 1):
        P[i, i + 1] = P[i + 1, i] = 1
    return P


def atlas(max_n: int = 7) -> list[np.ndarray]:
    """All graphs with 1..max_n vertices up to isomorphism (networkx atlas, max_n <= 7)."""
    return [from_nx(g) for g in nx.graph_atlas_g()[1:] if g.number_of_nodes() <= max_n]


def is_connected(adjm: np.ndarray) -> bool:
    n = adjm.shape[0]
    if n <= 1:
        return True
    seen, stack = {0}, [0]
    while stack:
        v = stack.pop()
        for w in np.nonzero(adjm[v])[0]:
            w = int(w)
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


# ------------------------------------------------------------------ isomorphism classes
def invariant(adjm: np.ndarray) -> tuple:
    """Cheap isomorphism invariant: order, size, degree sequence, sorted neighbour-degree multisets, triangles."""
    M = np.asarray(adjm, dtype=np.int64)
    deg = M.sum(axis=1)
    nd = sorted(tuple(sorted(deg[np.nonzero(M[v])[0]].tolist())) for v in range(M.shape[0]))
    tri = int(np.trace(M @ M @ M)) // 6 if M.shape[0] <= 400 else -1
    return (M.shape[0], int(M.sum()) // 2, tuple(sorted(deg.tolist())), tuple(nd), tri)


def isomorphic(G: np.ndarray, H: np.ndarray) -> bool:
    if G.shape != H.shape or invariant(G) != invariant(H):
        return False
    return nx.is_isomorphic(to_nx(G), to_nx(H))


class IsoRegistry:
    """Assigns a class id to every graph added; exact (VF2) within invariant buckets."""

    def __init__(self):
        self.buckets: dict[tuple, list[tuple[nx.Graph, int]]] = {}
        self.reps: list[np.ndarray] = []

    def find(self, adjm: np.ndarray) -> int | None:
        key = invariant(adjm)
        g = to_nx(adjm)
        for h, cid in self.buckets.get(key, []):
            if nx.is_isomorphic(g, h):
                return cid
        return None

    def add(self, adjm: np.ndarray) -> int:
        cid = self.find(adjm)
        if cid is not None:
            return cid
        cid = len(self.reps)
        self.reps.append(np.asarray(adjm, dtype=np.int8))
        self.buckets.setdefault(invariant(adjm), []).append((to_nx(adjm), cid))
        return cid


# ------------------------------------------------------------------ Kronecker characters
def character_matrix(adjm: np.ndarray, c: tuple) -> np.ndarray:
    """M_c(G) = c_E I + c_A A + c_N (J - I - A)."""
    n = adjm.shape[0]
    I = np.eye(n)
    Aa = np.asarray(adjm, dtype=float)
    return c[0] * I + c[1] * Aa + c[2] * (np.ones((n, n)) - I - Aa)


def kronecker_characters(code: int) -> list[tuple]:
    """All c = (c_E, c_A, c_N) with c_A != c_N and M_c(G*H) = M_c(G) (x) M_c(H) for all G, H.

    By the cell decomposition (see proofs/paper/C14.md, Theorem 4) this is equivalent to the finite system
    c_E^2 = c_E and c_r c_s = (c_A if (r, s) in S else c_N) for all cells (r, s) != (E, E); it is solved
    exactly here over the candidate values {-1, 0, 1} (the proof shows no other values occur).
    """
    S = set(cells_of(code))
    out = []
    for c in itertools.product((-1, 0, 1), repeat=3):
        if c[1] == c[2] or c[0] * c[0] != c[0]:
            continue
        if all(c[r] * c[s] == (c[A] if (r, s) in S else c[N]) for r, s in CELLS):
            out.append(c)
    return out


# ------------------------------------------------------------------ Seidel matrices and switching
def seidel(adjm: np.ndarray) -> np.ndarray:
    n = adjm.shape[0]
    return np.ones((n, n), dtype=np.int64) - np.eye(n, dtype=np.int64) - 2 * np.asarray(adjm, dtype=np.int64)


def switch(adjm: np.ndarray, X) -> np.ndarray:
    """Seidel switching with respect to the vertex set X."""
    G = np.array(adjm, dtype=np.int8)
    n = G.shape[0]
    inX = np.zeros(n, dtype=bool)
    inX[list(X)] = True
    cross = inX[:, None] != inX[None, :]
    G[cross] = 1 - G[cross]
    return G


def descendant(adjm: np.ndarray, v: int) -> np.ndarray:
    """Switch so that v becomes isolated, then delete v (the 'descendant' graph of the switching class)."""
    G = switch(adjm, np.nonzero(adjm[v])[0].tolist())
    keep = [i for i in range(G.shape[0]) if i != v]
    return G[np.ix_(keep, keep)]


def seidel_key(adjm: np.ndarray) -> tuple:
    ev = np.linalg.eigvalsh(seidel(adjm).astype(float))
    return (adjm.shape[0], tuple(np.round(np.sort(ev), 6).tolist()))


class SwitchingRegistry:
    """Assigns ids to switching classes (two-graphs): bucket by Seidel spectrum, decide by descendants."""

    def __init__(self):
        self.buckets: dict[tuple, list[tuple[np.ndarray, int]]] = {}
        self.reps: list[np.ndarray] = []

    @staticmethod
    def equivalent(G: np.ndarray, H: np.ndarray) -> bool:
        n = G.shape[0]
        if n != H.shape[0]:
            return False
        if n <= 2:
            return True
        d0 = to_nx(descendant(G, 0))
        return any(nx.is_isomorphic(d0, to_nx(descendant(H, v))) for v in range(n))

    def find(self, adjm: np.ndarray) -> int | None:
        for h, cid in self.buckets.get(seidel_key(adjm), []):
            if self.equivalent(adjm, h):
                return cid
        return None

    def add(self, adjm: np.ndarray) -> int:
        cid = self.find(adjm)
        if cid is not None:
            return cid
        cid = len(self.reps)
        self.reps.append(np.asarray(adjm, dtype=np.int8))
        self.buckets.setdefault(seidel_key(adjm), []).append((np.asarray(adjm, dtype=np.int8), cid))
        return cid
