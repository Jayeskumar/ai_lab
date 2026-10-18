"""Skeptic checks for cycle C05 (spectra of single-identity magma laws).

Independent of systems/magma.py: own term parser and enumerator, own evaluator, own CNF encoding
(one exactly-one value vector per tree node and per assignment, no subterm sharing); pysat is used
only as a SAT solver (kissat / CaDiCaL 1.9.5 by default, not the lab's CaDiCaL 1.5.3 / Glucose).

Usage: python3 c05_checks.py <part>
  tables    : re-check every Lean-certified table and the small Lean facts by brute force
  brute3    : all 115 identities, all magmas of order <= 3 by brute force (model counts, quasigroups)
  census    : SAT spectra n = 1..6 (and 7, 8 for the non-full ones) vs EXP-C05-01/02
  affine    : affine models over Z_n (n <= 6) for all 115 identities vs EXP-C05-05 / CLM-C05-06
  frontier  : the frontier gaps and memberships of CLM-C05-07/08 (sound constraints only)
  conj09    : structured model search at orders 8 and 10 for laws 677, 1313 (CLM-C05-09)
Writes out/c05_<part>.json.
"""
import itertools
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
ROOT = HERE.parents[2]


# ---------------------------------------------------------------- terms (own)
def parse(s):
    s = s.replace(" ", "").replace("*", "")
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


def leaves(t):
    return [t] if isinstance(t, str) else leaves(t[0]) + leaves(t[1])


def trees(k):
    if k == 0:
        return [None]
    out = []
    for i in range(k):
        for a in trees(i):
            for b in trees(k - 1 - i):
                out.append((a, b))
    return out


def fill(shape, labels):
    it = iter(labels)

    def go(s):
        return next(it) if s is None else (go(s[0]), go(s[1]))
    return go(shape)


def nontrivial_identities():
    """All terms t over {x, y} with 2..4 operations, x occurring, first and last leaf = y."""
    out = []
    for k in (2, 3, 4):
        for sh in trees(k):
            nl = k + 1
            for mid in itertools.product("xy", repeat=nl - 2):
                if "x" not in mid:
                    continue
                out.append(fill(sh, ("y",) + mid + ("y",)))
    return out


def mirror(t):
    return t if isinstance(t, str) else (mirror(t[1]), mirror(t[0]))


# ---------------------------------------------------------------- evaluation (own)
def evaluate(T, t, env):
    if isinstance(t, str):
        return env[t]
    return T[evaluate(T, t[0], env)][evaluate(T, t[1], env)]


def satisfies(T, t):
    n = len(T)
    return all(evaluate(T, t, {"x": x, "y": y}) == x for x in range(n) for y in range(n))


def satisfies_np(T, t):
    """Vectorised check over all (x, y)."""
    T = np.asarray(T)
    n = T.shape[0]
    X, Y = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")

    def ev(t):
        if t == "x":
            return X
        if t == "y":
            return Y
        return T[ev(t[0]), ev(t[1])]
    return bool(np.all(ev(t) == X))


# ---------------------------------------------------------------- CNF (own)
class Enc:
    def __init__(self, n):
        self.n = n
        self.nv = 0
        self.cl = []

    def new(self):
        self.nv += 1
        return self.nv

    def eo(self, lits):
        self.cl.append(list(lits))
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                self.cl.append([-lits[i], -lits[j]])


