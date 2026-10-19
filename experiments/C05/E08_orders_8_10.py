"""EXP-C05-08: laws 677 and 1313 at orders 8 and 10, by a complete case split on one row, every UNSAT case certified.

EXP-C05-03 left both laws UNKNOWN at n = 8 and 10. Both have the form x = y*T, so every row of a finite model is a
permutation (left_mul_bijective_of_law, C05_Magmas.lean); for 1313 every column is one too (Lemma 7 of
proofs/paper/C05.md). The case split (Lemma 8 there) picks the element relabelled 0:

* case "idempotent": every element satisfies x*x = x; then 0 is any element whose row has the fewest fixed points;
* case "non-idempotent": some x*x != x; then 0 is such an element whose row has the fewest fixed points among them.

After relabelling, row 0 is a fixed canonical permutation pi(lam, ell) with cycle type lam and 0 in a cycle of length
ell (ell = 1 exactly in the idempotent case), and the rows that compete with row 0 have at least lam.count(1) fixed
points. Each (case, lam, ell) is one CNF; the law has a model of order n iff one of them is satisfiable. Every CNF
also carries implied 'division' clauses that are sound because the translations are bijective (Lemma 7).
UNSAT answers come with a DRAT proof from CaDiCaL that drat-trim must verify; SAT answers are re-checked on the
table. An instance that exhausts its conflict budget is reported UNKNOWN and leaves its order undecided.
"""

import hashlib
import os
import subprocess
import sys
import tempfile
import time
from multiprocessing import get_context

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

from experiments.C05.E03_frontier_push import latin_rows
from experiments.C05.E06_certified_unsat import drat_path
from systems.magma import MagmaSAT, parse, satisfies

META = {
    "id": "EXP-C05-08",
    "cycle": "C05",
    "title": "Laws 677 and 1313 at orders 8 and 10: complete case split on the cycle type of one row, UNSAT cases "
             "certified by drat-trim",
    "agent": "Formal Verifier",
    "question": "Do x = y(x((yx)y)) (ETP 677) and x = y(((yx)x)y) (ETP 1313) have models of order 8 or 10, the two "
                "orders EXP-C05-03 left UNKNOWN?",
    "hypothesis": "H-C05-G: neither law has a model of order 8 or 10 (both have models of orders 5, 7, 9 and 16, none of "
                  "orders 2, 3, 4, 6).",
    "assumptions": ["rows are permutations for both laws (Lean: left_mul_bijective_of_law); columns are permutations "
                    "for 1313 (proofs/paper/C05.md, Lemma 7)",
                    "the case split of proofs/paper/C05.md, Lemma 8 (idempotent / non-idempotent, cycle type of the row "
                    "of an element with fewest fixed points) is complete",
                    "implied division clauses: for x = y*T, y*a = x forces T = a; for 677 (T = x*S) also x*a = T forces "
                    "S = a; for 1313 (T = S*y) also a*y = T forces S = a",
                    "CaDiCaL 1.5.3 (pysat) with proof logging; the conflict budget per instance is fixed, an exhausted "
                    "budget is reported UNKNOWN",
                    "drat-trim (github.com/marijnheule/drat-trim), found via DRAT_TRIM or the scratchpad build path",
                    "orders 5, 6, 7 are re-decided as a control (models known at 5 and 7, none at 6)"],
    "methodology": "For each law and n in (5, 6, 7, 8, 10), enumerate the cases (idempotent, lam, 1) for the partitions "
                   "lam of n with a part 1 and (non-idempotent, lam, ell) for every part ell >= 2 of every lam; build "
                   "the CNF (law, Latin rows, Latin columns for 1313, row 0 = pi(lam, ell), fixed-point bounds, "
                   "idempotency where applicable, division clauses); solve with CaDiCaL under a fixed conflict budget "
                   "(2 worker processes); verify every UNSAT proof with drat-trim and every SAT table with the law.",
    "falsification": "A verified model of order 8 or 10 refutes H-C05-G; a control order that disagrees with "
                     "EXP-C05-03 (SAT at 5, 7; UNSAT at 6) or a proof drat-trim rejects would expose an error.",
}

