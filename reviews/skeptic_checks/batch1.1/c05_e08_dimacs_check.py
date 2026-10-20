"""Skeptic batch 1.1 -- EXP-C05-08: does the experiment's builder produce the CNFs whose hashes are recorded, and
are the DIMACS files well formed?  Uses the lab's build() read-only (nothing is recorded); for the selected
cases it regenerates the CNF exactly as solve_case writes it, compares sha256 with results/EXP-C05-08.json,
and checks: max |literal| <= header variable count, no 0 literal inside a clause, no empty clause; and the
semantic check that the lab's CNF accepts my relabelled linear models (q = 5, 7, 9) in the case they fall into.
usage: python c05_e08_dimacs_check.py [n ...]
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from experiments.C05.E08_orders_8_10 import build, cases  # noqa: E402


def dimacs_bytes(sat):
    nv = sat.pool.top
    lines = [f"p cnf {nv} {len(sat.clauses)}\n"] + [" ".join(map(str, c)) + " 0\n" for c in sat.clauses]
    return "".join(lines).encode(), nv


def main():
    ns = [int(z) for z in sys.argv[1:]] or [5, 6, 7, 8]
    rec = json.load(open(os.path.join(ROOT, "results", "EXP-C05-08.json")))["results"]["instances"]
    by = {(r["law"], r["n"], r["case"], tuple(r["lam"]), r["ell"]): r for r in rec}
    out = {"checked": 0, "hash_match": 0, "hash_mismatch": [], "malformed": []}
    for law in (677, 1313):
        for n in ns:
            for case, lam, ell in cases(n):
                r = by[(law, n, case, tuple(lam), ell)]
                if r["status"] != "UNSAT":
                    continue
                sat, _ = build(law, n, case, lam, ell)
                data, nv = dimacs_bytes(sat)
                mx = max(abs(l) for c in sat.clauses for l in c)
                bad = mx > nv or any(0 in c for c in sat.clauses) or any(len(c) == 0 for c in sat.clauses)
                if bad:
                    out["malformed"].append((law, n, lam, ell, mx, nv))
                h = hashlib.sha256(data).hexdigest()
                out["checked"] += 1
                if h == r["cnf_sha256"]:
                    out["hash_match"] += 1
                else:
                    out["hash_mismatch"].append((law, n, case, lam, ell))
    out["semantic"] = semantic_check()
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, f"c05_e08_dimacs_check_{'_'.join(map(str, ns))}.json"), "w"), indent=1)


def semantic_check():
    """The lab's CNF of the Lemma-8 case of a genuine model must accept that (relabelled) model."""
    from pysat.solvers import Solver
    from experiments.C05.E08_orders_8_10 import canonical_permutation
    sys.path.insert(0, HERE)
    import c05_independent as C
    res = []
    fields = [(5, 1, [0, 1]), (7, 1, [0, 1]), (3, 2, [2, 2, 1])]
    for law in (677, 1313):
        for (p, k, f) in fields:
            for (A, Bc, T) in C.linear_models(law, p, k, f):
                n = len(T)
                fx = [C.fixes(T, a) for a in range(n)]
                idem = all(T[a][a] == a for a in range(n))
                if idem:
                    cand = [a for a in range(n) if fx[a] == min(fx)]
                    case = "idempotent"
                else:
                    ni = [a for a in range(n) if T[a][a] != a]
                    cand = [a for a in ni if fx[a] == min(fx[b] for b in ni)]
                    case = "non-idempotent"
                for a in cand:
                    lam, ell = C.cycle_type_and_ell(T[a], a)
                    lam = tuple(sorted(lam, reverse=True))
                    perm = canonical_permutation(lam, ell)
                    target = [perm[b] for b in range(n)]
                    # sigma: cycle of a -> cycle of 0 (a -> 0), other cycles -> canonical cycles of equal length
                    def cycles(pm, first):
                        seen, cs = set(), []
                        for s0 in [first] + [z for z in range(n) if z != first]:
                            if s0 in seen:
                                continue
                            c, z = [], s0
                            while z not in seen:
                                seen.add(z); c.append(z); z = pm[z]
                            cs.append(c)
                        return cs
                    src, dst = cycles(T[a], a), cycles(target, 0)
                    sigma, used = {}, [False] * len(dst)
                    for ci, c in enumerate(src):
                        for j, dd in enumerate(dst):
                            if not used[j] and len(dd) == len(c) and ((ci == 0) == (dd[0] == 0)):
                                used[j] = True
                                sigma.update(zip(c, dd))
                                break
                    inv = {v: u for u, v in sigma.items()}
                    U = [[sigma[T[inv[i]][inv[j]]] for j in range(n)] for i in range(n)]
                    assert U[0] == target and C.holds(U, law)
                    sat, _ = build(law, n, case, lam, ell)
                    with Solver(name="cadical195", bootstrap_with=sat.clauses) as s:
                        ok = s.solve(assumptions=[sat.v[i, j, U[i][j]] for i in range(n) for j in range(n)])
                    res.append({"law": law, "q": n, "a": A, "b": Bc, "elem": a, "case": case, "lam": lam,
                                "ell": ell, "accepted": bool(ok)})
    return {"tested": len(res), "accepted": sum(r["accepted"] for r in res),
            "rejected": [r for r in res if not r["accepted"]],
            "cases_seen": sorted({(r["law"], r["q"], r["case"], r["lam"], r["ell"]) for r in res})}


if __name__ == "__main__":
    main()
