"""Skeptic batch 1.1 -- EXP-C05-08: an independent decision of laws 677 and 1313 at small orders.

Written from scratch: no import from systems/, lab/ or experiments/.  pysat is used only as a SAT solver.

Laws (ETP numbering, as in the Lean file C05_Law1313.lean):
  677 : x = y*(x*((y*x)*y))          1313 : x = y*(((y*x)*x)*y)

Encoding (my own; aux-free except for nothing at all):
  m(a,b,c) <=> a*b = c.
  cells    : every cell has exactly one value (one at-least-one clause + pairwise at-most-one);
  rows     : every row is a permutation (sound for both laws: Lean law677_left_bijective /
             law1313_left_bijective -- a left translation is onto by the law, so bijective on a finite set);
  columns  : (1313 only) every column is a permutation (sound: Lean law1313_right_bijective);
  law      : n^5 clauses  -m(y,x,c) | -m(c,y,d) | -m(x,d,e) | m(y,e,x)          (677)
                          -m(y,x,c) | -m(c,x,d) | -m(d,y,e) | m(y,e,x)          (1313)
             (in a functional table the premise holds exactly for the true c, d, e, so the clauses say
             y*e = x for the true value e of the inner term: exactly the law);
  symmetry : MY case split "SB-min" (not the lab's Lemma 8): pick a with fix(L_a) minimal over ALL elements,
             relabel so that a -> 0 and L_0 = pi(lam, ell) (cycle type lam, 0 in a cycle of length ell);
             then every row has >= k = lam.count(1) fixed points.  Cases: every partition lam of n and every
             distinct part ell of lam.  The at-least-k constraint is encoded without auxiliary variables:
             every (n-k+1)-subset U of columns contains some b with a*b = b.
             Proof of completeness in reviews/skeptic_batch1.1.md (section 2).

usage: python c05_independent.py <law> <n> [solver] [budget] [first_case] [last_case]
       python c05_independent.py validate
"""
import itertools
import json
import os
import sys
import time

from pysat.solvers import Solver

HERE = os.path.dirname(os.path.abspath(__file__))


def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        return [[]]
    out = []
    for p in range(1, min(n, maxpart) + 1):          # increasing first part, different order from the lab
        for rest in partitions(n - p, p):
            out.append([p] + rest)
    return out


def my_cases(n):
    cs = []
    for lam in partitions(n):
        for ell in sorted(set(lam)):
            cs.append((tuple(sorted(lam)), ell))
    return cs


def perm_of(lam, ell, n):
    """A permutation of 0..n-1 of cycle type lam with 0 in a cycle of length ell.
    Cycle of 0 first: (0 1 ... ell-1); then the other cycles in increasing length, written consecutively."""
    rest = list(lam)
    rest.remove(ell)
    rest.sort()
    p = [None] * n
    start = 0
    for L in [ell] + rest:
        for i in range(L):
            p[start + i] = start + (i + 1) % L
        start += L
    assert start == n and sorted(p) == list(range(n))
    # self-check: cycle type and the length of the cycle of 0
    seen, ct = set(), []
    for s0 in range(n):
        if s0 in seen:
            continue
        L, z = 0, s0
        while z not in seen:
            seen.add(z)
            z = p[z]
            L += 1
        ct.append(L)
    L0, z = 1, p[0]
    while z != 0:
        z = p[z]
        L0 += 1
    assert sorted(ct) == sorted(lam) and L0 == ell, (lam, ell, p)
    return p


class CNF:
    def __init__(self, n):
        self.n = n
        self.cl = []

    def m(self, a, b, c):
        n = self.n
        return 1 + (a * n + b) * n + c

    def exactly_one(self, lits):
        self.cl.append(list(lits))
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                self.cl.append([-lits[i], -lits[j]])


DIVISION = os.environ.get("SKEPTIC_DIV") == "1"