def encode(t, n, latin_rows=False, latin_cols=False, symbreak=True, idempotent=False, latin_both=False,
           automorphism=None):
    E = Enc(n)
    R = range(n)
    m = [[[E.new() for c in R] for b in R] for a in R]
    for a in R:
        for b in R:
            E.eo([m[a][b][c] for c in R])
    for xv in R:
        for yv in R:
            env = {"x": xv, "y": yv}

            def node(s):
                """returns ('const', value) or ('vars', [lit per value])"""
                if isinstance(s, str):
                    return ("const", env[s])
                L, Rr = node(s[0]), node(s[1])
                u = [E.new() for _ in R]
                E.eo(u)
                ls = [L[1]] if L[0] == "const" else list(R)
                rs = [Rr[1]] if Rr[0] == "const" else list(R)
                for l in ls:
                    for r in rs:
                        for c in R:
                            clause = [-m[l][r][c], u[c]]
                            if L[0] == "vars":
                                clause.append(-L[1][l])
                            if Rr[0] == "vars":
                                clause.append(-Rr[1][r])
                            E.cl.append(clause)
                return ("vars", u)

            top = node(t)
            if top[0] == "const":
                if top[1] != xv:
                    E.cl.append([])
            else:
                E.cl.append([top[1][xv]])
    if latin_rows or latin_both:
        for a in R:
            for c in R:
                E.eo([m[a][b][c] for b in R])
    if latin_cols or latin_both:
        for b in R:
            for c in R:
                E.eo([m[a][b][c] for a in R])
    if symbreak and n > 1 and not idempotent and automorphism is None:
        E.cl.append([m[0][0][0], m[0][0][1]])
    if idempotent:
        for a in R:
            E.cl.append([m[a][a][a]])
    if automorphism is not None:
        sig = automorphism
        for a in R:
            for b in R:
                for c in R:
                    E.cl.append([-m[a][b][c], m[sig[a]][sig[b]][sig[c]]])
    return E, m


def solve(t, n, solver="cadical195", budget_s=None, **kw):
    E, m = encode(t, n, **kw)
    if any(len(c) == 0 for c in E.cl):
        return "UNSAT", None
    with Solver(name=solver, bootstrap_with=E.cl) as S:
        if budget_s is None:
            ok = S.solve()
        else:
            import threading
            timer = threading.Timer(budget_s, lambda: S.interrupt())
            timer.start()
            ok = S.solve_limited(expect_interrupt=True)
            timer.cancel()
        if ok is None:
            return "UNKNOWN", None
        if not ok:
            return "UNSAT", None
        model = set(l for l in S.get_model() if l > 0)
    T = [[next(c for c in range(n) if m[a][b][c] in model) for b in range(n)] for a in range(n)]
    assert satisfies(T, t), "model fails the law"
    return "SAT", T


def sound_kw(t):
    """Constraints that cannot change model existence: Latin rows for t = y*(...), Latin columns for t = (...)*y
    (Lean left_mul_bijective_of_law and its mirror), symmetry break 0*0 in {0, 1}."""
    return {"latin_rows": t[0] == "y", "latin_cols": t[1] == "y", "symbreak": True}


# ---------------------------------------------------------------- parts
def part_tables():
    src = (ROOT / "proofs/lean/Infinity/C05_Magmas.lean").read_text()
    laws = {"T4": "(yx)(xy)", "T5": "(yx)(xy)", "E467_order9": "y(x(x(yy)))", "E677_order5": "y(x((yx)y))",
            "E677_order7": "y(x((yx)y))", "E677_order9": "y(x((yx)y))", "E883_order10": "y((xy)(yy))",
            "E1286_order9": "y(((xy)x)y)", "E1313_order9": "y(((yx)x)y)", "E1516_order9": "(yy)(x(xy))",
            "E1719_order10": "(yy)((xx)y)", "nand2": "(yx)(x(yy))"}
    res = {}
    for name, law in laws.items():
        mt = re.search(r"def " + name + r" : Fin (\d+) → Fin \d+ → Fin \d+ := fun a b =>\s*\n?\s*!\[(.*?)\] a b", src, re.S)
        n = int(mt.group(1))
        rows = re.findall(r"!\[([0-9, ]+)\]", "![" + mt.group(2) + "]")
        T = [[int(v) for v in r.split(",")] for r in rows]
        assert len(T) == n and all(len(r) == n for r in T), name
        t = parse(law)
        res[name] = {"n": n, "law": "x = " + law, "satisfies": satisfies(T, t),
                     "quasigroup": all(len(set(r)) == n for r in T) and all(len(set(col)) == n for col in zip(*T)),
                     "idempotent": all(T[i][i] == i for i in range(n))}
    T4 = [[0, 3, 1, 0], [0, 2, 2, 2], [2, 0, 1, 3], [1, 3, 1, 3]]
    res["T4_row1"] = T4[1]
    # no model of law 167 / law 66 of order 2 and 3 (brute force)
    for law, nm in (("(yx)(xy)", "167"), ("y(x(yy))", "66")):
        t = parse(law)
        for n in (2, 3):
            cnt = sum(satisfies_np(np.array(v).reshape(n, n), t) for v in itertools.product(range(n), repeat=n * n))
            res[f"law{nm}_models_order{n}"] = int(cnt)
    # no affine model of x = (yx)(x(yy)) over Z_2; affine spectrum n <= 6
    t = parse("(yx)(x(yy))")
    aff = {}
    for n in range(1, 7):
        ar = np.arange(n)
        aff[n] = [(a, b, c) for a in range(n) for b in range(n) for c in range(n)
                  if satisfies_np((a * ar[:, None] + b * ar[None, :] + c) % n, t)]
    res["affine_models_(yx)(x(yy))"] = {n: len(v) for n, v in aff.items()}
    return res


