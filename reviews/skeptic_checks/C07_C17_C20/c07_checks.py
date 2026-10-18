"""Skeptic checks for cycle C07 (mex operations).  Independent of systems/ and lab/:
tables come from my own C program mextab.c (definition-level recursion) and, for a cross-check,
from a pure-Python set implementation below.  Lab results are only *read* for comparison.

usage: python3 c07_checks.py <part>
parts: crosscheck census formulas jacobsthal bitfacts periodic diagonals
"""
import itertools
import json
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MEXTAB = os.path.join(HERE, "mextab")
MASKNAME = {1: "x", 2: "y", 3: "x^y", 4: "z", 5: "x^z", 6: "y^z", 7: "x^y^z"}


def idx_of(L, R, masks):
    return (L << 8) | (R << 7) | sum(1 << (m - 1) for m in masks)


def decode(idx):
    return (idx >> 8) & 1, (idx >> 7) & 1, [m for m in range(1, 8) if idx & (1 << (m - 1))]


def name(idx):
    L, R, masks = decode(idx)
    parts = (["L"] if L else []) + (["R"] if R else []) + [f"D[{MASKNAME[m]}]" for m in masks]
    return "+".join(parts) if parts else "empty"


def lab_order():
    """The lab's enumeration order of specs (needed only to pick the same group representatives)."""
    out = []
    for L in (0, 1):
        for R in (0, 1):
            for r in range(8):
                for D in itertools.combinations(range(1, 8), r):
                    out.append(idx_of(L, R, D))
    return out


def run_mextab(args):
    subprocess.run(["nice", "-n", "10", MEXTAB] + [str(a) for a in args], check=True)


def load_tables(path, nr, nc):
    if not os.path.exists(path) and os.path.basename(path) == "mex64_all.bin":
        run_mextab(["rect", 64, 64, path])        # binary tables are regenerated on demand (not kept)
    a = np.fromfile(path, dtype=np.int32)
    return a.reshape(-1, nr, nc).astype(np.int64)


def py_table(idx, n):
    """Plain-Python mex table from the definition (sets), for cross-checking the C program."""
    L, R, masks = decode(idx)
    f = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            S = set()
            if L:
                for i in range(a):
                    S.add(f[i][b])
            if R:
                for j in range(b):
                    S.add(f[a][j])
            for i in range(a):
                for j in range(b):
                    x, y, z = f[i][b], f[a][j], f[i][j]
                    for m in masks:
                        S.add((x if m & 1 else 0) ^ (y if m & 2 else 0) ^ (z if m & 4 else 0))
            v = 0
            while v in S:
                v += 1
            f[a][b] = v
    return f


def nim_mul(x, y):
    """Nim-multiplication via Fermat 2-powers (Conway): F (x) F = F + F/2."""
    if x < 2 or y < 2:
        return x * y
    L = 1
    while (1 << (2 * L)) <= max(x, y):
        L *= 2
    F = 1 << L
    x1, x0 = x >> L, x & (F - 1)
    y1, y0 = y >> L, y & (F - 1)
    z0 = nim_mul(x0, y0)
    z1 = nim_mul(x1, y1)
    z01 = nim_mul(x0 ^ x1, y0 ^ y1)
    return ((z01 ^ z0) << L) ^ z0 ^ nim_mul(z1, F >> 1)


def assoc_witness(T):
    """All evaluable violating triples in [0,n)^3 (count) and the first one in lexicographic order."""
    n = T.shape[0]
    first, count, evaluated = None, 0, 0
    for a in range(n):
        ab = T[a, :]                                  # a*b for all b
        okb = ab < n
        for b in range(n):
            if not okb[b]:
                continue
            left = T[ab[b], :]                        # (a*b)*c for all c
            bc = T[b, :]
            okc = bc < n
            right = np.where(okc, T[a, np.where(okc, bc, 0)], -1)
            bad = okc & (left != right)
            evaluated += int(okc.sum())
            if bad.any():
                count += int(bad.sum())
                if first is None:
                    c = int(np.argmax(bad))
                    first = (a, b, c)
    return first, count, evaluated


def part_crosscheck():
    n = 16
    path = os.path.join(OUT, "mex16_all.bin")
    run_mextab(["rect", n, n, path])
    C = load_tables(path, n, n)
    t0 = time.time()
    mism = []
    for idx in range(512):
        P = np.array(py_table(idx, n))
        if not np.array_equal(P, C[idx]):
            mism.append(name(idx))
    res = {"window": n, "specs": 512, "mismatches_C_vs_python": mism, "seconds": round(time.time() - t0, 1)}
    # the C 64x64 tables restricted to 16x16 must agree with the 16x16 run (a rectangle is exact)
    C64 = load_tables(os.path.join(OUT, "mex64_all.bin"), 64, 64)
    res["c64_top_left_equals_c16"] = bool(np.array_equal(C64[:, :16, :16], C))
    return res


