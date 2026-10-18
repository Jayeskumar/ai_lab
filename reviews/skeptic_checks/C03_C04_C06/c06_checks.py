"""Skeptic checks for cycle C06 (successor-anchored magmas x*0 = x+1 mod N).
Own term parser and own CNF encoding (pysat used only as the SAT solver); nothing from systems/ or lab/.

Usage: python3 c06_checks.py <part> ...   parts: basic, family, conj10, golden, laver, products, affine, monoids
Outputs: out/c06_<part>.json
"""
import itertools
import json
import math
import sys
import time
from pathlib import Path

from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


# ------------------------------------------------------------ terms
def parse(s):
    s = s.replace(" ", "")
    pos = 0

    def atom():
        nonlocal pos
        if s[pos] == "(":
            pos += 1
            e = expr()
            assert s[pos] == ")"
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

    e = expr()
    assert pos == len(s)
    return e


def show(t):
    if isinstance(t, str):
        return t
    a = show(t[0]) if isinstance(t[0], str) else "(" + show(t[0]) + ")"
    b = show(t[1]) if isinstance(t[1], str) else "(" + show(t[1]) + ")"
    return a + b


def law(s):
    a, b = s.split("=")
    return parse(a), parse(b)


def term_vars(t, acc=None):
    acc = [] if acc is None else acc
    if isinstance(t, str):
        if t not in acc:
            acc.append(t)
    else:
        term_vars(t[0], acc)
        term_vars(t[1], acc)
    return acc


def evaluate(T, t, env):
    if isinstance(t, str):
        return env[t]
    return T[evaluate(T, t[0], env)][evaluate(T, t[1], env)]


def satisfies(T, lw):
    N = len(T)
    vs = term_vars(lw[0], term_vars(lw[1]))
    for vals in itertools.product(range(N), repeat=len(vs)):
        env = dict(zip(vs, vals))
        if evaluate(T, lw[0], env) != evaluate(T, lw[1], env):
            return False
    return True


def anchored(T):
    N = len(T)
    return all(T[x][0] == (x + 1) % N for x in range(N))


# ------------------------------------------------------------ own CNF encoding
class Enc:
    def __init__(self, N, laws):
        self.N = N
        self.nv = 0
        self.cl = []
        self.cell = {}
        for a in range(N):
            for b in range(1, N):
                vs = [self.new() for _ in range(N)]
                self.cell[a, b] = vs
                self.cl.append(vs[:])
                for i in range(N):
                    for j in range(i + 1, N):
                        self.cl.append([-vs[i], -vs[j]])
        self.memo = {}
        self.trivially_unsat = False
        for lw in laws:
            vs = term_vars(lw[0], term_vars(lw[1]))
            for vals in itertools.product(range(N), repeat=len(vs)):
                env = dict(zip(vs, vals))
                A = self.node(lw[0], env)
                B = self.node(lw[1], env)
                self.equal(A, B)

    def new(self):
        self.nv += 1
        return self.nv

    # a node value is ('c', k) constant or ('v', [lits]) one-hot vector
    def node(self, t, env):
        N = self.N
        if isinstance(t, str):
            return ("c", env[t])
        L = self.node(t[0], env)
        R = self.node(t[1], env)
        if L[0] == "c" and R[0] == "c":
            a, b = L[1], R[1]
            if b == 0:
                return ("c", (a + 1) % N)
            return ("v", self.cell[a, b])
        key = (show(t), L if L[0] == "c" else ("v", tuple(L[1])), R if R[0] == "c" else ("v", tuple(R[1])))
        if key in self.memo:
            return self.memo[key]
        X = [self.new() for _ in range(N)]
        avals = [L[1]] if L[0] == "c" else range(N)
        bvals = [R[1]] if R[0] == "c" else range(N)
        for a in avals:
            for b in bvals:
                pre = []
                if L[0] == "v":
                    pre.append(-L[1][a])
                if R[0] == "v":
                    pre.append(-R[1][b])
                if b == 0:
                    self.cl.append(pre + [X[(a + 1) % N]])
                else:
                    for c in range(N):
                        self.cl.append(pre + [-self.cell[a, b][c], X[c]])
        for i in range(N):
            for j in range(i + 1, N):
                self.cl.append([-X[i], -X[j]])
        res = ("v", X)
        self.memo[key] = res
        return res

    def equal(self, A, B):
        if A[0] == "c" and B[0] == "c":
            if A[1] != B[1]:
                self.trivially_unsat = True
                self.cl.append([])
        elif A[0] == "c":
            self.cl.append([B[1][A[1]]])
        elif B[0] == "c":
            self.cl.append([A[1][B[1]]])
        else:
            for c in range(self.N):
                self.cl.append([-A[1][c], B[1][c]])
                self.cl.append([-B[1][c], A[1][c]])

    def table(self, model):
        pos = set(l for l in model if l > 0)
        N = self.N
        T = [[(a + 1) % N if b == 0 else None for b in range(N)] for a in range(N)]
        for (a, b), vs in self.cell.items():
            for c in range(N):
                if vs[c] in pos:
                    T[a][b] = c
        return T


