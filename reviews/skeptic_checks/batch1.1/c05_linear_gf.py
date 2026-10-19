"""Skeptic batch 1.1 -- CLM-C05-10 / EXP-C05-07: linear models x*y = a x + b y over GF(q), q <= 128.

Independent of systems/, lab/ and experiments/ (the lab's result files are read only for comparison).
* GF(p^k) is built as GF(p)[t]/(f) with f the LAST monic irreducible of degree k in lexicographic order
  (the lab uses the first one), by my own polynomial arithmetic; every non-zero element is checked to have
  an inverse.
* For every law, every q and every (a, b) in GF(q)^2 the law is checked TWO ways:
    (A) coefficient method: t evaluates to alpha x + beta y; the law holds iff alpha = 1 and beta = 0;
    (B) brute force: the full q x q table a x + b y is evaluated on all q^2 pairs (x, y).
  The two solution sets must coincide.
usage: python c05_linear_gf.py [QMAX]
"""
import itertools
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# the 15 open laws of EXP-C05-03 (ETP numbering), x = t
LAWS = {467: "y(x(x(yy)))", 501: "y(y(x(xy)))", 670: "y(x((xy)y))", 677: "y(x((yx)y))", 704: "y(y((xx)y))",
        883: "y((xy)(yy))", 907: "y((yx)(xy))", 1076: "y((x(xy))y)", 1083: "y((x(yx))y)", 1110: "y((y(xx))y)",
        1279: "y(((xx)y)y)", 1286: "y(((xy)x)y)", 1313: "y(((yx)x)y)", 1516: "(yy)(x(xy))", 1719: "(yy)((xx)y)"}


def parse(s):
    """Juxtaposition = product; products associate to the left; parentheses group."""
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
        assert c in "xy"
        pos += 1
        return c

    def expr():
        nonlocal pos
        e = atom()
        while pos < len(s) and s[pos] != ")":
            e = (e, atom())
        return e

    t = expr()
    assert pos == len(s)
    return t


def show(t):
    return t if isinstance(t, str) else "(" + show(t[0]) + "*" + show(t[1]) + ")"


def factor_prime_power(q):
    for p in range(2, q + 1):
        if q % p == 0:
            k = 0
            while q % p == 0:
                q //= p
                k += 1
            return (p, k) if q == 1 else None


def pmod(a, f, p):
    """Remainder of polynomial a modulo monic f over GF(p); lists low -> high."""
    a = list(a)
    d = len(f) - 1
    for i in range(len(a) - 1, d - 1, -1):
        c = a[i] % p
        if c:
            for j in range(d + 1):
                a[i - d + j] = (a[i - d + j] - c * f[j]) % p
    a = [c % p for c in a[:d]]
    return a + [0] * (d - len(a))


