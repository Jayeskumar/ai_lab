"""Skeptic batch 1.1 -- detached, restartable runner for the 677/1313 case CNFs of my encoding.

Each finished case is appended at once as one JSON line to the output file, so a killed run loses at most the
case in progress; cases already present in the output file are skipped on restart.

usage: python c05_certify_runner.py <mode> <law> <n> <indices|all> <out.jsonl> [budget] [cap_seconds]
  mode = lemma8-cert : the Lemma-8 CNF (c05_independent.build_lemma8) solved with DRAT proof logging and the
                       proof checked by drat-trim (proof deleted afterwards)
  mode = sbmin       : my SB-min CNF (c05_independent.build with a case), solver only
  mode = sbmin-r1    : SB-min refined by R1 (see the report, section 2.4): in a case with ell = 1, every
                       non-idempotent row has >= k+1 fixed points; solver only
  mode = sbmin-r1-cert: the sbmin-r1 CNF with DRAT proof logging, checked by drat-trim
  mode = sbmin-r1-noncancel: the sbmin-r1 CNF plus "some column contains a repeated value" (677 only; the
                       split covers every model up to isomorphism, and right-cancellativity is invariant)
Division clauses are used iff SKEPTIC_DIV=1 (as in c05_independent).
"""
import hashlib
import itertools
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c05_independent as C  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

DRAT = C.DRAT
SCRATCH = C.SCRATCH


def lemma8_cases(n):
    cs = [("idempotent", tuple(sorted(lam)), 1) for lam in C.partitions(n) if 1 in lam]
    cs += [("non-idempotent", tuple(sorted(lam)), ell) for lam in C.partitions(n) for ell in sorted(set(lam))
           if ell >= 2]
    return cs


def r1_extra(F, lam, ell, n):
    """R1 in a case with ell = 1: for a >= 1, a*a = a or a has >= k+1 fixed points (aux-free)."""
    k = list(lam).count(1)
    if ell != 1 or k + 1 > n:
        return
    for a in range(1, n):
        for U in itertools.combinations(range(n), n - (k + 1) + 1):
            cl = [F.m(a, b, b) for b in U]
            if a not in U:
                cl.append(F.m(a, a, a))
            F.cl.append(cl)


def main():
    mode, law, n, sel, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    budget = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] != "0" else None
    cap = float(sys.argv[7]) if len(sys.argv) > 7 else None
    if mode == "lemma8-cert":
        cases = lemma8_cases(n)
    else:
        cases = [("sbmin",) + c for c in C.my_cases(n)]
    idx = list(range(len(cases))) if sel == "all" else [int(z) for z in sel.split(",")]
    done = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                done.add(json.loads(line)["i"])
            except Exception:
                pass
    os.makedirs(SCRATCH, exist_ok=True)
    for i in idx:
        if i in done:
            continue
        kind, lam, ell = cases[i]
        cert = mode.endswith("-cert")
        if mode == "lemma8-cert":
            F = C.build_lemma8(law, n, kind, lam, ell)
        else:
            F = C.build(law, n, (lam, ell))
            if mode.startswith("sbmin-r1"):
                r1_extra(F, lam, ell, n)
            if mode == "sbmin-r1-noncancel":
                top = n ** 3
                zs = []
                for b in range(n):
                    for a1 in range(n):
                        for a2 in range(a1 + 1, n):
                            for c in range(n):
                                top += 1
                                zs.append(top)
                                F.cl.append([-top, F.m(a1, b, c)])
                                F.cl.append([-top, F.m(a2, b, c)])
                F.cl.append(zs)
        t0 = time.time()
        r = {"i": i, "mode": mode, "case": kind, "lam": list(lam), "ell": ell, "division": C.DIVISION}
        with Solver(name="cadical195", bootstrap_with=F.cl, with_proof=cert) as s:
            if budget:
                s.conf_budget(budget)
                ok = s.solve_limited()
            elif cap:
                # time cap via repeated conflict budgets of 100k
                ok = None
                while ok is None and time.time() - t0 < cap:
                    s.conf_budget(100_000)
                    ok = s.solve_limited()
            else:
                ok = s.solve()
            r["status"] = {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[ok]
            r["conflicts"] = s.accum_stats().get("conflicts")
            r["solve_s"] = round(time.time() - t0, 1)
            if ok:
                T = C.table_from_model(s.get_model(), n)
                r["model_ok"] = C.holds(T, law)
                r["model"] = T
            if ok is False and cert:
                proof = s.get_proof()
        if ok is False and cert:
            base = os.path.join(SCRATCH, f"{mode}_{law}_n{n}_case{i}_{os.getpid()}")
            with open(base + ".cnf", "w") as fh:
                fh.write(f"p cnf {n ** 3} {len(F.cl)}\n")
                for c in F.cl:
                    fh.write(" ".join(map(str, c)) + " 0\n")
            with open(base + ".drat", "w") as fh:
                fh.write("\n".join(proof) + "\n")
            r["proof_lines"] = len(proof)
            del proof
            r["cnf_sha256"] = hashlib.sha256(open(base + ".cnf", "rb").read()).hexdigest()
            t1 = time.time()
            res = subprocess.run([DRAT, base + ".cnf", base + ".drat"], capture_output=True, text=True,
                                 timeout=3 * 3600)
            r["drat_trim"] = [l for l in res.stdout.splitlines() if l.startswith("s ")]
            r["verified"] = r["drat_trim"] == ["s VERIFIED"]
            r["check_s"] = round(time.time() - t1, 1)
            os.remove(base + ".drat")
            os.remove(base + ".cnf")
        with open(out, "a") as fh:
            fh.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main()