def models(N, laws, limit=None, solver="cd15"):
    """Enumerate anchored models (tables); returns (list_of_tables_or_count, complete)."""
    if N == 1:
        return [[[0]]], True
    E = Enc(N, laws)
    if E.trivially_unsat:
        return [], True
    out = []
    with Solver(name=solver, bootstrap_with=[c for c in E.cl if c]) as S:
        while S.solve():
            T = E.table(S.get_model())
            assert anchored(T) and all(satisfies(T, lw) for lw in laws), "encoding error"
            out.append(T)
            if limit and len(out) >= limit:
                return out, False
            S.add_clause([-E.cell[a, b][T[a][b]] for a in range(N) for b in range(1, N)])
    return out, True


def exists(N, laws, solver="cd15"):
    ms, _ = models(N, laws, limit=1, solver=solver)
    return len(ms) > 0, (ms[0] if ms else None)


def count_models(N, laws, limit=None):
    ms, complete = models(N, laws, limit)
    return len(ms), complete


# ------------------------------------------------------------ parts
LD = law("x(yz)=(xy)(xz)")
RD = law("(xy)z=(xz)(yz)")
ASSOC = law("x(yz)=(xy)z")
LP = law("x(yz)=y(xz)")
RP = law("(xy)z=(xz)y")
ODD = law("(xy)z=x((yz)z)")
GOLD = law("(xy)z=x(y(zz))")
ODD_TWIN = law("(xy)z=x((zy)y)")
GOLD_TWIN = law("(xy)z=x(z(yy))")


def part_basic():
    out = {}
    t0 = time.time()
    out["LD_counts_N1_10"] = {N: count_models(N, [LD])[0] for N in range(1, 11)}
    out["RD_counts_N1_10"] = {N: count_models(N, [RD])[0] for N in range(1, 11)}
    out["assoc_counts_N1_10"] = {N: count_models(N, [ASSOC])[0] for N in range(1, 11)}
    out["RP_counts_N1_6"] = {N: count_models(N, [RP])[0] for N in range(1, 7)}
    out["RP_expected"] = {N: N ** (N - 1) for N in range(1, 7)}
    out["LP_counts_N1_5"] = {N: count_models(N, [LP])[0] for N in range(1, 6)}
    odd = {}
    for N in range(1, 14):
        ms, _ = models(N, [ODD])
        good = all(all(T[x][y] == (x + 1 + y * pow(2, -1, N)) % N for x in range(N) for y in range(N)) for T in ms) if N % 2 else None
        odd[N] = {"models": len(ms), "is_x+1+y/2": good}
    out["odd_law_N1_13"] = odd
    # the RD and assoc models are the claimed formulas
    out["RD_model_is_x+1"] = all(all(T[x][y] == (x + 1) % N for x in range(N) for y in range(N))
                                 for N in range(1, 9) for T in models(N, [RD])[0])
    out["assoc_model_is_x+y+1"] = all(all(T[x][y] == (x + y + 1) % N for x in range(N) for y in range(N))
                                      for N in range(1, 9) for T in models(N, [ASSOC])[0])
    # RP models all of the form x + c(y)
    out["RP_models_are_x+c(y)_N_le_5"] = all(all((T[x][y] - x) % N == T[0][y] for x in range(N) for y in range(N))
                                              for N in range(1, 6) for T in models(N, [RP])[0])
    out["seconds"] = round(time.time() - t0, 1)
    return out


