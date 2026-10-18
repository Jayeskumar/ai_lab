"""System B: magmas, terms, identities and SAT-based model search.

A *term* is a variable name (a one-letter string) or a pair ``(left, right)``
standing for ``left * right``.  An *identity* is a pair of terms ``(s, t)``
read as "s = t for every assignment of the variables".  A finite magma of size
n is a Cayley table ``T`` with ``T[a][b] = a*b`` on ``{0, ..., n-1}``.

Model search uses a direct SAT encoding (pysat):

* ``v[a,b,c]``  <=>  ``a*b = c``  (exactly one c for each (a, b));
* for every compound subterm s and every assignment of its variables, value
  variables ``w[s,sigma,c]`` linked by  w[s1] & w[s2] & v -> w[s]  plus
  at-most-one; the top terms of both sides are then required to agree.

The encoding is exact: its models are precisely the Cayley tables satisfying
the identities (see ``proofs/paper/C05.md``, Lemma 0).
"""

from __future__ import annotations

import itertools
from functools import lru_cache

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

# ------------------------------------------------------------------ terms
def is_var(t) -> bool:
    return isinstance(t, str)


def leaves(t) -> list[str]:
    return [t] if is_var(t) else leaves(t[0]) + leaves(t[1])


def n_ops(t) -> int:
    return 0 if is_var(t) else 1 + n_ops(t[0]) + n_ops(t[1])


def variables(t) -> list[str]:
    seen = []
    for v in leaves(t):
        if v not in seen:
            seen.append(v)
    return seen


def mirror(t):
    return t if is_var(t) else (mirror(t[1]), mirror(t[0]))


def rename(t, mapping):
    return mapping.get(t, t) if is_var(t) else (rename(t[0], mapping), rename(t[1], mapping))


def to_str(t) -> str:
    if is_var(t):
        return t
    a = to_str(t[0]) if is_var(t[0]) else "(" + to_str(t[0]) + ")"
    b = to_str(t[1]) if is_var(t[1]) else "(" + to_str(t[1]) + ")"
    return a + b


def parse(s: str):
    """Parse juxtaposition notation, left-associative: 'y(xy)', '(xy)(yx)', 'xyz' = (xy)z."""
    s = s.replace(" ", "").replace("*", "")
    pos = 0

    def atom():
        nonlocal pos
        if s[pos] == "(":
            pos += 1
            e = expr()
            assert s[pos] == ")", s
            pos += 1
            return e
        c = s[pos]
        pos += 1
        return c

    def expr():
        nonlocal pos
        e = atom()
        while pos < len(s) and s[pos] != ")":
            e = (e, atom())
        return e

    out = expr()
    assert pos == len(s), s
    return out


@lru_cache(maxsize=None)
def shapes(k: int) -> tuple:
    """All binary-tree shapes with k internal nodes; leaves are None."""
    if k == 0:
        return (None,)
    out = []
    for i in range(k):
        for a in shapes(i):
            for b in shapes(k - 1 - i):
                out.append((a, b))
    return tuple(out)


def fill(shape, labels):
    it = iter(labels)

    def go(s):
        if s is None:
            return next(it)
        return (go(s[0]), go(s[1]))

    return go(shape)


def n_leaves(shape) -> int:
    return 1 if shape is None else n_leaves(shape[0]) + n_leaves(shape[1])


# ------------------------------------------------------------------ evaluation
def eval_array(T: np.ndarray, t, var_order: list[str]) -> np.ndarray:
    """Value of term t for all assignments, as an array with one axis per variable in var_order."""
    n = T.shape[0]
    r = len(var_order)
    if is_var(t):
        i = var_order.index(t)
        shape = [1] * r
        shape[i] = n
        return np.broadcast_to(np.arange(n).reshape(shape), (n,) * r)
    return T[eval_array(T, t[0], var_order), eval_array(T, t[1], var_order)]


def satisfies(T, identity) -> bool:
    T = np.asarray(T)
    s, t = identity
    vs = variables(s)
    for v in variables(t):
        if v not in vs:
            vs.append(v)
    return bool(np.all(eval_array(T, s, vs) == eval_array(T, t, vs)))


def is_quasigroup(T) -> bool:
    T = np.asarray(T)
    n = T.shape[0]
    return all(len(set(T[a, :])) == n for a in range(n)) and all(len(set(T[:, b])) == n for b in range(n))


def canonical(T) -> tuple:
    """Canonical form under isomorphism (minimum relabelled table)."""
    T = np.asarray(T)
    n = T.shape[0]
    best = None
    for p in itertools.permutations(range(n)):
        p = np.array(p)
        inv = np.argsort(p)
        # relabelled table U[p[a], p[b]] = p[T[a, b]]  ->  U[i, j] = p[T[inv[i], inv[j]]]
        U = p[T[np.ix_(inv, inv)]]
        key = tuple(U.flatten().tolist())
        if best is None or key < best:
            best = key
    return best


