"""Skeptic's own toolkit for cycle C13 (anchored magmas).  Does NOT import systems/ or lab/.

Terms: a variable is a str ('x', 'y', 'z'); a product is a 2-tuple (left, right).
Anchored magma of size N: a table T on Z/N with T[x][0] = x + 1.
Affine table with parameter a: x*y = x + a*y + 1.
"""
from __future__ import annotations

import itertools
from functools import lru_cache
from math import gcd

import numpy as np

# ----------------------------------------------------------------------------------------- terms


def tree_shapes(leaves: int):
    """All binary tree shapes with the given number of leaves (leaf = None)."""
    if leaves == 1:
        return [None]
    out = []
    for k in range(1, leaves):
        for a in tree_shapes(k):
            for b in tree_shapes(leaves - k):
                out.append((a, b))
    return out


def label(shape, labels):
    it = iter(labels)

    def rec(s):
        if s is None:
            return next(it)
        left = rec(s[0])
        right = rec(s[1])
        return (left, right)
    return rec(shape)


def nleaves(t):
    return 1 if isinstance(t, str) else nleaves(t[0]) + nleaves(t[1])


def all_terms(variables, max_leaves):
    out = []
    for n in range(1, max_leaves + 1):
        for sh in tree_shapes(n):
            for lab in itertools.product(variables, repeat=n):
                out.append(label(sh, lab))
    return out


def show(t):
    """Juxtaposition notation (left factor without parentheses if it is a variable)."""
    if isinstance(t, str):
        return t
    a = show(t[0]) if isinstance(t[0], str) else "(" + show(t[0]) + ")"
    b = show(t[1]) if isinstance(t[1], str) else "(" + show(t[1]) + ")"
    return a + b


def read_term(s):
    """Parse juxtaposition notation; juxtaposition associates to the left: xyz = (xy)z."""
    s = s.replace(" ", "").replace("*", "")
    toks = list(s)
    i = 0

    def factor():
        nonlocal i
        if toks[i] == "(":
            i += 1
            e = seq()
            assert toks[i] == ")"
            i += 1
            return e
        c = toks[i]
        i += 1
        return c

    def seq():
        nonlocal i
        e = factor()
        while i < len(toks) and toks[i] != ")":
            e = (e, factor())
        return e
    e = seq()
    assert i == len(toks)
    return e


def read_law(s):
    a, b = s.split("=")
    return read_term(a), read_term(b)


def term_vars(t, acc=None):
    if acc is None:
        acc = []
    if isinstance(t, str):
        if t not in acc:
            acc.append(t)
    else:
        term_vars(t[0], acc)
        term_vars(t[1], acc)
    return acc


def subst(t, m):
    return m.get(t, t) if isinstance(t, str) else (subst(t[0], m), subst(t[1], m))


def law_orbit_key(s, t, variables):
    """Canonical key of the law s = t under all permutations of `variables` and exchange of sides."""
    keys = []
    for perm in itertools.permutations(variables):
        m = dict(zip(variables, perm))
        a, b = show(subst(s, m)), show(subst(t, m))
        keys.append(min((a, b), (b, a)))
    return min(keys)


def laws_up_to_iso(variables, max_leaves):
    terms = all_terms(variables, max_leaves)
    seen = {}
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            k = law_orbit_key(terms[i], terms[j], variables)
            if k not in seen:
                seen[k] = (terms[i], terms[j])
    return seen


# ----------------------------------------------------------------------------------------- polynomials (lists, low first)


def ptrim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    n = max(len(p), len(q))
    return ptrim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def pscale_a(p):
    return ptrim([0] + list(p)) if p else []


def pneg(p):
    return [-c for c in p]


@lru_cache(maxsize=None)
def affine(t):
    """(coeffs, const) of term t under x*y = x + a*y + 1; coeffs: tuple of (var, poly-tuple)."""
    if isinstance(t, str):
        return ((t, (1,)),), ()
    cl, dl = affine(t[0])
    cr, dr = affine(t[1])
    co = {v: list(p) for v, p in cl}
    for v, p in cr:
        co[v] = padd(co.get(v, []), pscale_a(p))
    d = padd(padd(list(dl), pscale_a(list(dr))), [1])
    return tuple(sorted((v, tuple(p)) for v, p in co.items() if p)), tuple(d)