def part_census():
    C = load_tables(os.path.join(OUT, "mex64_all.bin"), 64, 64)
    n = 64
    groups = {}
    for idx in lab_order():
        groups.setdefault(C[idx].tobytes(), []).append(idx)
    ops = list(groups.values())
    comm = [g for g in ops if np.array_equal(C[g[0]], C[g[0]].T)]
    res = {"specs": 512, "distinct_operations_64": len(ops), "commutative": len(comm)}
    assoc_ops, nonassoc_specs, witnesses = [], 0, {}
    for g in ops:
        T = C[g[0]]
        first, count, evaluated = assoc_witness(T)
        if first is None:
            assoc_ops.append(g)
        else:
            a, b, c = first
            # re-verify the witness by direct look-ups
            assert T[T[a, b], c] != T[a, T[b, c]]
            for idx in g:
                witnesses[name(idx)] = [a, b, c, int(T[T[a, b], c]), int(T[a, T[b, c]])]
            nonassoc_specs += len(g)
    res["associative_operations_64"] = len(assoc_ops)
    res["associative_specs_64"] = sum(len(g) for g in assoc_ops)
    res["nonassociative_specs_with_witness"] = nonassoc_specs
    res["associative_groups"] = [[name(i) for i in g] for g in assoc_ops]
    # closure of commutative operations on [0,2), [0,4), [0,16)
    notclosed = []
    for g in comm:
        T = C[g[0]]
        if not all((T[:k, :k] < k).all() for k in (2, 4, 16)):
            notclosed.append(name(g[0]))
    res["commutative_not_closed_2_4_16"] = len(notclosed)
    dxy = C[idx_of(0, 0, [3])]
    res["D[x^y] f(2,3)"] = int(dxy[2, 3])
    res["D[x^y] commutative"] = bool(np.array_equal(dxy, dxy.T))
    # zero identity / absorbing in the commutative ones (Theorem 2 corollary) on [0,64)
    res["commutative_zero_neither"] = [name(g[0]) for g in comm
                                       if not ((C[g[0]][0, :] == 0).all() or (C[g[0]][0, :] == np.arange(n)).all())]
    # Theorem 2 on all 512 specs: L,R both -> f(0,b)=b, f(a,0)=a; neither -> 0
    t2 = []
    for idx in range(512):
        L, R, _ = decode(idx)
        T = C[idx]
        ok = (np.array_equal(T[0, :], np.arange(n) if R else np.zeros(n)) and
              np.array_equal(T[:, 0], np.arange(n) if L else np.zeros(n)))
        if not ok:
            t2.append(name(idx))
    res["theorem2_violations_all_512"] = t2
    # compare with the lab's stored census
    lab = json.load(open(os.path.join(ROOT, "results", "EXP-C07-01.json")))["results"]
    lab_groups = sorted(sorted(r["specs"]) for r in lab["rows"])
    my_groups = sorted(sorted(name(i) for i in g) for g in ops)
    res["same_partition_as_lab"] = lab_groups == my_groups
    lab_assoc = sorted(sorted(r["specs"]) for r in lab["rows"] if r["associative_window"])
    res["same_associative_groups_as_lab"] = lab_assoc == sorted(sorted(x) for x in res["associative_groups"])
    res["witness_examples"] = dict(list(witnesses.items())[:12])
    json.dump(witnesses, open(os.path.join(OUT, "c07_assoc_witnesses.json"), "w"), indent=0)
    return res


def formula(nm, a, b):
    if nm == "empty":
        return 0
    if nm == "L":
        return a
    if nm == "R":
        return b
    if nm == "D[x]":
        return a if b > 0 else 0
    if nm == "D[y]":
        return b if a > 0 else 0
    if nm == "D[z]":
        return min(a, b)
    if nm == "L+R":
        return a ^ b
    if nm == "D[x^y^z]":
        return nim_mul(a, b)
    if nm == "L+R+D[z]":
        return a + b
    if nm == "D[x]+D[y]":
        return 0 if a == 0 or b == 0 else ((a - 1) ^ (b - 1)) + 1
    if nm == "D[x]+D[y]+D[z]":
        return 0 if a == 0 or b == 0 else a + b - 1
    raise KeyError(nm)