def part_golden(Nmax=13):
    out = {}
    for name, lw in (("golden", GOLD), ("golden_twin", GOLD_TWIN), ("odd_twin", ODD_TWIN)):
        res = {}
        for N in range(1, Nmax + 1):
            t0 = time.time()
            ms, _ = models(N, [lw])
            aff = []
            for T in ms:
                a = (T[0][1] - 1) % N if N > 1 else 0
                aff.append(all(T[x][y] == (x + 1 + a * y) % N for x in range(N) for y in range(N)))
            res[N] = {"models": len(ms), "all_affine": all(aff), "a": sorted(((T[0][1] - 1) % N) for T in ms) if N > 1 else [0],
                      "sec": round(time.time() - t0, 1)}
            print(name, N, res[N], flush=True)
        out[name] = res
    roots = {N: sorted(a for a in range(N) if (a * a + a - 1) % N == 0) for N in range(1, Nmax + 1)}
    out["roots_a2+a-1"] = roots
    out["golden_counts_equal_roots"] = all(out["golden"][N]["models"] == len(roots[N]) for N in range(1, Nmax + 1))
    out["golden_a_equal_roots"] = all(out["golden"][N]["a"] == roots[N] for N in range(2, Nmax + 1))
    out["twin_counts_equal_golden"] = all(out["golden_twin"][N]["models"] == out["golden"][N]["models"] for N in range(1, Nmax + 1))
    out["oddtwin_counts_1_iff_odd"] = all(out["odd_twin"][N]["models"] == (N % 2) for N in range(1, Nmax + 1))
    # number theory of the spectrum: N with a root, N <= 2000, versus the description 5^e m
    def predicted(N):
        if N % 25 == 0 or N % 2 == 0:
            return False
        m = N // 5 if N % 5 == 0 else N
        p = 2
        mm = m
        while p * p <= mm:
            while mm % p == 0:
                if p % 5 not in (1, 4):
                    return False
                mm //= p
            p += 1
        return mm == 1 or mm % 5 in (1, 4)
    spec = [N for N in range(1, 2001) if any((a * a + a - 1) % N == 0 for a in range(N))]
    out["spectrum_description_ok_N_le_2000"] = spec == [N for N in range(1, 2001) if predicted(N)]
    out["spectrum_first_terms"] = spec[:12]
    # number of roots = 2^omega(m)
    def omega(m):
        k, p = 0, 2
        while p * p <= m:
            if m % p == 0:
                k += 1
                while m % p == 0:
                    m //= p
            p += 1
        return k + (m > 1)
    out["root_count_2^omega_ok_N_le_2000"] = all(
        sum((a * a + a - 1) % N == 0 for a in range(N)) == 2 ** omega(N // 5 if N % 5 == 0 else N) for N in spec)
    return out


def family_laws():
    """All laws x(yz) = t, (xy)z = t, t with 3 or 4 leaves using exactly x, y, z (own enumeration)."""
    def shapes(k):
        if k == 0:
            return [None]
        out = []
        for i in range(k):
            for a in shapes(i):
                for b in shapes(k - 1 - i):
                    out.append((a, b))
        return out

    def fill(sh, it):
        if sh is None:
            return next(it)
        a = fill(sh[0], it)
        b = fill(sh[1], it)
        return (a, b)

    def nleaves(sh):
        return 1 if sh is None else nleaves(sh[0]) + nleaves(sh[1])

    rhs = []
    for k in (2, 3):
        for sh in shapes(k):
            for lab in itertools.product("xyz", repeat=nleaves(sh)):
                if set(lab) == {"x", "y", "z"}:
                    rhs.append(fill(sh, iter(lab)))
    laws = []
    for lhs in (parse("x(yz)"), parse("(xy)z")):
        for t in rhs:
            if t != lhs:
                laws.append((lhs, t))
    return laws


def part_family(Nmax=6):
    laws = family_laws()
    rows = {}
    t0 = time.time()
    for lw in laws:
        name = f"{show(lw[0])} = {show(lw[1])}"
        rows[name] = [N for N in range(1, Nmax + 1) if exists(N, [lw])[0]]
    classes = {"trivial only": [], "all": [], "restricted": []}
    for k, v in rows.items():
        if v == [1]:
            classes["trivial only"].append(k)
        elif v == list(range(1, Nmax + 1)):
            classes["all"].append(k)
        else:
            classes["restricted"].append(k)
    restricted = {k: rows[k] for k in classes["restricted"]}
    # compare with the lab's EXP-C06-03 classification
    lab = json.load(open(ROOT / "results/EXP-C06-03.json"))["results"]
    labrows = {r["law"]: r["sat"] for r in lab["rows"]}
    disagree = [k for k in rows if labrows.get(k) != rows[k]]
    return {"n_laws": len(laws), "class_counts": {k: len(v) for k, v in classes.items()},
            "restricted": restricted, "disagreements_with_lab": disagree, "missing_in_lab": [k for k in rows if k not in labrows],
            "seconds": round(time.time() - t0, 1)}


CONJ10_13 = ["x(yz)=((zx)x)y", "x(yz)=((zx)y)x", "x(yz)=((zy)x)x", "(xy)z=y((zx)y)", "(xy)z=y((zy)x)",
             "(xy)z=z((yx)z)", "(xy)z=z((yz)x)"]
CONJ10_12 = ["x(yz)=y((yx)z)", "x(yz)=((xx)y)z", "x(yz)=((xx)z)y", "x(yz)=((xy)x)z", "x(yz)=((xy)y)z",
             "x(yz)=((xy)z)x", "x(yz)=((xy)z)y", "x(yz)=((xz)x)y", "x(yz)=((xz)y)x", "x(yz)=((xz)y)y"]


def part_conj10(Nmin=1, Nmax=12):
    out = {}
    for s in CONJ10_13 + CONJ10_12:
        lw = law(s)
        sp = []
        times = {}
        for N in range(Nmin, Nmax + 1):
            t0 = time.time()
            ok, T = exists(N, [lw])
            times[N] = round(time.time() - t0, 1)
            if ok:
                sp.append(N)
        expected = [1, 3] if s in CONJ10_13 else [1, 2]
        out[s] = {"spectrum": sp, "expected_within_range": [n for n in expected if Nmin <= n <= Nmax],
                  "ok": sp == [n for n in expected if Nmin <= n <= Nmax], "max_sec": max(times.values())}
        print(s, out[s], flush=True)
    out["all_ok"] = all(v["ok"] for v in out.values() if isinstance(v, dict))
    return out


def part_laver():
    """Own Laver-table construction and LD check; own run of the recursion for general N <= 64."""
    import numpy as np
    out = {}

    def rec(N):
        # 1-based rows p = N..1: L[N][q] = q, L[p][1] = p+1, L[p][q+1] = L[L[p][q]][p+1]
        L = [[0] * (N + 2) for _ in range(N + 2)]
        for q in range(1, N + 1):
            L[N][q] = q
        for p in range(N - 1, 0, -1):
            L[p][1] = p + 1
            for q in range(1, N):
                v = L[p][q]
                if v <= p:          # the needed row is not yet available: recursion breaks down
                    return None
                L[p][q + 1] = L[v][p + 1]
        return np.array([[L[p][q] - 1 for q in range(1, N + 1)] for p in range(1, N + 1)], dtype=np.int64)

    def is_ld(T):
        n = len(T)
        for a in range(n):
            if not np.array_equal(T[a][T], T[np.ix_(T[a], T[a])]):
                return False
        return True

    res = {}
    for N in range(1, 65):
        T = rec(N)
        res[N] = "breaks" if T is None else ("LD" if is_ld(T) else "not LD")
    out["recursion_LD_N_le_64"] = [N for N, v in res.items() if v == "LD"]
    out["recursion_outcomes_non_pow2"] = sorted({v for N, v in res.items() if N & (N - 1)})
    ok = {}
    for n in range(0, 9):
        T = rec(2 ** n)
        ok[2 ** n] = bool(T is not None and is_ld(T) and all(T[x][0] == (x + 1) % (2 ** n) for x in range(2 ** n)))
    out["A_n_LD_exhaustive_N_le_256"] = ok
    # Lean's laver3 table equals our A_3
    lean = [[1, 3, 5, 7, 1, 3, 5, 7], [2, 3, 6, 7, 2, 3, 6, 7], [3, 7, 3, 7, 3, 7, 3, 7], [4, 5, 6, 7, 4, 5, 6, 7],
            [5, 7, 5, 7, 5, 7, 5, 7], [6, 7, 6, 7, 6, 7, 6, 7], [7, 7, 7, 7, 7, 7, 7, 7], [0, 1, 2, 3, 4, 5, 6, 7]]
    out["lean_laver3_equals_own_A3"] = rec(8).tolist() == lean
    # SAT models of LD at N = 8 and 4 equal the Laver tables
    for N in (2, 4, 8):
        ms, _ = models(N, [LD])
        out[f"LD_SAT_models_N{N}_equal_Laver"] = len(ms) == 1 and ms[0] == rec(N).tolist()
    return out


def crt_product(T1, T2):
    N, M = len(T1), len(T2)
    NM = N * M
    inv = {}
    for x in range(NM):
        inv[(x % N, x % M)] = x
    return [[inv[(T1[x % N][y % N], T2[x % M][y % M])] for y in range(NM)] for x in range(NM)]


def part_products():
    out = {}
    cases = [("left-permutable", LP, 2, 3), ("left-permutable", LP, 3, 4), ("right-permutable", RP, 4, 5),
             ("odd", ODD, 3, 5), ("odd", ODD, 5, 7), ("golden", GOLD, 5, 11), ("assoc", ASSOC, 4, 9),
             ("x(yz)=y(x(yz))", law("x(yz)=y(x(yz))"), 2, 3), ("x(yz)=y(x(yz))", law("x(yz)=y(x(yz))"), 4, 5)]
    for name, lw, N, M in cases:
        m1, _ = models(N, [lw], limit=3)
        m2, _ = models(M, [lw], limit=3)
        good = 0
        tot = 0
        for T1 in m1:
            for T2 in m2:
                P = crt_product(T1, T2)
                tot += 1
                good += anchored(P) and satisfies(P, lw)
        out[f"{name} {N}x{M}"] = f"{good}/{tot}"
    return out


def part_affine():
    """Affine models x*y = x + a y + 1 for the 16 affine-only laws of CLM-C06-10 and the 4 laws of CLM-C06-09."""
    import sympy as sp
    a, x, y, z = sp.symbols("a x y z")

    def ev(t):
        if isinstance(t, str):
            return {"x": x, "y": y, "z": z}[t]
        return sp.expand(ev(t[0]) + a * ev(t[1]) + 1)

    out = {}
    for s in CONJ10_13 + CONJ10_12 + ["x(yz)=y(x(yz))", "x(yz)=y(x(xz))", "x(yz)=y(y(xz))", "x(yz)=(yx)(yz)"]:
        lw = law(s)
        diff = sp.Poly(sp.expand(ev(lw[0]) - ev(lw[1])), x, y, z)
        conds = [sp.Poly(c, a) for c in diff.coeffs()]
        G = sp.groebner([c.as_expr() for c in conds], a, domain=sp.QQ)
        no_common_root = list(G.exprs) == [1]
        spec = [N for N in range(1, 301) if any(all(int(c.eval(av)) % N == 0 for c in conds) for av in range(N))]
        out[s] = {"conditions": [str(c.as_expr()) for c in conds], "no_common_complex_root": no_common_root,
                  "affine_spectrum_N_le_300": spec}
    return out


def part_monoids():
    """Count commutative monoid structures on {0..N-1} with identity 0 (own brute force), N <= 5."""
    out = {}
    for N in range(1, 6):
        els = list(range(1, N))
        pairs = [(i, j) for i in els for j in els if i <= j]
        cnt = 0
        # backtracking over the symmetric table on non-identity elements with associativity pruning
        T = [[None] * N for _ in range(N)]
        for i in range(N):
            T[0][i] = i
            T[i][0] = i

        def assoc_ok():
            for p in range(N):
                for q in range(N):
                    pq = T[p][q]
                    if pq is None:
                        continue
                    for r in range(N):
                        qr = T[q][r]
                        if qr is None:
                            continue
                        lhs = T[pq][r]
                        rhs = T[p][qr]
                        if lhs is not None and rhs is not None and lhs != rhs:
                            return False
            return True

        def bt(k):
            nonlocal cnt
            if k == len(pairs):
                cnt += 1
                return
            i, j = pairs[k]
            for v in range(N):
                T[i][j] = T[j][i] = v
                if assoc_ok():
                    bt(k + 1)
            T[i][j] = T[j][i] = None

        bt(0)
        out[N] = cnt
    out["matches_LP_claim"] = [out[N] for N in range(1, 6)] == [1, 2, 9, 94, 1486]
    return out


def part_selftest():
    """Encoder completeness/soundness: SAT model counts == brute-force counts over all anchored tables, N <= 3."""
    laws = family_laws() + [LD, RD, ASSOC, LP, RP, law("x(xy)=xy"), law("x(yx)=xy"), law("(xy)y=xy")]
    bad = []
    for N in (2, 3):
        cells = [(a, b) for a in range(N) for b in range(1, N)]
        tables = []
        for vals in itertools.product(range(N), repeat=len(cells)):
            T = [[(a + 1) % N] + [0] * (N - 1) for a in range(N)]
            for (a, b), v in zip(cells, vals):
                T[a][b] = v
            tables.append(T)
        for lw in laws:
            bf = sum(satisfies(T, lw) for T in tables)
            sat = count_models(N, [lw])[0]
            if bf != sat:
                bad.append([show(lw[0]) + "=" + show(lw[1]), N, bf, sat])
    return {"laws": len(laws), "sizes": [2, 3], "mismatches": bad}


PARTS = {"basic": part_basic, "family": part_family, "conj10": part_conj10, "golden": part_golden,
         "laver": part_laver, "products": part_products, "affine": part_affine, "monoids": part_monoids,
         "selftest": part_selftest}

if __name__ == "__main__":
    args = sys.argv[1:]
    name = args[0]
    kw = {}
    if name == "conj10" and len(args) >= 3:
        kw = {"Nmin": int(args[1]), "Nmax": int(args[2])}
    if name == "golden" and len(args) >= 2:
        kw = {"Nmax": int(args[1])}
    t0 = time.time()
    res = PARTS[name](**kw)
    res["_seconds"] = round(time.time() - t0, 1)
    suffix = "" if not kw else "_" + "_".join(str(v) for v in kw.values())
    (OUT / f"c06_{name}{suffix}.json").write_text(json.dumps(res, indent=1, default=str))
    print(f"== {name} ({res['_seconds']} s)")
    print(json.dumps(res, default=str)[:4000], flush=True)