def part_brute3():
    ids = nontrivial_identities()
    lab = {r["identity"]: r for r in json.loads((ROOT / "results/EXP-C05-01.json").read_text())["results"]["rows"]}
    tabs = {n: [np.array(v).reshape(n, n) for v in itertools.product(range(n), repeat=n * n)] for n in (1, 2, 3)}
    out, mism, nonqg = {}, [], []
    for t in ids:
        key = show(t) + " = x"
        counts = {}
        has_nonqg = False
        for n in (1, 2, 3):
            models = [T for T in tabs[n] if satisfies_np(T, t)]
            counts[n] = len(models)
            for T in models:
                if not (all(len(set(r)) == n for r in T) and all(len(set(c)) == n for c in T.T)):
                    has_nonqg = True
        out[key] = counts
        if has_nonqg:
            nonqg.append(key)
        L = lab.get(key)
        if L is None:
            mism.append([key, "not in lab census"])
        else:
            labc = {int(k): v[0] for k, v in L["models_total_iso_complete_n1_3"].items()}
            if labc != counts:
                mism.append([key, counts, labc])
    return {"n_identities": len(ids), "n_distinct": len({show(t) for t in ids}),
            "lab_identities_not_generated": sorted(set(lab) - set(out)),
            "model_count_mismatches_vs_EXP-C05-01": mism,
            "identities_with_nonquasigroup_models_order_le_3": len(nonqg)}


def part_census():
    ids = nontrivial_identities()
    lab = {r["identity"]: r for r in json.loads((ROOT / "results/EXP-C05-01.json").read_text())["results"]["rows"]}
    lab2 = json.loads((ROOT / "results/EXP-C05-02.json").read_text())["results"]
    res, mism, unknown = {}, [], []
    t0 = time.time()
    for t in ids:
        key = show(t) + " = x"
        pat = ""
        for n in range(1, 7):
            st, _ = solve(t, n, budget_s=60, **sound_kw(t))
            pat += {"SAT": "1", "UNSAT": "0", "UNKNOWN": "?"}[st]
            if st == "UNKNOWN":
                unknown.append([key, n])
        res[key] = pat
        if lab[key]["spectrum_1_6"] != pat:
            mism.append([key, pat, lab[key]["spectrum_1_6"]])
    full = sum(p == "111111" for p in res.values())
    only1 = sum(p == "100000" for p in res.values())
    # n = 7, 8 for the non-full ones
    ext = {}
    for t in ids:
        key = show(t) + " = x"
        if res[key] == "111111":
            continue
        pat = res[key]
        for n in (7, 8):
            st, _ = solve(t, n, budget_s=90, **sound_kw(t))
            pat += {"SAT": "1", "UNSAT": "0", "UNKNOWN": "?"}[st]
        ext[key] = pat
    from collections import Counter
    return {"patterns_1_6": dict(Counter(res.values())), "full_1_6": full, "only_n1_on_1_6": only1,
            "mismatches_vs_EXP-C05-01": mism, "unknown_1_6": unknown,
            "patterns_1_8_nonfull": dict(Counter(ext.values())), "per_identity_1_8": ext,
            "lab_EXP-C05-02_keys": list(lab2.keys())[:20], "seconds": round(time.time() - t0, 1)}