def build(law, n, case=None, columns=None, division=None):
    """division: add MY aux-free implied 'division' clauses (sound by row injectivity; see the report):
      677 : y*a = x, y*x = c, c*y = d  ->  x*d = a          and   y*b = x, x*a = b, y*x = c  ->  c*y = a
      1313: y*a = x, y*x = c, c*x = d  ->  d*y = a          and   y*b = x, a*y = b, y*x = c  ->  c*x = a
    (the second 1313 family uses injectivity of right translations, Lean law1313_right_bijective)."""
    if division is None:
        division = DIVISION
    F = CNF(n)
    R = range(n)
    m = F.m
    for a in R:
        for b in R:
            F.exactly_one([m(a, b, c) for c in R])
    for a in R:
        for c in R:
            F.exactly_one([m(a, b, c) for b in R])
    if columns is None:
        columns = (law == 1313)
    if columns:
        for b in R:
            for c in R:
                F.exactly_one([m(a, b, c) for a in R])
    for x in R:
        for y in R:
            for c in R:
                for d in R:
                    for e in R:
                        if law == 677:
                            F.cl.append([-m(y, x, c), -m(c, y, d), -m(x, d, e), m(y, e, x)])
                        elif law == 1313:
                            F.cl.append([-m(y, x, c), -m(c, x, d), -m(d, y, e), m(y, e, x)])
                        else:
                            raise ValueError(law)
    if division:
        for x in R:
            for y in R:
                for c in R:
                    for d in R:
                        for a in R:
                            if law == 677:
                                F.cl.append([-m(y, a, x), -m(y, x, c), -m(c, y, d), m(x, d, a)])
                                # here d plays the role of b: y*d = x, x*a = d, y*x = c -> c*y = a
                                F.cl.append([-m(y, d, x), -m(x, a, d), -m(y, x, c), m(c, y, a)])
                            else:
                                F.cl.append([-m(y, a, x), -m(y, x, c), -m(c, x, d), m(d, y, a)])
                                F.cl.append([-m(y, d, x), -m(a, y, d), -m(y, x, c), m(c, x, a)])
    if case is not None:
        lam, ell = case
        p = perm_of(lam, ell, n)
        for b in R:
            F.cl.append([m(0, b, p[b])])
        k = list(lam).count(1)
        if k:
            for a in range(1, n):
                for U in itertools.combinations(R, n - k + 1):
                    F.cl.append([m(a, b, b) for b in U])
    return F


