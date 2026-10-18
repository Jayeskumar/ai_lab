"""Successor-anchored magmas: affine theory, law enumeration and SAT helpers (cycle C13).

An *anchored* magma of size N is a binary operation on Z/N with x*0 = x + 1.  Its *spectrum* for a set of laws
is the set of N admitting a model.  The *affine* anchored tables are x*y = x + a*y + 1 (a in Z/N); under the
anchor these are the only tables of the form alpha*x + beta*y + gamma.

Affine evaluation.  Under x*y = x + a*y + 1 every term t evaluates to a linear form
    t = sum_v C_t[v](a) * v + D_t(a)
with polynomials C, D in Z[a] with non-negative coefficients:  C_{uw} = C_u + a*C_w,  D_{uw} = D_u + a*D_w + 1.
A law s = t holds in the affine table with parameter a (mod N) iff every polynomial of its *affine system*
    {C_s[v] - C_t[v] : v}  u  {D_s - D_t}
vanishes at a modulo N.  Polynomials are tuples of ints (coefficient of a^i at index i), trimmed.
"""

from __future__ import annotations

import itertools
from functools import lru_cache
from math import gcd

import numpy as np
from pysat.solvers import Cadical153

from systems.magma import MagmaSAT, fill, is_var, n_leaves, parse, shapes, to_str, variables

# ------------------------------------------------------------------ polynomials over Z (tuples)


def ptrim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return tuple(p)


def padd(p, q):
    n = max(len(p), len(q))
    return ptrim(tuple((p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)))


def psub(p, q):
    return padd(p, tuple(-c for c in q))


def pshift(p):
    """Multiply by a."""
    return ptrim((0,) + tuple(p)) if p else ()


def peval_mod(p, a, n):
    """Value of p at a (int or numpy array) modulo n (Horner)."""
    v = 0 * a
    for c in reversed(p):
        v = (v * a + c) % n
    return v


def pstr(p, var="a"):
    if not p:
        return "0"
    terms = []
    for i in range(len(p) - 1, -1, -1):
        c = p[i]
        if c == 0:
            continue
        mono = "" if i == 0 else (var if i == 1 else f"{var}^{i}")
        coef = str(abs(c)) if (abs(c) != 1 or i == 0) else ""
        sign = "-" if c < 0 else "+"
        terms.append((sign, coef + mono))
    s = "".join(f" {sg} {t}" for sg, t in terms).strip()
    return s[2:] if s.startswith("+ ") else "-" + s[2:]


ONE = (1,)

# ------------------------------------------------------------------ affine evaluation of terms and laws


@lru_cache(maxsize=None)
def affine_form(t):
    """(C, D) for term t: C is a sorted tuple of (variable, poly) pairs, D a poly."""
    if is_var(t):
        return ((t, ONE),), ()
    Cu, Du = affine_form(t[0])
    Cw, Dw = affine_form(t[1])
    C = dict(Cu)
    for v, p in Cw:
        C[v] = padd(C.get(v, ()), pshift(p))
    return tuple(sorted((v, p) for v, p in C.items() if p)), padd(padd(Du, pshift(Dw)), ONE)


def affine_system(law) -> tuple:
    """Sorted tuple of the non-zero polynomials whose common roots mod N are the affine models of `law`."""
    s, t = law
    Cs, Ds = affine_form(s)
    Ct, Dt = affine_form(t)
    Cs, Ct = dict(Cs), dict(Ct)
    polys = set()
    for v in set(Cs) | set(Ct):
        d = psub(Cs.get(v, ()), Ct.get(v, ()))
        if d:
            polys.add(normalize_sign(d))
    d = psub(Ds, Dt)
    if d:
        polys.add(normalize_sign(d))
    return tuple(sorted(polys))


def normalize_sign(p):
    return p if p[-1] > 0 else tuple(-c for c in p)


def system_of_laws(laws) -> tuple:
    out = set()
    for law in laws:
        out.update(affine_system(law))
    return tuple(sorted(out))


def affine_roots(system, n) -> list[int]:
    """All a in Z/n at which every polynomial of `system` vanishes mod n."""
    a = np.arange(n, dtype=np.int64)
    ok = np.ones(n, dtype=bool)
    for p in system:
        ok &= peval_mod(p, a, n) == 0
    return [int(x) for x in np.nonzero(ok)[0]]


def affine_table(n, a):
    x = np.arange(n).reshape(-1, 1)
    y = np.arange(n).reshape(1, -1)
    return (x + a * y + 1) % n


def factorize(n: int) -> dict:
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def affine_spectrum(system, nmax: int) -> list[int]:
    """Affine spectrum up to nmax, computed through prime powers (CRT, Theorem 1 of proofs/paper/C13.md)."""
    if not system:
        return list(range(1, nmax + 1))
    pp_ok = {}
    out = []
    for n in range(1, nmax + 1):
        ok = True
        for p, e in factorize(n).items():
            q = p ** e
            if q not in pp_ok:
                pp_ok[q] = bool(affine_roots(system, q))
            ok &= pp_ok[q]
        if ok:
            out.append(n)
    return out


# ------------------------------------------------------------------ laws


def terms_up_to(vars_, max_leaves):
    out = []
    for k in range(0, max_leaves):  # k internal nodes -> k+1 leaves
        for sh in shapes(k):
            for lab in itertools.product(vars_, repeat=n_leaves(sh)):
                out.append(fill(sh, lab))
    return out