def part_affine():
    ids = nontrivial_identities()
    out = {}
    for t in ids:
        key = show(t) + " = x"
        sp = []
        for n in range(1, 7):
            ar = np.arange(n)
            ok = any(satisfies_np((a * ar[:, None] + b * ar[None, :] + c) % n, t)
                     for a in range(n) for b in range(n) for c in range(n))
            if ok:
                sp.append(n)
        out[key] = sp
    lab = {r["identity"]: r["spectrum_1_6"] for r in json.loads((ROOT / "results/EXP-C05-01.json").read_text())["results"]["rows"]}
    full_no_affine = {k: v for k, v in out.items() if lab[k] == "111111" and v != [1, 2, 3, 4, 5, 6]}
    affine_outside_spectrum = [k for k, v in out.items() if any(lab[k][n - 1] == "0" for n in v)]
    restricted_with_nonaffine_members = [k for k, v in out.items() if lab[k] not in ("111111", "100000")
                                         and any(lab[k][n - 1] == "1" and n not in v for n in range(1, 7))]
    return {"full_spectrum_but_not_all_affine": full_no_affine,
            "affine_model_outside_SAT_spectrum": affine_outside_spectrum,
            "n_restricted_with_members_without_affine_model": len(restricted_with_nonaffine_members)}


FRONTIER = {501: "y(y(x(xy)))", 677: "y(x((yx)y))", 883: "y((xy)(yy))", 1076: "y((x(xy))y)",
            1083: "y((x(yx))y)", 1286: "y(((xy)x)y)", 1313: "y(((yx)x)y)", 1516: "(yy)(x(xy))",
            1719: "(yy)((xx)y)", 467: "y(x(x(yy)))"}
GAPS = {501: [2, 3, 6, 7], 677: [2, 3, 4, 6], 883: [3, 6], 1076: [8], 1083: [2, 5, 6], 1719: [2]}
MEMBERS = {677: [5, 7, 9], 1286: [9], 1313: [9], 1516: [9], 467: [9]}


def part_frontier():
    res = {"gaps": {}, "members": {}}
    for law, ns in GAPS.items():
        t = parse(FRONTIER[law])
        for n in ns:
            t0 = time.time()
            st, _ = solve(t, n, solver="kissat404", budget_s=600, **sound_kw(t))
            st2 = None
            if n <= 6:     # second, unconstrained run (no Latin rows, no symmetry break) where cheap
                st2, _ = solve(t, n, solver="cadical195", budget_s=300, latin_rows=False, latin_cols=False,
                               symbreak=False)
            res["gaps"][f"{law}@{n}"] = {"kissat_sound_constraints": st, "cadical_no_extra_constraints": st2,
                                         "seconds": round(time.time() - t0, 1)}
            print(law, n, st, st2, flush=True)
    for law, ns in MEMBERS.items():
        t = parse(FRONTIER[law])
        for n in ns:
            t0 = time.time()
            st, T = solve(t, n, solver="cadical195", budget_s=300, **sound_kw(t))
            res["members"][f"{law}@{n}"] = {"status": st, "seconds": round(time.time() - t0, 1)}
            print(law, n, st, flush=True)
    return res