def table_from_model(model, n):
    pos = set(l for l in model if l > 0)
    T = [[None] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            vals = [c for c in range(n) if 1 + (a * n + b) * n + c in pos]
            assert len(vals) == 1
            T[a][b] = vals[0]
    return T


def holds(T, law):
    n = len(T)
    for x in range(n):
        for y in range(n):
            if law == 677:
                t = T[y][T[x][T[T[y][x]][y]]]
            else:
                t = T[y][T[T[T[y][x]][x]][y]]
            if t != x:
                return False
    return True


def solve(F, solver="cadical195", budget=None):
    with Solver(name=solver, bootstrap_with=F.cl) as s:
        if budget:
            s.conf_budget(budget)
            ok = s.solve_limited()
        else:
            ok = s.solve()
        st = s.accum_stats()
        model = s.get_model() if ok else None
    return ok, st.get("conflicts"), model


DRAT = "/tmp/claude-0/-home-user-ai-lab/5e93bf16-791a-5608-a61f-d865140bf384/scratchpad/drat/drat-trim"
SCRATCH = "/tmp/claude-0/-home-user-ai-lab/5e93bf16-791a-5608-a61f-d865140bf384/scratchpad/c05cert"


def certify_case(law, n, case, i, solver="cadical195"):
    """Solve with DRAT proof logging and check the proof with drat-trim (files kept in the scratchpad)."""
    import hashlib
    import subprocess
    os.makedirs(SCRATCH, exist_ok=True)
    F = build(law, n, case)
    t0 = time.time()
    with Solver(name=solver, bootstrap_with=F.cl, with_proof=True) as s:
        ok = s.solve()
        conf = s.accum_stats().get("conflicts")
        proof = s.get_proof() if ok is False else None
        model = s.get_model() if ok else None
    r = {"i": i, "lam": list(case[0]), "ell": case[1], "status": "SAT" if ok else "UNSAT", "conflicts": conf,
         "solve_s": round(time.time() - t0, 1)}
    if ok:
        T = table_from_model(model, n)
        r["model_ok"] = holds(T, law)
        r["model"] = T
        return r
    base = os.path.join(SCRATCH, f"{law}_n{n}_case{i}")
    nv = n ** 3
    with open(base + ".cnf", "w") as fh:
        fh.write(f"p cnf {nv} {len(F.cl)}\n")
        for c in F.cl:
            fh.write(" ".join(map(str, c)) + " 0\n")
    with open(base + ".drat", "w") as fh:
        fh.write("\n".join(proof) + "\n")
    r["cnf_sha256"] = hashlib.sha256(open(base + ".cnf", "rb").read()).hexdigest()
    r["proof_lines"] = len(proof)
    t1 = time.time()
    res = subprocess.run([DRAT, base + ".cnf", base + ".drat"], capture_output=True, text=True, timeout=3600)
    lines = [l for l in res.stdout.splitlines() if l.startswith("s ")]
    r["drat_trim"] = lines
    r["verified"] = lines == ["s VERIFIED"]
    r["check_s"] = round(time.time() - t1, 1)
    os.remove(base + ".drat")
    return r


def run_law(law, n, solver="cadical195", budget=None, lo=0, hi=None):
    cs = my_cases(n)
    hi = len(cs) if hi is None else hi
    res = []
    for i, case in enumerate(cs[lo:hi], start=lo):
        t0 = time.time()
        F = build(law, n, case)
        ok, conf, model = solve(F, solver, budget)
        r = {"i": i, "lam": list(case[0]), "ell": case[1], "status": {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[ok],
             "conflicts": conf, "seconds": round(time.time() - t0, 1)}
        if ok:
            T = table_from_model(model, n)
            r["model_ok"] = holds(T, law)
            r["model"] = T
        res.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != "model"}), flush=True)
        if ok:
            break      # one model decides the order
    return {"law": law, "n": n, "solver": solver, "cases_total": len(cs), "cases_run": [lo, hi], "results": res}


