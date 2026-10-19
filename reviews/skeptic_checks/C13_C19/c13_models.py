"""Skeptic check C13-C: model-level checks with own SAT encoding / exhaustive search (no systems/, no lab/).

 wfam   : Theorem 3 (CLM-C13-03): for every one-variable term W with <= 6 leaves, the anchored models of
          (xy)z = x(y W(z)) of size N <= 6 (5 leaves: N <= 7) are exactly the affine tables with a c_W(a) = 1;
          plus Theorem 3 (iv): the set of polynomials c_W over trees with n leaves (n <= 16) equals the set of
          gap-free polynomials with constant term 1 and coefficient sum n (2^(n-2) of them).
 cube   : Theorem 5 (CLM-C13-05): exhaustive N = 2, explicit model N = 3..300; spectrum of x = x(x(xx)) by SAT
          for N <= 12.
 onevar : one-variable laws (CLM-C13-09/10, EXP-C13-07): all laws with <= 5 leaves per side, N <= 16; all laws
          with <= 6 leaves per side, N <= 12.
 divcl  : divisor-closure counterexamples quoted in CLM-C13-07 / EXP-C13-05/06, N <= 9 (3-variable: N <= 8).
 rigid  : EXP-C13-02 selection check (finite vs infinite affine classes of the 199 tested laws) and a sample of
          its non-affine-model claims re-checked.
 c06    : the 17 laws of CLM-C06-10, N <= 12: all models, affine or not.
usage: python3 c13_models.py <task>
"""
import itertools
import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
sys.path.insert(0, HERE)
from c13_lib import (affine_system_of, affine_tab, all_terms, count_models, is_model, read_law, read_term,  # noqa
                     roots_mod, sat_model, show, tree_shapes, label)


def cpoly(W):
    """c_W as a tuple (low first): leaves weighted by a^(number of right steps)."""
    out = Counter()

    def rec(t, r):
        if isinstance(t, str):
            out[r] += 1
        else:
            rec(t[0], r)
            rec(t[1], r + 1)
    rec(W, 0)
    return tuple(out[i] for i in range(max(out) + 1))


def peval(p, a):
    v = 0
    for c in reversed(p):
        v = v * a + c
    return v


def wfam():
    t0 = time.time()
    res = {"mismatch": [], "checked": 0}
    for n_leaves, Nmax in ((1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 6)):
        for sh in tree_shapes(n_leaves):
            W = label(sh, ["z"] * n_leaves)
            law = ((("x", "y"), "z"), ("x", ("y", W)))
            P = cpoly(W)
            for N in range(1, Nmax + 1):
                roots = [a for a in range(N) if (a * peval(P, a) - 1) % N == 0]
                cnt, tabs = count_models(N, [law], limit=200)
                affine_ok = all(any(T == affine_tab(N, a) for a in roots) for T in tabs)
                res["checked"] += 1
                if cnt != len(roots) or not affine_ok:
                    res["mismatch"].append((show(W), N, cnt, len(roots)))
        print("W leaves", n_leaves, "done; mismatches so far", len(res["mismatch"]), flush=True)
    # Theorem 3 (iv)
    S = {1: {(1,)}}
    for n in range(2, 17):
        cur = set()
        for k in range(1, n):
            for p in S[k]:
                for q in S[n - k]:
                    r = list(p) + [0] * (len(q) + 1 - len(p))
                    for i, c in enumerate(q):
                        r[i + 1] += c
                    cur.add(tuple(r))
        S[n] = cur
    iv = {}
    for n in range(1, 17):
        gapfree = set()
        # compositions of n - 1 into positive parts -> coefficients of a, a^2, ...
        for m in range(0, n):
            for comp in itertools.combinations(range(1, n - 1), m - 1) if m >= 1 else [()]:
                if m == 0:
                    if n == 1:
                        gapfree.add((1,))
                    continue
                cuts = (0,) + comp + (n - 1,)
                parts = tuple(cuts[i + 1] - cuts[i] for i in range(len(cuts) - 1))
                gapfree.add((1,) + parts)
        iv[n] = (len(S[n]), len(gapfree), S[n] == gapfree)
    res["iv"] = iv
    res["elapsed_s"] = round(time.time() - t0, 1)
    print("Theorem 3 (iv): n -> (#c_W, #gap-free, equal):", iv)
    print("W-family mismatches:", res["mismatch"][:5], "checked", res["checked"])
    json.dump(res, open(os.path.join(OUT, "c13_wfam.json"), "w"), indent=1)