def part_conj09():
    """Look for models of 677 / 1313 at orders 8 and 10 (a model would refute CLM-C05-09)."""
    res = {}
    # (a) affine models over Z_2^3 with matrix coefficients, over Z_8, Z_4 x Z_2, Z_10
    def law_affine_check(t, add, A, B, c, elems):
        def op(u, v):
            return add(add(A(u), B(v)), c)
        for x in elems:
            for y in elems:
                def ev(s):
                    if s == "x":
                        return x
                    if s == "y":
                        return y
                    return op(ev(s[0]), ev(s[1]))
                if ev(t) != x:
                    return False
        return True

    for law in (677, 1313, 1286):
        t = parse(FRONTIER[law])
        found = []
        # Z_2^3, vectors as ints 0..7, matrices as 3 column images
        elems = list(range(8))
        mats = []
        for cols in itertools.product(range(8), repeat=3):
            def M(v, cols=cols):
                r = 0
                for i in range(3):
                    if v >> i & 1:
                        r ^= cols[i]
                return r
            mats.append((cols, M))
        add = lambda u, v: u ^ v
        cnt = 0
        for (ca, A) in mats:
            for (cb, B) in mats:
                for c in (0,):          # constants handled below
                    pass
                # linear part must satisfy the law with c = 0 first (necessary: the law's linear part)
                if law_affine_check(t, add, A, B, 0, elems):
                    found.append(["Z2^3", ca, cb, 0])
                    cnt += 1
        # constant c != 0 with linear part satisfying the homogeneous law is covered by translating; search all c
        for (ca, A) in mats:
            for (cb, B) in mats:
                for c in range(1, 8):
                    if law_affine_check(t, add, A, B, c, elems):
                        found.append(["Z2^3", ca, cb, c])
        # cyclic groups Z_8, Z_10 and Z_4 x Z_2
        for n in (8, 10):
            for a in range(n):
                for b in range(n):
                    for c in range(n):
                        T = [[(a * u + b * v + c) % n for v in range(n)] for u in range(n)]
                        if satisfies(T, t):
                            found.append([f"Z{n}", a, b, c])
        # Z_4 x Z_2: endomorphisms (u1,u2) -> (p u1 + 2 q u2, r u1 + s u2) with p in Z4, q, r, s in Z2
        els = [(u1, u2) for u1 in range(4) for u2 in range(2)]
        ends = [(p, q, r, s) for p in range(4) for q in range(2) for r in range(2) for s in range(2)]
        idx = {e: i for i, e in enumerate(els)}

        def ap(E, u):
            p, q, r, s = E
            return ((p * u[0] + 2 * q * u[1]) % 4, (r * u[0] + s * u[1]) % 2)
        for EA in ends:
            for EB in ends:
                for c in els:
                    T = [[idx[((ap(EA, u)[0] + ap(EB, v)[0] + c[0]) % 4, (ap(EA, u)[1] + ap(EB, v)[1] + c[1]) % 2)]
                          for v in els] for u in els]
                    if satisfies(T, t):
                        found.append(["Z4xZ2", EA, EB, c])
        res[f"affine_{law}"] = found[:5] + ([f"... {len(found)} total"] if len(found) > 5 else [])
    # (b) SAT with extra (unsound-for-UNSAT) structure: idempotent Latin square with an automorphism
    for law in (677, 1313):
        t = parse(FRONTIER[law])
        for n in (8, 10):
            for name, sig in (("cyclic Z_{n-1} fixing n-1", [(i + 1) % (n - 1) for i in range(n - 1)] + [n - 1]),
                              ("regular Z_n", [(i + 1) % n for i in range(n)]),
                              ("two cycles of length n/2", [(i + 1) % (n // 2) for i in range(n // 2)] +
                               [n // 2 + (i + 1) % (n // 2) for i in range(n // 2)])):
                t0 = time.time()
                st, T = solve(t, n, solver="cadical195", budget_s=120, latin_both=True, idempotent=True,
                              automorphism=sig, symbreak=False)
                res[f"{law}@{n} idempotent Latin + automorphism {name}"] = {"status": st, "table": T,
                                                                           "seconds": round(time.time() - t0, 1)}
                print(law, n, name, st, flush=True)
    return res


PARTS = {"tables": part_tables, "brute3": part_brute3, "census": part_census, "affine": part_affine,
         "frontier": part_frontier, "conj09": part_conj09}

if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = PARTS[part]()
    res = {"part": part, "result": res, "wall_seconds": round(time.time() - t0, 1)}
    (OUT / f"c05_{part}.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, default=str)[:4000])
