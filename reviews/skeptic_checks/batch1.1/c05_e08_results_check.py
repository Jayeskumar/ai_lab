"""Skeptic batch 1.1 -- check results/EXP-C05-08.json against the case lists (read-only).

* for each (law, n) the recorded instances are exactly the cases of Lemma 8, each once
  (idempotent: partitions of n with a part 1, ell = 1; non-idempotent: every distinct part ell >= 2);
* every SAT model satisfies the law (my own evaluator) and the constraints of its case
  (row 0 = pi(lam, ell) in the lab's convention, idempotency / conditional fixed-point bounds, Latin rows,
  Latin columns for 1313);
* every UNSAT instance has drat_trim == VERIFIED; verdicts follow from the instance list.
"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        return [[]]
    out = []
    for p in range(1, min(n, maxpart) + 1):
        for rest in partitions(n - p, p):
            out.append([p] + rest)
    return out


def lemma8_cases(n):
    cs = set()
    for lam in partitions(n):
        lam = tuple(sorted(lam, reverse=True))
        if 1 in lam:
            cs.add(("idempotent", lam, 1))
        for ell in set(lam):
            if ell >= 2:
                cs.add(("non-idempotent", lam, ell))
    return cs


def holds(T, law):
    n = len(T)
    for x in range(n):
        for y in range(n):
            t = T[y][T[x][T[T[y][x]][y]]] if law == 677 else T[y][T[T[T[y][x]][x]][y]]
            if t != x:
                return False
    return True


def lab_perm(lam, ell):
    parts = list(lam)
    parts.remove(ell)
    perm, start = {}, 0
    for p in [ell] + parts:
        cyc = list(range(start, start + p))
        for i, a in enumerate(cyc):
            perm[a] = cyc[(i + 1) % p]
        start += p
    return [perm[b] for b in range(len(perm))]


def main():
    d = json.load(open(os.path.join(ROOT, "results", "EXP-C05-08.json")))["results"]
    inst = d["instances"]
    rep = {"case_list_mismatch": [], "duplicates": [], "sat_problems": [], "unverified_unsat": [], "verdicts": {}}
    by = collections.defaultdict(list)
    for r in inst:
        by[(r["law"], r["n"])].append(r)
    for (law, n), rs in sorted(by.items()):
        recorded = [(r["case"], tuple(r["lam"]), r["ell"]) for r in rs]
        if len(set(recorded)) != len(recorded):
            rep["duplicates"].append((law, n))
        if set(recorded) != lemma8_cases(n):
            rep["case_list_mismatch"].append((law, n, len(recorded), len(lemma8_cases(n))))
        for r in rs:
            if r["status"] == "SAT":
                T = r["model"]
                k = list(r["lam"]).count(1)
                ok = holds(T, law)
                ok &= T[0] == lab_perm(r["lam"], r["ell"])
                ok &= all(sorted(row) == list(range(n)) for row in T)
                if law == 1313:
                    ok &= all(sorted(T[a][b] for a in range(n)) == list(range(n)) for b in range(n))
                fix = [sum(T[a][b] == b for b in range(n)) for a in range(n)]
                if r["case"] == "idempotent":
                    ok &= all(T[a][a] == a for a in range(n)) and all(f >= k for f in fix)
                else:
                    ok &= all(T[a][a] == a or fix[a] >= k for a in range(1, n))
                if not ok:
                    rep["sat_problems"].append((law, n, r["case"], r["lam"], r["ell"]))
            elif r["status"] == "UNSAT" and r.get("drat_trim") != "VERIFIED":
                rep["unverified_unsat"].append((law, n, r["lam"], r["ell"]))
        sat = any(r["status"] == "SAT" for r in rs)
        rep["verdicts"][f"{law}/{n}"] = {"cases": len(rs), "expected_cases": len(lemma8_cases(n)),
                                         "SAT": sum(r["status"] == "SAT" for r in rs),
                                         "UNSAT_verified": sum(r.get("drat_trim") == "VERIFIED" for r in rs),
                                         "lab_verdict": d["verdict"][f"{law}/{n}"],
                                         "my_verdict": "model found" if sat else (
                                             "no model (every case certified)" if all(
                                                 r.get("drat_trim") == "VERIFIED" for r in rs) else "?")}
    rep["proof_lines_total"] = sum(r.get("proof_lines", 0) for r in inst)
    rep["proof_lines_by"] = {f"{k[0]}/{k[1]}": sum(r.get("proof_lines", 0) for r in v) for k, v in sorted(by.items())}
    rep["max_conflicts_by"] = {f"{k[0]}/{k[1]}": max(r["conflicts"] for r in v) for k, v in sorted(by.items())}
    print(json.dumps(rep, indent=1))
    json.dump(rep, open(os.path.join(HERE, "c05_e08_results_check.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