# ------------------------------------------------------------------ SAT
class MagmaSAT:
    """SAT encoding of 'n-element magma satisfying all given identities'."""

    def __init__(self, n: int, identities, extra=None):
        self.n = n
        self.pool = IDPool()
        self.clauses: list[list[int]] = []
        P = self.pool
        R = range(n)
        self.v = {(a, b, c): P.id(("v", a, b, c)) for a in R for b in R for c in R}
        for a in R:
            for b in R:
                lits = [self.v[a, b, c] for c in R]
                self.clauses += CardEnc.equals(lits, 1, vpool=P, encoding=EncType.pairwise).clauses
        for idn, (s, t) in enumerate(identities):
            vs = variables(s)
            for x in variables(t):
                if x not in vs:
                    vs.append(x)
            for sigma in itertools.product(R, repeat=len(vs)):
                asg = dict(zip(vs, sigma))
                ls = self._encode(s, asg)
                lt = self._encode(t, asg)
                # both sides must take the same value
                if isinstance(ls, int) and isinstance(lt, int):
                    if ls != lt:
                        self.clauses.append([])
                elif isinstance(ls, int):
                    self.clauses.append([lt[ls]])
                elif isinstance(lt, int):
                    self.clauses.append([ls[lt]])
                else:
                    for c in R:
                        self.clauses.append([-ls[c], lt[c]])
                        self.clauses.append([-lt[c], ls[c]])
        if extra:
            self.clauses += extra(self)

    def _encode(self, t, asg):
        """Return an int (the value, for a variable) or a dict c -> literal 'term has value c'."""
        if is_var(t):
            return asg[t]
        key = ("w", self._key(t, asg))
        P = self.pool
        if P.obj2id.get((key, 0)) is not None:
            return {c: P.id((key, c)) for c in range(self.n)}
        w = {c: P.id((key, c)) for c in range(self.n)}
        A = self._encode(t[0], asg)
        B = self._encode(t[1], asg)
        R = range(self.n)
        for a in ([A] if isinstance(A, int) else R):
            for b in ([B] if isinstance(B, int) else R):
                for c in R:
                    cl = [-self.v[a, b, c], w[c]]
                    if not isinstance(A, int):
                        cl.append(-A[a])
                    if not isinstance(B, int):
                        cl.append(-B[b])
                    self.clauses.append(cl)
        self.clauses += CardEnc.atmost(list(w.values()), 1, vpool=P, encoding=EncType.pairwise).clauses
        return w

    def _key(self, t, asg):
        vs = variables(t)
        return (to_str(t), tuple(asg[x] for x in vs))

    def table_from_model(self, model) -> np.ndarray:
        pos = set(x for x in model if x > 0)
        n = self.n
        T = np.zeros((n, n), dtype=np.int64)
        for (a, b, c), lit in self.v.items():
            if lit in pos:
                T[a, b] = c
        return T

    def solve(self, conf_budget: int | None = None):
        """Return (status, table): status in {'SAT', 'UNSAT', 'UNKNOWN'}."""
        if any(len(c) == 0 for c in self.clauses):
            return "UNSAT", None
        with Cadical153(bootstrap_with=self.clauses) as s:
            if conf_budget is None:
                ok = s.solve()
            else:
                s.conf_budget(conf_budget)
                ok = s.solve_limited()
            if ok is None:
                return "UNKNOWN", None
            if not ok:
                return "UNSAT", None
            return "SAT", self.table_from_model(s.get_model())

    def enumerate(self, limit: int = 100_000):
        """All models (Cayley tables), up to ``limit``; returns (tables, complete_flag)."""
        if any(len(c) == 0 for c in self.clauses):
            return [], True
        out = []
        with Cadical153(bootstrap_with=self.clauses) as s:
            while s.solve():
                T = self.table_from_model(s.get_model())
                out.append(T)
                if len(out) >= limit:
                    return out, False
                s.add_clause([-self.v[a, b, int(T[a, b])] for a in range(self.n) for b in range(self.n)])
        return out, True


def spectrum(identities, sizes, conf_budget=None) -> dict:
    out = {}
    for n in sizes:
        status, _ = MagmaSAT(n, identities).solve(conf_budget)
        out[n] = status
    return out


def models_up_to_iso(identities, n: int, limit: int = 50_000):
    tables, complete = MagmaSAT(n, identities).enumerate(limit)
    classes = {}
    for T in tables:
        classes.setdefault(canonical(T), T)
    return len(tables), len(classes), complete, list(classes.values())


# ------------------------------------------------------------------ identity families
def identities_t_eq_x(k_ops: int, var_names=("x", "y")):
    """All identities t = x with n_ops(t) = k_ops over the given variables, up to renaming.

    Canonical form: the right-hand side is 'x'; the other variables of t are named
    y, z, ... in order of first appearance.  Variables need not all occur.
    """
    others = [v for v in var_names if v != "x"]
    seen = {}
    for shape in shapes(k_ops):
        L = n_leaves(shape)
        for labels in itertools.product(var_names, repeat=L):
            # canonical renaming of the non-x variables by first appearance
            mapping, nxt = {}, iter(others)
            ok = True
            for lab in labels:
                if lab != "x" and lab not in mapping:
                    mapping[lab] = next(nxt)
            canon = tuple(mapping.get(l, l) for l in labels)
            if canon != labels:
                continue
            t = fill(shape, labels)
            seen[to_str(t)] = t
    return [(t, "x") for t in seen.values()]


def classify_trivially(t) -> str:
    """Cheap a-priori classification of t = x."""
    ls = leaves(t)
    if "x" not in ls:
        return "collapsing (x absent: only the 1-element magma)"
    if ls[0] == "x":
        return "left projection is a model of every size"
    if ls[-1] == "x":
        return "right projection is a model of every size"
    return "nontrivial"


def affine_models(identity, n: int):
    """All (a, b, c) in Z_n^3 such that x*y = a x + b y + c (mod n) satisfies the identity."""
    out = []
    ar = np.arange(n)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                T = (a * ar[:, None] + b * ar[None, :] + c) % n
                if satisfies(T, identity):
                    out.append((a, b, c))
    return out