def affine_system_of(s, t):
    """Set of non-zero difference polynomials (as tuples, sign-normalised: leading coeff > 0)."""
    cs, ds = affine(s)
    ct, dt = affine(t)
    cs, ct = dict(cs), dict(ct)
    out = set()
    for v in set(cs) | set(ct):
        d = padd(list(cs.get(v, ())), pneg(list(ct.get(v, ()))))
        if d:
            out.add(tuple(d) if d[-1] > 0 else tuple(-c for c in d))
    d = padd(list(ds), pneg(list(dt)))
    if d:
        out.add(tuple(d) if d[-1] > 0 else tuple(-c for c in d))
    return frozenset(out)


def peval(p, a):
    v = 0
    for c in reversed(p):
        v = v * a + c
    return v


def roots_mod(system, N):
    """All a in [0, N) that are common roots of the system modulo N (direct search)."""
    return [a for a in range(N) if all(peval(p, a) % N == 0 for p in system)]


def has_root_table(system, Nmax):
    """For N = 1..Nmax: does the system have a common root mod N?  Direct search (vectorised)."""
    a = np.arange(Nmax, dtype=object)
    vals = [np.array([peval(p, int(x)) for x in range(Nmax)], dtype=object) for p in system]
    out = {}
    for N in range(1, Nmax + 1):
        ok = np.ones(N, dtype=bool)
        for v in vals:
            ok &= np.array([int(x) % N == 0 for x in v[:N]], dtype=bool)
        out[N] = bool(ok.any())
    return out


# ----------------------------------------------------------------------------------------- evaluation in a table


def eval_term(T, t, asg):
    if isinstance(t, str):
        return asg[t]
    return T[eval_term(T, t[0], asg)][eval_term(T, t[1], asg)]


def is_model(T, laws):
    N = len(T)
    for s, t in laws:
        vs = term_vars(s, term_vars(t, []))
        for vals in itertools.product(range(N), repeat=len(vs)):
            asg = dict(zip(vs, vals))
            if eval_term(T, s, asg) != eval_term(T, t, asg):
                return False
    return True


def affine_tab(N, a):
    return [[(x + a * y + 1) % N for y in range(N)] for x in range(N)]


# ----------------------------------------------------------------------------------------- SAT (own encoding, pysat as solver)


class AnchoredSAT:
    """CNF for 'an anchored magma on Z/N satisfying the laws'.

    Variables tab[x,y,c] <=> x*y = c (exactly one c per cell), anchor unit clauses.  For each law instance and
    each compound subterm occurrence (memoised by (subterm, values of its variables)) value variables
    val[c] with: tab[a,b,c] & val_left[a] & val_right[b] -> val[c], and at most one val[c].  Both sides'
    values are then forced equal.  Exactness: in any model the forced value variables equal the true values
    (by induction, since exactly-one on tab and at-least-one implications), so the CNF is satisfiable iff a
    model exists."""

    def __init__(self, N, laws, block_affine=False):
        from pysat.formula import IDPool
        self.N = N
        self.pool = IDPool()
        self.cl = []
        R = range(N)
        self.tab = {(x, y, c): self.pool.id(("t", x, y, c)) for x in R for y in R for c in R}
        for x in R:
            for y in R:
                lits = [self.tab[x, y, c] for c in R]
                self.cl.append(lits)
                for i in range(N):
                    for j in range(i + 1, N):
                        self.cl.append([-lits[i], -lits[j]])
        for x in R:
            self.cl.append([self.tab[x, 0, (x + 1) % N]])
        self.memo = {}
        self.unsat = False
        for s, t in laws:
            vs = term_vars(s, term_vars(t, []))
            for vals in itertools.product(R, repeat=len(vs)):
                asg = dict(zip(vs, vals))
                A = self.enc(s, asg)
                B = self.enc(t, asg)
                if isinstance(A, int) and isinstance(B, int):
                    if A != B:
                        self.unsat = True
                elif isinstance(A, int):
                    self.cl.append([B[A]])
                elif isinstance(B, int):
                    self.cl.append([A[B]])
                else:
                    for c in R:
                        self.cl.append([-A[c], B[c]])
                        self.cl.append([-B[c], A[c]])
        if block_affine:
            for a in R:
                self.cl.append([-self.tab[x, y, (x + a * y + 1) % N] for x in R for y in R])

    def enc(self, t, asg):
        if isinstance(t, str):
            return asg[t]
        key = (t, tuple(sorted((v, asg[v]) for v in term_vars(t, []))))
        if key in self.memo:
            return self.memo[key]
        N = self.N
        R = range(N)
        val = {c: self.pool.id(("v", key, c)) for c in R}
        A = self.enc(t[0], asg)
        B = self.enc(t[1], asg)
        for a in ([A] if isinstance(A, int) else R):
            for b in ([B] if isinstance(B, int) else R):
                for c in R:
                    clause = [-self.tab[a, b, c], val[c]]
                    if not isinstance(A, int):
                        clause.append(-A[a])
                    if not isinstance(B, int):
                        clause.append(-B[b])
                    self.cl.append(clause)
        for i in range(N):
            for j in range(i + 1, N):
                self.cl.append([-val[i], -val[j]])
        self.memo[key] = val
        return val

    def table(self, model):
        pos = set(l for l in model if l > 0)
        N = self.N
        T = [[None] * N for _ in range(N)]
        for (x, y, c), v in self.tab.items():
            if v in pos:
                T[x][y] = c
        return T