def part_formulas():
    """The 11 canonical formulas and the 33 further specs of the same groups on [0,128)^2;
    my nim-product is checked against Conway's small table first."""
    assert [nim_mul(2, 2), nim_mul(2, 3), nim_mul(3, 3), nim_mul(4, 4), nim_mul(2, 4), nim_mul(8, 8)] == [3, 1, 2, 6, 8, 13]
    # nim-product associativity / distributivity spot check on [0,64)
    rng = np.random.default_rng(7)
    for _ in range(3000):
        a, b, c = (int(v) for v in rng.integers(0, 256, 3))
        assert nim_mul(nim_mul(a, b), c) == nim_mul(a, nim_mul(b, c))
        assert nim_mul(a, b ^ c) == nim_mul(a, b) ^ nim_mul(a, c)
    census = json.load(open(os.path.join(OUT, "c07_census.json")))
    groups = census["associative_groups"]
    canon = ["empty", "L", "R", "D[x]", "D[y]", "D[z]", "L+R", "D[x^y^z]", "L+R+D[z]", "D[x]+D[y]", "D[x]+D[y]+D[z]"]
    name2idx = {name(i): i for i in range(512)}
    specs = [s for g in groups for s in g]
    n = 128
    path = os.path.join(OUT, "mex128_assoc44.bin")
    run_mextab(["rect", n, n, path] + [name2idx[s] for s in specs])
    T = load_tables(path, n, n)
    res = {"window": n, "groups": {}}
    k = 0
    for g in groups:
        c = [s for s in g if s in canon]
        assert len(c) == 1, g
        F = np.array([[formula(c[0], a, b) for b in range(n)] for a in range(n)])
        bad = []
        for s in g:
            if not np.array_equal(T[k], F):
                bad.append(s)
            k += 1
        res["groups"][c[0]] = {"specs": g, "specs_differing_from_formula_on_128": bad}
    res["all_44_equal_formula_on_128"] = all(not v["specs_differing_from_formula_on_128"] for v in res["groups"].values())
    # associativity of the 11 formulas on a larger random sample (exact integers)
    for c in canon:
        for _ in range(2000):
            a, b, cc = (int(v) for v in rng.integers(0, 300, 3))
            assert formula(c, formula(c, a, b), cc) == formula(c, a, formula(c, b, cc)), c
    res["formulas_associative_random_2000_each"] = True
    return res


def jacobsthal(k):
    return (2 ** k - (-1) ** k) // 3


def formula_g(b):
    if b == 0:
        return 0
    k = 1
    while not (jacobsthal(k + 1) <= b < jacobsthal(k + 2)):
        k += 1
    return b + jacobsthal(k) if b < 2 ** k else b - jacobsthal(k)


def part_jacobsthal(NB=1 << 18):
    path = os.path.join(OUT, "jac_row2.bin")
    t0 = time.time()
    run_mextab(["jac", NB, path])
    g = np.fromfile(path, dtype=np.int32).astype(np.int64)
    secs = round(time.time() - t0, 1)
    F = np.array([formula_g(b) for b in range(NB)])
    mism = np.nonzero(g != F)[0]
    inv = bool(np.array_equal(g[g[g < NB]], np.arange(NB)[g < NB]))
    # compare the beginning with the 64x64 C table (row 2 of D[x^y])
    C = load_tables(os.path.join(OUT, "mex64_all.bin"), 64, 64)
    row2_64 = C[idx_of(0, 0, [3]), 2, :]
    h = np.abs(g - np.arange(NB))
    return {"NB": NB, "seconds": secs, "formula_mismatches": int(mism.size),
            "first_mismatch": int(mism[0]) if mism.size else None, "involution_on_range": inv,
            "agrees_with_64x64_table": bool(np.array_equal(row2_64, g[:64])),
            "first_terms": g[:24].tolist(), "max_abs_g_minus_b": int(h.max()),
            "values_of_abs_dev": sorted(set(int(v) for v in h))[:20]}