LAWS = {677: "y(x((yx)y))", 1313: "y(((yx)x)y)"}
ORDERS = (5, 6, 7, 8, 10)
BUDGET = {5: 200_000, 6: 200_000, 7: 200_000, 8: 2_000_000, 10: 4_000_000}
WORKERS = 2


def partitions(n, largest=None):
    largest = n if largest is None else largest
    if n == 0:
        yield ()
        return
    for p in range(min(n, largest), 0, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest


def cases(n):
    out = [("idempotent", lam, 1) for lam in partitions(n) if 1 in lam]
    out += [("non-idempotent", lam, ell) for lam in partitions(n) for ell in sorted(set(lam)) if ell >= 2]
    return out


def canonical_permutation(lam, ell):
    """Cycles of lengths lam on 0..n-1, written consecutively, the first one of length ell (it contains 0)."""
    parts = list(lam)
    parts.remove(ell)
    perm, start = {}, 0
    for p in [ell] + parts:
        cyc = list(range(start, start + p))
        for i, a in enumerate(cyc):
            perm[a] = cyc[(i + 1) % p]
        start += p
    return perm


def latin_columns(sat):
    n = sat.n
    cls = []
    for b in range(n):
        for c in range(n):
            cls += CardEnc.equals([sat.v[a, b, c] for a in range(n)], 1, vpool=sat.pool,
                                  encoding=EncType.pairwise).clauses
    return cls


def build(num, n, case, lam, ell):
    law = (parse(LAWS[num]), "x")
    sat = MagmaSAT(n, [law])
    v = sat.v
    sat.clauses += latin_rows(sat)
    if num == 1313:
        sat.clauses += latin_columns(sat)
    perm = canonical_permutation(lam, ell)
    sat.clauses += [[v[0, b, perm[b]]] for b in range(n)]
    k = lam.count(1)
    if case == "idempotent":
        sat.clauses += [[v[a, a, a]] for a in range(n)]
    if k:
        for a in range(1, n):
            card = CardEnc.atleast([v[a, b, b] for b in range(n)], k, vpool=sat.pool,
                                   encoding=EncType.seqcounter).clauses
            # idempotent case: every row competes with row 0; otherwise only the rows of non-idempotent elements
            # (a clause set C with the literal v[a,a,a] added to each clause encodes 'a*a = a or C')
            sat.clauses += card if case == "idempotent" else [cl + [v[a, a, a]] for cl in card]
    T = parse(LAWS[num])[1]          # the law is x = y * T
    for x in range(n):
        for y in range(n):
            asg = {"x": x, "y": y}
            wT = sat._encode(T, asg)
            sat.clauses += [[-v[y, a, x], wT[a]] for a in range(n)]
            if num == 677:           # T = x * S
                wS = sat._encode(T[1], asg)
                sat.clauses += [[-v[y, b, x], -v[x, a, b], wS[a]] for a in range(n) for b in range(n)]
            else:                    # T = S * y
                wS = sat._encode(T[0], asg)
                sat.clauses += [[-v[y, b, x], -v[a, y, b], wS[a]] for a in range(n) for b in range(n)]
    return sat, law


def solve_case(job):
    num, n, case, lam, ell, budget, checker = job
    sat, law = build(num, n, case, lam, ell)
    nv = sat.pool.top
    t0 = time.perf_counter()
    with Cadical153(bootstrap_with=sat.clauses, with_proof=True) as s:
        s.conf_budget(budget)
        ok = s.solve_limited()
        conflicts = s.accum_stats()["conflicts"]
        model = s.get_model() if ok else None
        proof = s.get_proof() if ok is False else None
    out = {"law": num, "n": n, "case": case, "lam": list(lam), "ell": ell, "conflicts": conflicts,
           "status": {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[ok], "clauses": len(sat.clauses)}
    times = {"solve_s": round(time.perf_counter() - t0, 2)}
    if ok:
        table = sat.table_from_model(model)
        out["model_verified"] = bool(satisfies(table, law))
        out["model"] = table.tolist()
    if ok is False:
        with tempfile.TemporaryDirectory() as d:
            cnf, prf = os.path.join(d, "f.cnf"), os.path.join(d, "f.drat")
            with open(cnf, "w") as fh:
                fh.write(f"p cnf {nv} {len(sat.clauses)}\n")
                fh.writelines(" ".join(map(str, c)) + " 0\n" for c in sat.clauses)
            with open(prf, "w") as fh:
                fh.write("\n".join(proof) + "\n")
            out["cnf_sha256"] = hashlib.sha256(open(cnf, "rb").read()).hexdigest()
            out["proof_lines"] = len(proof)
            del proof
            if checker:
                t1 = time.perf_counter()
                res = subprocess.run([checker, cnf, prf], capture_output=True, text=True, timeout=6 * 3600)
                out["drat_trim"] = "VERIFIED" if "s VERIFIED" in res.stdout else "NOT VERIFIED"
                times["check_s"] = round(time.perf_counter() - t1, 2)
            else:
                out["drat_trim"] = "checker unavailable"
    # progress on stderr only (not part of the results)
    print(f"[EXP-C05-08] {num}/{n} {case} {lam}/{ell}: {out['status']} {conflicts} conflicts "
          f"{out.get('drat_trim', '')} {times}", file=sys.stderr, flush=True)
    return out, times


def run():
    checker = drat_path()
    jobs = [(num, n, case, lam, ell, BUDGET[n], checker)
            for num in LAWS for n in ORDERS for case, lam, ell in cases(n)]
    with get_context("fork").Pool(WORKERS) as pool:
        done = pool.map(solve_case, jobs, chunksize=1)
    instances = [r for r, _ in done]
    timings = {f"{r['law']}/{r['n']}/{r['case']}/{'.'.join(map(str, r['lam']))}/{r['ell']}": t for r, t in done}
    verdict = {}
    for num in LAWS:
        for n in ORDERS:
            rs = [r for r in instances if r["law"] == num and r["n"] == n]
            if any(r["status"] == "SAT" and r["model_verified"] for r in rs):
                verdict[f"{num}/{n}"] = "model found"
            elif all(r["status"] == "UNSAT" and r.get("drat_trim") == "VERIFIED" for r in rs):
                verdict[f"{num}/{n}"] = "no model (every case certified)"
            elif all(r["status"] == "UNSAT" for r in rs):
                verdict[f"{num}/{n}"] = "no model (not all proofs checked)"
            else:
                verdict[f"{num}/{n}"] = "UNDECIDED"
    unknown = [(r["law"], r["n"], r["case"], r["lam"], r["ell"]) for r in instances if r["status"] == "UNKNOWN"]
    rejected = [(r["law"], r["n"], r["lam"], r["ell"]) for r in instances if r.get("drat_trim") == "NOT VERIFIED"]
    return {
        "checker": bool(checker),
        "verdict": verdict,
        "instances": instances,
        "unknown_instances": unknown,
        "rejected_proofs": rejected,
        "timings": timings,
        "summary": [
            "verdicts: " + "; ".join(f"{k}: {v}" for k, v in verdict.items()),
            f"{len(instances)} instances; UNSAT certified by drat-trim: "
            f"{sum(r.get('drat_trim') == 'VERIFIED' for r in instances)}; SAT (model re-checked): "
            f"{sum(r['status'] == 'SAT' for r in instances)}; UNKNOWN: {len(unknown)}; rejected proofs: {len(rejected)}",
            "UNKNOWN instances: " + (", ".join(f"{a}/{b} {c} {d}/{e}" for a, b, c, d, e in unknown) or "none"),
        ],
    }