def cube():
    law = read_law("x=x(x(xx))")
    res = {}
    # exhaustive N = 2: free entries 0*1 and 1*1
    m2 = [(a, b) for a in range(2) for b in range(2) if is_model([[1, a], [0, b]], [law])]
    res["N2_models"] = m2

    def cubeop(N):
        T = [[0] * N for _ in range(N)]
        for x in range(N):
            for y in range(N):
                if y == 0:
                    T[x][y] = (x + 1) % N
                elif x == 0:
                    T[x][y] = 2 % N if y == 1 else 0
                else:
                    T[x][y] = x if y == x else 0
        return T
    res["explicit_bad"] = [N for N in range(3, 301) if not is_model(cubeop(N), [law])]
    res["sat"] = {N: sat_model(N, [law])[0] for N in range(1, 13)}
    print("cube law: N=2 models", m2, "explicit model failures (3..300):", res["explicit_bad"], "SAT:", res["sat"])
    json.dump(res, open(os.path.join(OUT, "c13_cube.json"), "w"), indent=1)


def onevar_laws(max_leaves):
    terms = all_terms(("x",), max_leaves)
    return [(s, t) for s, t in itertools.combinations(terms, 2)]


def onevar():
    t0 = time.time()
    res = {}
    for ml, Nmax in ((5, 16), (6, 12)):
        laws = onevar_laws(ml)
        cls = Counter()
        detail = {}
        for s, t in laws:
            spec = []
            for N in range(1, Nmax + 1):
                st, _ = sat_model(N, [(s, t)])
                assert st in ("SAT", "UNSAT")
                if st == "SAT":
                    spec.append(N)
            missing = [N for N in range(1, Nmax + 1) if N not in spec]
            if spec == [1]:
                c = "{1}"
            elif not missing:
                c = "all"
            elif max(spec) <= Nmax // 2 and all(N % 1 == 0 for N in spec):
                c = "finite:" + ",".join(map(str, spec))
            else:
                c = "missing:" + ",".join(map(str, missing))
            cls[c] += 1
            detail[f"{show(s)} = {show(t)}"] = spec
        # divisor-closure violations
        viol = [k for k, sp in detail.items() if any(N % d == 0 and d not in sp for N in sp for d in range(1, N))]
        res[f"le{ml}"] = {"n_laws": len(laws), "Nmax": Nmax, "classes": dict(cls), "divisor_violations": len(viol)}
        print(f"one-variable laws <= {ml} leaves ({len(laws)} laws, N <= {Nmax}):", dict(cls),
              "divisor-closure violations:", len(viol), flush=True)
        res[f"le{ml}_spectra"] = detail
        for name in ("x = (xx)x", "x = ((xx)x)x", "x = (((xx)x)x)x"):
            s, t = read_law(name.replace(" ", ""))
            key = f"{show(s)} = {show(t)}"
            if key in detail:
                print("   ", name, detail[key])
    res["elapsed_s"] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(OUT, "c13_onevar.json"), "w"), indent=1)


def divcl():
    res = {}
    for name, Nmax in (("((xy)x)y=(y(xx))x", 9), ("(xx)(xy)=y(y(yy))", 9), ("x(xy)=y(y(xx))", 9),
                       ("(x(xy))x=x((zz)y)", 8), ("((xx)x)x=(y(xx))y", 8), ("x=x(x(xx))", 8)):
        law = read_law(name)
        spec = {}
        for N in range(1, Nmax + 1):
            st, _ = sat_model(N, [law], budget=5_000_000)
            spec[N] = st
        res[name] = spec
        print(name, {N: s[0] for N, s in spec.items()}, flush=True)
    json.dump(res, open(os.path.join(OUT, "c13_divcl.json"), "w"), indent=1)