def part_bitfacts():
    res = {}
    # (J1), (J2)
    res["J1_all_k_le_60"] = all(jacobsthal(k + 1) + jacobsthal(k) == 2 ** k for k in range(0, 61))
    res["J2a_fails_at"] = [k for k in range(1, 61) if not jacobsthal(k) < 2 ** (k - 1)]
    res["J2b_fails_at"] = [k for k in range(2, 61) if not jacobsthal(k + 1) > 2 ** (k - 1)]
    res["recurrence"] = all(jacobsthal(k + 1) == jacobsthal(k) + 2 * jacobsthal(k - 1) for k in range(1, 60))
    # (X): 0 <= x < c  =>  x ^ (x + c) > x, exhaustive for c <= 2^11
    badX = [(x, c) for c in range(1, 2049) for x in range(c) if not (x ^ (x + c)) > x]
    res["X_violations_c_le_2048"] = len(badX)
    # Case analysis of the proof, checked literally for k = 3..20 on every t:
    case_fail = []
    for k in range(3, 21):
        Jk, Jk1, Jk2 = jacobsthal(k), jacobsthal(k + 1), jacobsthal(k + 2)
        M = 2 ** k - 1
        for t in range(Jk):
            b = Jk1 + t
            # (i) first block: complement trick v ^ b = (M - v) ^ (M - b), both < J_k < 2^(k-1)
            if not (M - b < Jk and Jk <= 2 ** (k - 1) and 2 ** (k - 1) < Jk1):
                case_fail.append(("first-i-bounds", k, t))
            v = 2 ** k + t
            if not ((v ^ b) > 2 ** k + t):
                case_fail.append(("first-ii", k, t))
            b2 = 2 ** k + t
            v2 = Jk1 + t
            if not (v2 < 2 ** k and (v2 ^ b2) >= Jk2):
                case_fail.append(("second-ii", k, t))
        # (i) exhaustive in v for small k
        if k <= 12:
            for t in range(Jk):
                b = Jk1 + t
                for vv in range(Jk1, 2 ** k):
                    if not (vv ^ b) < Jk1:
                        case_fail.append(("first-i-exh", k, t, vv))
    res["proof_case_failures_k_3_20"] = case_fail[:10]
    res["n_proof_case_failures"] = len(case_fail)
    return res


def additive_period(r, pmax, min_tail=200):
    n = len(r)
    for p in range(1, pmax + 1):
        d = r[p:] - r[:-p]
        s = d[-1]
        bad = np.nonzero(d != s)[0]
        b0 = int(bad[-1]) + 1 if bad.size else 0
        if n - p - b0 >= max(min_tail, 3 * p):
            return (p, int(s), b0)
    return None


def part_periodic():
    NR, NC = 6, 1500
    path = os.path.join(OUT, "mex6x1500_all.bin")
    if not os.path.exists(path):
        run_mextab(["rect", NR, NC, path])
    R6 = load_tables(path, NR, NC)
    C = load_tables(os.path.join(OUT, "mex64_all.bin"), 64, 64)
    groups = {}
    for idx in lab_order():
        groups.setdefault(C[idx].tobytes(), []).append(idx)
    reps = [g[0] for g in groups.values()]
    per = {idx: [additive_period(R6[idx][a], NC // 4) for a in range(1, 6)] for idx in reps}
    n_rows = 5 * len(reps)
    n_per = sum(1 for idx in reps for v in per[idx] if v)
    full = [name(i) for i in reps if all(per[i])]
    none_ = [name(i) for i in reps if not any(per[i])]
    # do specs in the same 64x64 group have the same 6 x 1500 rectangle?
    split = []
    for g in groups.values():
        rects = {R6[i].tobytes() for i in g}
        if len(rects) > 1:
            split.append([name(i) for i in g])
    # any representative-dependence of the periodicity census?
    dep = []
    for g in groups.values():
        pats = {tuple(bool(v) for v in [additive_period(R6[i][a], NC // 4) for a in range(1, 6)]) for i in g}
        if len(pats) > 1:
            dep.append([name(i) for i in g])
    # D[x^y] row 2 is in the census: is it flagged non-periodic?
    lab = json.load(open(os.path.join(ROOT, "results", "EXP-C07-03.json")))["results"]
    lab_map = {r["spec"]: [bool(v) for _, v in sorted(r["periods"].items())] for r in lab["rows"]}
    mine_map = {name(i): [bool(v) for v in per[i]] for i in reps}
    diff = [k for k in mine_map if lab_map.get(k) != mine_map[k]]
    return {"operations": len(reps), "rows": n_rows, "rows_periodic": n_per, "all_five_periodic": len(full),
            "no_row_periodic": len(none_), "groups_whose_6x1500_rectangles_differ": split,
            "groups_with_representative_dependent_periodicity": dep,
            "differences_from_lab_per_operation": diff,
            "D[x^y]_rows_periodic": mine_map.get("D[x^y]")}


def part_diagonals():
    C = load_tables(os.path.join(OUT, "mex64_all.bin"), 64, 64)
    out = {}
    for nm, masks, L, R in [("L+R+D[x^y^z]", [7], 1, 1), ("D[z]+D[x^y^z]", [4, 7], 0, 0)]:
        T = C[idx_of(L, R, masks)]
        out[nm] = {"diag": [int(T[i, i]) for i in range(24)], "commutative": bool(np.array_equal(T, T.T))}
    return out


if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = globals()["part_" + part]()
    res["_seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, f"c07_{part}.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str)[:6000])