def irreducible_last(p, k):
    best = None
    for coeffs in itertools.product(range(p), repeat=k):   # lexicographic in (c0, ..., c_{k-1})
        f = list(coeffs) + [1]
        if f[0] == 0:
            continue
        ok = True
        for d in range(1, k // 2 + 1):
            for g in itertools.product(range(p), repeat=d):
                if not any(pmod(f, list(g) + [1], p)):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            best = f
    return best


def field(q):
    p, k = factor_prime_power(q)
    if k == 1:
        r = np.arange(q)
        return (r[:, None] + r[None, :]) % q, (r[:, None] * r[None, :]) % q, None
    f = irreducible_last(p, k)
    dig = [[(x // p ** i) % p for i in range(k)] for x in range(q)]
    num = lambda v: sum(c * p ** i for i, c in enumerate(v))
    add = np.array([[num([(u + v) % p for u, v in zip(dig[x], dig[y])]) for y in range(q)] for x in range(q)])
    mul = np.zeros((q, q), dtype=np.int64)
    for x in range(q):
        for y in range(q):
            prod = [0] * (2 * k - 1)
            for i, u in enumerate(dig[x]):
                for j, v in enumerate(dig[y]):
                    prod[i + j] += u * v
            mul[x, y] = num(pmod(prod, f, p))
    # sanity: GF(q) is a field (every non-zero element invertible), 1 is the unit, mul is commutative
    assert all(1 in mul[x, 1:] or q == 2 for x in range(1, q)) and all((mul[1] == np.arange(q)))
    assert (mul == mul.T).all()
    return add, mul, f


def coeff(t, add, mul, A, B):
    if t == "x":
        return np.ones_like(A), np.zeros_like(A)
    if t == "y":
        return np.zeros_like(A), np.ones_like(A)
    a1, b1 = coeff(t[0], add, mul, A, B)
    a2, b2 = coeff(t[1], add, mul, A, B)
    return add[mul[A, a1], mul[B, a2]], add[mul[A, b1], mul[B, b2]]


def evaluate(t, T, X, Y):
    if t == "x":
        return X
    if t == "y":
        return Y
    return T[evaluate(t[0], T, X, Y), evaluate(t[1], T, X, Y)]


def main():
    qmax = int(sys.argv[1]) if len(sys.argv) > 1 else 128
    qs = [q for q in range(2, qmax + 1) if factor_prime_power(q)]
    t0 = time.time()
    fields = {q: field(q) for q in qs}
    terms = {num: parse(s) for num, s in LAWS.items()}
    out = {"q": qs, "moduli": {q: fields[q][2] for q in qs}, "laws": {}, "method_disagreements": []}
    for num, t in terms.items():
        orders, counts = [], {}
        for q in qs:
            add, mul, _ = fields[q]
            A, B = (z.ravel() for z in np.meshgrid(np.arange(q), np.arange(q), indexing="ij"))
            al, be = coeff(t, add, mul, A, B)
            solA = set(zip(A[(al == 1) & (be == 0)].tolist(), B[(al == 1) & (be == 0)].tolist()))
            X, Y = np.meshgrid(np.arange(q), np.arange(q), indexing="ij")
            solB = set()
            for a in range(q):
                for b in range(q):
                    T = add[mul[a][:, None], mul[b][None, :]]
                    if np.array_equal(evaluate(t, T, X, Y), X):
                        solB.add((a, b))
            if solA != solB:
                out["method_disagreements"].append((num, q))
            if solB:
                orders.append(q)
                counts[q] = len(solB)
        out["laws"][num] = {"law": "x = " + LAWS[num], "term": show(t), "orders": orders, "solution_counts": counts}
        print(num, orders, flush=True)
    # comparison with the lab's EXP-C05-07 (read only)
    try:
        lab = json.load(open(os.path.join(ROOT, "results", "EXP-C05-07.json")))["results"]
        cmp = {}
        for row in lab["rows"]:
            num = row["etp_number"]
            mine = [q for q in out["laws"][num]["orders"]]
            theirs = [q for q in row["linear_model_orders"] if q <= qmax]
            cmp[num] = {"agree": mine == theirs, "only_mine": sorted(set(mine) - set(theirs)),
                        "only_lab": sorted(set(theirs) - set(mine)),
                        "count_disagreements": [q for q, e in row["examples"].items()
                                                if int(q) <= qmax and e["models"] != out["laws"][num]["solution_counts"].get(int(q))]}
        out["comparison_with_EXP-C05-07"] = cmp
        e03 = {r["etp_number"]: r for r in json.load(open(os.path.join(ROOT, "results", "EXP-C05-03.json")))["results"]["rows"]}
        gaps = {501: [6, 7], 677: [6], 883: [6], 1076: [8], 1083: [5, 6]}          # CLM-C05-08
        notes_out = {670: [6, 7], 704: [9], 907: [2, 4, 5, 6], 1076: [6, 7], 1279: [9]}  # ETP notes (E03 data)
        conflicts = []
        for num, d in out["laws"].items():
            for q in d["orders"]:
                if q <= 10 and e03[num]["status_n_2_10"].get(str(q)) == "UNSAT":
                    conflicts.append((num, q, "EXP-C05-03 UNSAT"))
                if q in gaps.get(num, []):
                    conflicts.append((num, q, "certified gap"))
                if q in notes_out.get(num, []):
                    conflicts.append((num, q, "notes: not in spectrum"))
        out["conflicts_with_unsat_or_gaps"] = conflicts
    except FileNotFoundError as e:
        out["comparison_with_EXP-C05-07"] = str(e)
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(HERE, "c05_linear_gf.json"), "w"), indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("method_disagreements", "comparison_with_EXP-C05-07",
                                          "conflicts_with_unsat_or_gaps", "seconds") if k in out}, indent=1,
                     default=str))


if __name__ == "__main__":
    main()