def canonical_law(s, t, vars_=("x", "y", "z")):
    """Canonical representative of the law s = t under renaming of variables and exchange of sides."""
    best = None
    for perm in itertools.permutations(vars_):
        m = dict(zip(vars_, perm))
        a, b = to_str(_rename(s, m)), to_str(_rename(t, m))
        key = (a, b) if (len(a), a) <= (len(b), b) else (b, a)
        if best is None or key < best:
            best = key
    return best


def _rename(t, m):
    return m.get(t, t) if is_var(t) else (_rename(t[0], m), _rename(t[1], m))


def enumerate_laws(vars_=("x", "y", "z"), max_leaves=4):
    """All laws s = t (s != t) over vars_ with at most max_leaves leaves per side, up to renaming/swap."""
    ts = terms_up_to(vars_, max_leaves)
    seen = set()
    out = []
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            key = canonical_law(ts[i], ts[j], vars_)
            if key in seen:
                continue
            seen.add(key)
            out.append(key)
    return out


def law_from_key(key):
    return parse(key[0]), parse(key[1])


def law_str(key):
    return f"{key[0]} = {key[1]}"


# ------------------------------------------------------------------ cheap necessary condition: zero substitutions


def _zero_eval(t, free):
    """Evaluate t when every variable except `free` is 0, using only the anchor u*0 = u + 1.
    Returns ('c', k) for the constant k, ('v', k) for free + k, or None if an unknown entry is needed."""
    if is_var(t):
        return ("v", 0) if t == free else ("c", 0)
    left, right = t
    r = _zero_eval(right, free)
    if r != ("c", 0):
        return None  # right argument is not the element 0: unknown table entry
    l = _zero_eval(left, free)
    if l is None:
        return None
    return (l[0], l[1] + 1)


def zero_modulus(law) -> int | None:
    """An integer m >= 0 such that every anchored model has size dividing m (m = 1: only the trivial model),
    derived from substitutions of 0; None if no substitution is decisive."""
    s, t = law
    vs = sorted(set(variables(s)) | set(variables(t)))
    g = 0
    decisive = False
    for free in vs + [None]:
        a, b = _zero_eval(s, free), _zero_eval(t, free)
        if a is None or b is None:
            continue
        if a[0] != b[0]:
            return 1  # free + k = constant for all values of free
        d = abs(a[1] - b[1])
        if d:
            g = gcd(g, d)
            decisive = True
    return g if decisive else None


# ------------------------------------------------------------------ SAT


def anchor_clauses(n):
    return lambda S: [[S.v[x, 0, (x + 1) % n]] for x in range(n)]


def anchored_status(laws, n, budget=2_000_000, exclude_affine=False):
    """'SAT' / 'UNSAT' / 'UNKNOWN' for an anchored model of size n (optionally excluding all affine tables)."""
    S = MagmaSAT(n, laws, extra=anchor_clauses(n))
    if any(len(c) == 0 for c in S.clauses):
        return "UNSAT", None
    clauses = list(S.clauses)
    if exclude_affine:
        for a in range(n):
            T = affine_table(n, a)
            clauses.append([-S.v[x, y, int(T[x, y])] for x in range(n) for y in range(n)])
    with Cadical153(bootstrap_with=clauses) as sol:
        sol.conf_budget(budget)
        ok = sol.solve_limited()
        if ok is None:
            return "UNKNOWN", None
        if not ok:
            return "UNSAT", None
        return "SAT", S.table_from_model(sol.get_model())


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def divisor_violations(spec_status: dict) -> list:
    """Pairs (N, d) with N in the spectrum and a proper divisor d not in it (UNKNOWN counts as unresolved)."""
    out = []
    for n, st in spec_status.items():
        if st != "SAT":
            continue
        for d in divisors(n)[:-1]:
            if spec_status.get(d) == "UNSAT":
                out.append((n, d))
    return out


# ------------------------------------------------------------------ affine classes and rigidity profiles


def affine_classes(vars_=("x", "y", "z"), max_leaves=4, nmax=200):
    """Map spectrum (tuple of N <= nmax) -> list of (system, [law keys]) for all laws of the family."""
    from collections import defaultdict
    groups = defaultdict(list)
    for k in enumerate_laws(vars_, max_leaves):
        groups[affine_system(law_from_key(k))].append(k)
    spec = defaultdict(list)
    for sysm, ks in groups.items():
        spec[tuple(affine_spectrum(sysm, nmax))].append((sysm, ks))
    return spec


def law_size(key):
    return len(key[0]) + len(key[1])


def rigidity_profile(laws, sizes, budget=2_000_000):
    """For each N: number of affine models, and whether a NON-affine anchored model exists."""
    sysm = system_of_laws(laws)
    out = {}
    for n in sizes:
        roots = affine_roots(sysm, n) if sysm else list(range(n))
        st, T = anchored_status(laws, n, budget=budget, exclude_affine=True)
        out[n] = {"affine": len(roots), "non_affine": st,
                  "example": T.tolist() if (T is not None and n <= 5) else None}
    return out


def is_affine_table(T):
    """(True, a) if T is the affine anchored table x + a*y + 1, else (False, None)."""
    T = np.asarray(T)
    n = T.shape[0]
    if n == 1:
        return True, 0
    a = int((T[0, 1] - 1) % n)
    return bool(np.array_equal(T, affine_table(n, a))), a