# ------------------------------------------------------------------ validation of the encoding
def gf_tables(p, k, f):
    """GF(p^k) = GF(p)[t]/(f), f monic of degree k given low->high; elements as base-p digit integers."""
    q = p ** k
    def to_d(x):
        return [(x // p ** i) % p for i in range(k)]
    def to_i(d):
        return sum(c * p ** i for i, c in enumerate(d))
    add = [[to_i([(u + v) % p for u, v in zip(to_d(x), to_d(y))]) for y in range(q)] for x in range(q)]
    mul = [[0] * q for _ in range(q)]
    for x in range(q):
        for y in range(q):
            prod = [0] * (2 * k)
            for i, u in enumerate(to_d(x)):
                for j, v in enumerate(to_d(y)):
                    prod[i + j] = (prod[i + j] + u * v) % p
            for i in range(2 * k - 1, k - 1, -1):     # reduce by f
                c = prod[i]
                if c:
                    for j in range(k + 1):
                        prod[i - k + j] = (prod[i - k + j] - c * f[j]) % p
            mul[x][y] = to_i(prod[:k])
    return add, mul


def linear_models(law, p, k, f):
    add, mul = gf_tables(p, k, f)
    q = p ** k
    out = []
    for A in range(q):
        for B in range(q):
            T = [[add[mul[A][x]][mul[B][y]] for y in range(q)] for x in range(q)]
            if holds(T, law):
                out.append((A, B, T))
    return out


def fixes(T, a):
    return sum(T[a][b] == b for b in range(len(T)))


def cycle_type_and_ell(row, a):
    n = len(row)
    seen, lam = set(), []
    ell = None
    for s in range(n):
        if s in seen:
            continue
        L, x = 0, s
        while x not in seen:
            seen.add(x)
            x = row[x]
            L += 1
        lam.append(L)
        # length of the cycle containing a
    x, L = row[a], 1
    while x != a:
        x = row[x]
        L += 1
    return tuple(sorted(lam)), L


def relabel_to_case(T):
    """Apply SB-min to the model T: returns (case, relabelled table)."""
    n = len(T)
    a = min(range(n), key=lambda z: fixes(T, z))
    lam, ell = cycle_type_and_ell(T[a], a)
    target = perm_of(lam, ell, n)
    # bijection sigma: cycle of a -> cycle of 0 in target (a -> 0), other cycles -> cycles of equal length
    def cycles(perm, first):
        seen, out = set(), []
        order = [first] + [z for z in range(len(perm)) if z != first]
        for s in order:
            if s in seen:
                continue
            c, x = [], s
            while x not in seen:
                seen.add(x)
                c.append(x)
                x = perm[x]
            out.append(c)
        return out
    src = cycles(T[a], a)
    dst = cycles(target, 0)
    sigma = {}
    used = [False] * len(dst)
    for c in src:
        for j, d in enumerate(dst):
            if not used[j] and len(d) == len(c) and (c[0] != a or d[0] == 0) and (c[0] == a or d[0] != 0):
                used[j] = True
                for u, v in zip(c, d):
                    sigma[u] = v
                break
    assert len(sigma) == n
    inv = {v: u for u, v in sigma.items()}
    U = [[sigma[T[inv[i]][inv[j]]] for j in range(n)] for i in range(n)]
    assert U[0] == target
    return (lam, ell), U


def assign_units(F, T):
    n = F.n
    return [F.m(a, b, T[a][b]) for a in range(n) for b in range(n)]


def validate():
    """(V1) linear models over GF(q) satisfy the plain CNF; (V2) after SB-min relabelling they satisfy the CNF of
    their case; (V3) 200 random tables with permutation rows: CNF verdict == direct evaluation."""
    import random
    rng = random.Random(1)
    report = []
    fields = [(5, 1, [0, 1]), (7, 1, [0, 1]), (3, 2, [2, 2, 1]), (2, 4, [1, 1, 0, 0, 1])]  # t^2+2t+2, t^4+t+1
    for law in (677, 1313):
        for (p, k, f) in fields:
            q = p ** k
            if q > 9 and law == 1313 and False:
                continue
            mods = linear_models(law, p, k, f)
            ok_plain = ok_case = 0
            for (A, B, T) in mods[:3]:
                F = build(law, q)
                with Solver(name="cadical195", bootstrap_with=F.cl) as s:
                    ok_plain += bool(s.solve(assumptions=assign_units(F, T)))
                case, U = relabel_to_case(T)
                assert holds(U, law)
                G = build(law, q, case)
                with Solver(name="cadical195", bootstrap_with=G.cl) as s:
                    ok_case += bool(s.solve(assumptions=assign_units(G, U)))
            report.append({"law": law, "q": q, "linear_models": len(mods), "tested": min(3, len(mods)),
                           "plain_cnf_accepts": ok_plain, "case_cnf_accepts": ok_case})
        # random tables with permutation rows (and columns for 1313 when possible)
        n = 5
        F = build(law, n, columns=False)
        agree = 0
        with Solver(name="cadical195", bootstrap_with=F.cl) as s:
            for _ in range(200):
                T = [rng.sample(range(n), n) for _ in range(n)]
                agree += (bool(s.solve(assumptions=assign_units(F, T))) == holds(T, law))
        report.append({"law": law, "random_row_permutation_tables_n5": 200, "cnf_agrees_with_evaluation": agree})
    return report


if __name__ == "__main__":
    if sys.argv[1] == "plain":
        # no case split: Latin rows (+ columns for 1313) and either no symmetry break ("none") or 0*0 in {0, 1} ("00")
        law, n, sb = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        budget = int(sys.argv[5]) if len(sys.argv) > 5 else None
        F = build(law, n)
        if sb == "00":
            F.cl.append([F.m(0, 0, 0), F.m(0, 0, 1)])
        t0 = time.time()
        ok, conf, model = solve(F, "cadical195", budget)
        r = {"law": law, "n": n, "sb": sb, "status": {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[ok],
             "conflicts": conf, "seconds": round(time.time() - t0, 1)}
        if ok:
            T = table_from_model(model, n)
            r["model_ok"] = holds(T, law)
            r["model"] = T
        print(json.dumps(r))
        json.dump(r, open(os.path.join(HERE, f"c05_plain_{law}_n{n}_{sb}.json"), "w"), indent=1)
        sys.exit()
    if sys.argv[1] == "certify":
        law, n = int(sys.argv[2]), int(sys.argv[3])
        out = {"law": law, "n": n, "results": []}
        t0 = time.time()
        for i, case in enumerate(my_cases(n)):
            r = certify_case(law, n, case, i)
            out["results"].append(r)
            print(json.dumps({k: v for k, v in r.items() if k != "model"}), flush=True)
            if r["status"] == "SAT":
                break
        out["seconds"] = round(time.time() - t0, 1)
        out["all_unsat_verified"] = all(r.get("verified") for r in out["results"]) and len(out["results"]) == len(my_cases(n))
        json.dump(out, open(os.path.join(HERE, f"c05_certify_{law}_n{n}.json"), "w"), indent=1)
        print(json.dumps({"law": law, "n": n, "cases": len(out["results"]), "all_unsat_verified": out["all_unsat_verified"],
                          "seconds": out["seconds"]}))
        sys.exit()
    if sys.argv[1] == "validate":
        r = validate()
        print(json.dumps(r, indent=1))
        json.dump(r, open(os.path.join(HERE, "c05_validate.json"), "w"), indent=1)
        sys.exit()
    if sys.argv[1] == "cases":
        # python c05_independent.py cases <law> <n> <i1,i2,...> [budget]   (no early stop)
        law, n = int(sys.argv[2]), int(sys.argv[3])
        idx = [int(z) for z in sys.argv[4].split(",")]
        budget = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "0" else None
        cs = my_cases(n)
        res = []
        for i in idx:
            t0 = time.time()
            ok, conf, model = solve(build(law, n, cs[i]), "cadical195", budget)
            r = {"i": i, "lam": list(cs[i][0]), "ell": cs[i][1], "division": DIVISION,
                 "status": {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[ok], "conflicts": conf,
                 "seconds": round(time.time() - t0, 1)}
            if ok:
                T = table_from_model(model, n)
                r["model_ok"] = holds(T, law)
                r["model"] = T
            res.append(r)
            print(json.dumps({k: v for k, v in r.items() if k != "model"}), flush=True)
        tag = f"c05_cases_{law}_n{n}_{'div' if DIVISION else 'plain'}_{idx[0]}-{idx[-1]}"
        json.dump(res, open(os.path.join(HERE, tag + ".json"), "w"), indent=1)
        sys.exit()
    law, n = int(sys.argv[1]), int(sys.argv[2])
    solver = sys.argv[3] if len(sys.argv) > 3 else "cadical195"
    budget = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != "0" else None
    lo = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    hi = int(sys.argv[6]) if len(sys.argv) > 6 else None
    t0 = time.time()
    out = run_law(law, n, solver, budget, lo, hi)
    out["seconds"] = round(time.time() - t0, 1)
    tag = f"c05_{law}_n{n}_{solver}_{lo}_{hi if hi is not None else 'end'}"
    json.dump(out, open(os.path.join(HERE, tag + ".json"), "w"), indent=1)
    st = [r["status"] for r in out["results"]]
    print(json.dumps({"law": law, "n": n, "cases_total": out["cases_total"], "run": len(st),
                      "SAT": st.count("SAT"), "UNSAT": st.count("UNSAT"), "UNKNOWN": st.count("UNKNOWN"),
                      "seconds": out["seconds"]}))