def sat_model(N, laws, block_affine=False, budget=None):
    """('SAT', table) / ('UNSAT', None) / ('UNKNOWN', None)."""
    from pysat.solvers import Solver
    enc = AnchoredSAT(N, laws, block_affine)
    if enc.unsat:
        return "UNSAT", None
    with Solver(name="cadical153", bootstrap_with=enc.cl) as s:
        if budget:
            s.conf_budget(budget)
            r = s.solve_limited()
        else:
            r = s.solve()
        if r is None:
            return "UNKNOWN", None
        if not r:
            return "UNSAT", None
        T = enc.table(s.get_model())
        assert is_model(T, laws) and all(T[x][0] == (x + 1) % N for x in range(N)), "SAT model fails check"
        return "SAT", T


def count_models(N, laws, limit=1000):
    """Number of anchored models (all tables), by blocking clauses; returns (count, tables)."""
    from pysat.solvers import Solver
    enc = AnchoredSAT(N, laws)
    if enc.unsat:
        return 0, []
    out = []
    with Solver(name="cadical153", bootstrap_with=enc.cl) as s:
        while s.solve():
            T = enc.table(s.get_model())
            assert is_model(T, laws)
            out.append(T)
            s.add_clause([-enc.tab[x, y, T[x][y]] for x in range(N) for y in range(N)])
            if len(out) >= limit:
                break
    return len(out), out


# ----------------------------------------------------------------------------------------- offset congruence closure (own)