def rigid():
    import sympy as sp
    A = sp.Symbol("a")
    d = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "results",
                                    "EXP-C13-02.json")))["results"]
    rows = d["rows"]
    kinds = Counter()
    finite_rows = []
    for r in rows:
        s, t = read_law(r["law"].replace(" ", ""))
        sysm = affine_system_of(s, t)
        polys = [sp.Poly(list(reversed(p)), A) for p in sysm]
        g = polys[0]
        for q in polys[1:]:
            g = sp.gcd(g, q)
        kind = "infinite" if g.degree() >= 1 else "finite"
        kinds[kind] += 1
        if kind == "finite":
            finite_rows.append((r["law"], r["affine_spectrum_head"], r["non_affine_N"], r["unknown_N"]))
    print("EXP-C13-02 tested laws by affine-spectrum kind:", dict(kinds))
    print("laws with FINITE affine spectrum among them:", len(finite_rows))
    for fr in finite_rows[:12]:
        print("   ", fr)
    nonrig_fin = sum(1 for fr in finite_rows if fr[2])
    inf_rows = [r for r in rows if (r["law"], r["affine_spectrum_head"], r["non_affine_N"], r["unknown_N"])
                not in finite_rows]
    print("non-rigid among finite-class laws:", nonrig_fin, "; infinite-class laws:", len(inf_rows),
          "non-rigid among them:", sum(1 for r in inf_rows if r["non_affine_N"]))
    all678 = [r["law"] for r in inf_rows if all(n in r["non_affine_N"] for n in (6, 7, 8))]
    print("infinite-class laws with non-affine models at every N = 6, 7, 8:", len(all678))
    # re-check a sample of non-affine claims with own SAT (affine tables blocked)
    sample = ["x=x(x(xx))", "(xx)x=(yy)y"]
    chk = {}
    for name in sample:
        law = read_law(name)
        chk[name] = {N: sat_model(N, [law], block_affine=True)[0] for N in range(2, 9)}
        print("non-affine models,", name, chk[name], flush=True)
    rigid_law = d["rigid"][0]
    law = read_law(rigid_law.replace(" ", ""))
    chk[rigid_law] = {N: sat_model(N, [law], block_affine=True)[0] for N in range(2, 9)}
    print("the 'rigid' law", rigid_law, chk[rigid_law])
    json.dump({"kinds": dict(kinds), "finite_rows": finite_rows, "nonrigid_finite": nonrig_fin,
               "n_infinite": len(inf_rows), "inf_all678": len(all678), "sat": chk},
              open(os.path.join(OUT, "c13_rigid.json"), "w"), indent=1)


def c06():
    names = ["x(yz)=((zx)x)y", "x(yz)=((zx)y)x", "x(yz)=((zy)x)x", "(xy)z=y((zx)y)", "(xy)z=y((zy)x)",
             "(xy)z=z((yx)z)", "(xy)z=z((yz)x)", "x(yz)=y((yx)z)", "x(yz)=((xx)y)z", "x(yz)=((xx)z)y",
             "x(yz)=((xy)x)z", "x(yz)=((xy)y)z", "x(yz)=((xy)z)x", "x(yz)=((xy)z)y", "x(yz)=((xz)x)y",
             "x(yz)=((xz)y)x", "x(yz)=((xz)y)y"]
    res = {}
    for name in names:
        law = read_law(name)
        spec = []
        nonaff = []
        for N in range(1, 10):
            cnt, tabs = count_models(N, [law], limit=50)
            if cnt:
                spec.append(N)
            for T in tabs:
                if not any(T == affine_tab(N, a) for a in range(N)):
                    nonaff.append((N, T))
        res[name] = {"spectrum_le9": spec, "non_affine": nonaff}
        print(name, spec, "non-affine:", nonaff, flush=True)
    json.dump(res, open(os.path.join(OUT, "c13_c06laws.json"), "w"), indent=1)


if __name__ == "__main__":
    globals()[sys.argv[1]]()