class OffsetCC:
    """Own implementation of congruence closure with integer offsets for anchored magmas.

    Nodes: 0 is the element 0; every other node is a table entry created for a pair of (already named)
    arguments.  An *element* is a pair (node, k) meaning 'value of node + k'.  Union-find over nodes with
    offsets: value(node) = value(parent) + off.  Facts used: law instances (both sides equal), the anchor
    (u * 0 = u + 1, used only when the right argument is literally (root 0, offset 0)) and functionality
    (equal arguments => equal entries), closed to a fixpoint after every round.  Every derived equation
    'node + k1 = node + k2' gives N | k1 - k2; g is the gcd of all such k1 - k2."""

    def __init__(self):
        self.par = [0]
        self.off = [0]
        self.entries = {}      # (elem, elem) normalised -> node
        self.g = 0

    def find(self, n):
        """(root, offset) with value(n) = value(root) + offset."""
        off = 0
        m = n
        while self.par[m] != m:
            off += self.off[m]
            m = self.par[m]
        r = m
        # path compression
        m = n
        o = off
        while self.par[m] != m:
            nxt = self.par[m]
            o_next = o - self.off[m]
            self.par[m] = r
            self.off[m] = o
            m = nxt
            o = o_next
        return r, off

    def norm(self, e):
        r, o = self.find(e[0])
        return (r, e[1] + o)

    def new_node(self):
        self.par.append(len(self.par))
        self.off.append(0)
        return len(self.par) - 1

    def merge(self, e1, e2):
        """Record value(e1) = value(e2). Returns True if the partition changed."""
        (r1, k1), (r2, k2) = self.norm(e1), self.norm(e2)
        if r1 == r2:
            if k1 != k2:
                self.g = gcd(self.g, abs(k1 - k2))
            return False
        # value(r1) + k1 = value(r2) + k2; attach the non-zero root below the other one, keep node 0 a root
        if r1 == 0:
            r1, k1, r2, k2 = r2, k2, r1, k1
        self.par[r1] = r2
        self.off[r1] = k2 - k1
        return True

    def entry(self, a, b):
        a, b = self.norm(a), self.norm(b)
        if b == (0, 0):
            return (a[0], a[1] + 1)
        key = (a, b)
        n = self.entries.get(key)
        if n is None:
            n = self.new_node()
            self.entries[key] = n
        return self.norm((n, 0))

    def value(self, t, asg):
        if isinstance(t, str):
            return self.norm(asg[t])
        return self.entry(self.value(t[0], asg), self.value(t[1], asg))

    def close(self):
        """Congruence + anchor closure to a fixpoint."""
        changed_any = False
        while True:
            changed = False
            new = {}
            for (a, b), n in list(self.entries.items()):
                a2, b2 = self.norm(a), self.norm(b)
                if b2 == (0, 0):
                    changed |= self.merge((n, 0), (a2[0], a2[1] + 1))
                    continue
                k = (a2, b2)
                if k in new:
                    changed |= self.merge((new[k], 0), (n, 0))
                else:
                    new[k] = n
            self.entries = new
            if not changed:
                break
            changed_any = True
        return changed_any


def own_closure_bound(laws, values=(0, 1, 2, 3, -1), rounds=4, node_values=0, max_nodes=20000):
    cc = OffsetCC()
    vs = sorted({v for s, t in laws for side in (s, t) for v in term_vars(side, [])})
    for _ in range(rounds):
        before = (len(cc.par), cc.g, len(cc.entries))
        elems = [(0, c) for c in values] + [(n, 0) for n in range(1, min(len(cc.par), 1 + node_values))]
        for s, t in laws:
            for combo in itertools.product(elems, repeat=len(vs)):
                asg = dict(zip(vs, combo))
                cc.merge(cc.value(s, asg), cc.value(t, asg))
                if cc.g == 1:
                    return 1
        cc.close()
        if cc.g == 1:
            return 1
        if len(cc.par) > max_nodes:
            break
        if (len(cc.par), cc.g, len(cc.entries)) == before:
            break
    return cc.g


# ----------------------------------------------------------------------------------------- exhaustive small tables


def all_anchored_tables(N):
    """Array (count, N, N) of all anchored tables of size N (column 0 fixed)."""
    free = N * (N - 1)
    cnt = N ** free
    idx = np.arange(cnt, dtype=np.int64)
    T = np.zeros((cnt, N, N), dtype=np.int8)
    for x in range(N):
        T[:, x, 0] = (x + 1) % N
    pos = 0
    for x in range(N):
        for y in range(1, N):
            T[:, x, y] = (idx // (N ** pos)) % N
            pos += 1
    return T


def law_holds_all_tables(Ts, s, t):
    """Boolean vector: which tables (array (M,N,N)) satisfy s = t."""
    M, N, _ = Ts.shape
    vs = term_vars(s, term_vars(t, []))
    ok = np.ones(M, dtype=bool)
    rows = np.arange(M)
    for vals in itertools.product(range(N), repeat=len(vs)):
        asg = dict(zip(vs, vals))

        def ev(u):
            if isinstance(u, str):
                return np.full(M, asg[u], dtype=np.int64)
            a = ev(u[0])
            b = ev(u[1])
            return Ts[rows, a, b].astype(np.int64)
        ok &= ev(s) == ev(t)
        if not ok.any():
            break
    return ok
