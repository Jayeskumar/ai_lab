"""Certified spectrum decisions for laws x = y * T by a complete case split (batch 1.2).

The method of EXP-C05-08 (proofs/paper/C05.md, Lemmas 7-9), for any law of the form x = y * T(x, y):

* every left translation of a finite model is a bijection (the law makes it onto), so "rows are permutations";
* if moreover T = S * y, every right translation is a bijection too (``columns_bijective``; Lean:
  ``right_mul_bijective_of_law`` in proofs/lean/Infinity/C05_QuasigroupLaws.lean), so the table is a Latin square;
* Lemma 8: a model of order n exists iff one of the CNFs (idempotent, lam, 1) or (non-idempotent, lam, ell) is
  satisfiable - row 0 is the canonical permutation of cycle type lam with 0 in a cycle of length ell, and the
  competing rows have at least lam.count(1) fixed points;
* Lemma 9, generalised: implied "division" clauses. y * a = x forces T = a; then, going down T, a node A * B whose
  left factor A is a variable has B = A \\ (A * B), and, when the columns are bijective, a node whose right factor
  B is a variable has A = (A * B) / B.

``decide`` runs the cases of one (law, n) in a fixed order and stops at the first verified model; an UNSAT case
carries a DRAT proof from CaDiCaL that drat-trim must verify. Per-case results can be checkpointed to a directory
so that an interrupted run resumes; every case is deterministic, so a resumed run gives the same results.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

from systems.magma import MagmaSAT, is_var, parse, satisfies

DEFAULT_DRAT = "/tmp/claude-0/-home-user-ai-lab/5e93bf16-791a-5608-a61f-d865140bf384/scratchpad/drat/drat-trim"


def drat_path():
    p = os.environ.get("DRAT_TRIM") or shutil.which("drat-trim") or DEFAULT_DRAT
    return p if os.path.exists(p) else None


def partitions(n, largest=None):
    largest = n if largest is None else largest
    if n == 0:
        yield ()
        return
    for p in range(min(n, largest), 0, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest


def cases(n):
    """The cases of Lemma 8, in a fixed order."""
    out = [("idempotent", lam, 1) for lam in partitions(n) if 1 in lam]
    out += [("non-idempotent", lam, ell) for lam in partitions(n) for ell in sorted(set(lam)) if ell >= 2]
    return out


def canonical_permutation(lam, ell):
    parts = list(lam)
    parts.remove(ell)
    perm, start = {}, 0
    for p in [ell] + parts:
        cyc = list(range(start, start + p))
        for i, a in enumerate(cyc):
            perm[a] = cyc[(i + 1) % p]
        start += p
    return perm


def inner_term(law: str):
    """T for a law x = y * T given as the string of its right-hand side; None if the law has another shape."""
    t = parse(law)
    if is_var(t) or t[0] != "y":
        return None
    return t[1]


def columns_bijective(law: str) -> bool:
    """True when T = S * y, so that right translations are bijective in finite models."""
    T = inner_term(law)
    return T is not None and not is_var(T) and T[1] == "y"


def _latin(sat, rows: bool):
    n, v, cls = sat.n, sat.v, []
    for a in range(n):
        for c in range(n):
            lits = [v[a, b, c] for b in range(n)] if rows else [v[b, a, c] for b in range(n)]
            cls += CardEnc.equals(lits, 1, vpool=sat.pool, encoding=EncType.pairwise).clauses
    return cls


def build(law: str, n: int, case: str, lam, ell):
    T = inner_term(law)
    assert T is not None, f"law {law} is not of the form x = y * T"
    cols = columns_bijective(law)
    identity = (parse(law), "x")
    sat = MagmaSAT(n, [identity])
    v = sat.v
    sat.clauses += _latin(sat, rows=True)
    if cols:
        sat.clauses += _latin(sat, rows=False)
    perm = canonical_permutation(lam, ell)
    sat.clauses += [[v[0, b, perm[b]]] for b in range(n)]
    k = lam.count(1)
    if case == "idempotent":
        sat.clauses += [[v[a, a, a]] for a in range(n)]
    if k:
        for a in range(1, n):
            card = CardEnc.atleast([v[a, b, b] for b in range(n)], k, vpool=sat.pool, encoding=EncType.seqcounter).clauses
            sat.clauses += card if case == "idempotent" else [cl + [v[a, a, a]] for cl in card]
    for x in range(n):
        for y in range(n):
            asg = {"x": x, "y": y}
            node = T
            if is_var(node):
                break
            w = sat._encode(node, asg)
            sat.clauses += [[-v[y, a, x], w[a]] for a in range(n)]
            while not is_var(node):
                A, B = node
                if is_var(A) and not is_var(B):              # B = A \ node
                    wB = sat._encode(B, asg)
                    av = asg[A]
                    sat.clauses += [[-w[t], -v[av, b, t], wB[b]] for t in range(n) for b in range(n)]
                    node, w = B, wB
                elif cols and is_var(B) and not is_var(A):    # A = node / B
                    wA = sat._encode(A, asg)
                    bv = asg[B]
                    sat.clauses += [[-w[t], -v[a, bv, t], wA[a]] for t in range(n) for a in range(n)]
                    node, w = A, wA
                else:
                    break
    return sat, identity


def _cnf_text(sat) -> str:
    lines = [f"p cnf {sat.pool.top} {len(sat.clauses)}"]
    lines += [" ".join(map(str, c)) + " 0" for c in sat.clauses]
    return "\n".join(lines) + "\n"


def solve_case(law, n, case, lam, ell, budget, checker, checkpoint=None):
    """Decide one case; returns (record, timings). With a checkpoint directory, a finished case is reused."""
    sat, identity = build(law, n, case, lam, ell)
    cnf = _cnf_text(sat)
    cnf_sha = hashlib.sha256(cnf.encode()).hexdigest()
    key = f"{cnf_sha}_{budget}"
    if checkpoint:
        f = os.path.join(checkpoint, key + ".json")
        if os.path.exists(f):
            with open(f) as fh:
                saved = json.load(fh)
            return saved["record"], dict(saved["timings"], from_checkpoint=True)
    rec = {"law": law, "n": n, "case": case, "lam": list(lam), "ell": ell, "cnf_sha256": cnf_sha,
           "clauses": len(sat.clauses)}
    t0 = time.perf_counter()
    with Cadical153(bootstrap_with=sat.clauses, with_proof=True) as s:
        s.conf_budget(budget)
        ok = s.solve_limited()
        rec["conflicts"] = s.accum_stats()["conflicts"]
        model = s.get_model() if ok else None
        proof = s.get_proof() if ok is False else None
    times = {"solve_s": round(time.perf_counter() - t0, 2)}
    rec["status"] = {True: "SAT", False: "UNSAT", None: "UNKNOWN"}[ok]
    if ok:
        table = sat.table_from_model(model)
        rec["model_verified"] = bool(satisfies(table, identity))
        rec["model"] = table.tolist()
    if ok is False:
        rec["proof_lines"] = len(proof)
        if checker:
            with tempfile.TemporaryDirectory() as d:
                fc, fp = os.path.join(d, "f.cnf"), os.path.join(d, "f.drat")
                with open(fc, "w") as fh:
                    fh.write(cnf)
                with open(fp, "w") as fh:
                    fh.write("\n".join(proof) + "\n")
                del proof
                t1 = time.perf_counter()
                res = subprocess.run([checker, fc, fp], capture_output=True, text=True, timeout=6 * 3600)
                rec["drat_trim"] = "VERIFIED" if "s VERIFIED" in res.stdout else "NOT VERIFIED"
                times["check_s"] = round(time.perf_counter() - t1, 2)
        else:
            rec["drat_trim"] = "checker unavailable"
    if checkpoint:
        os.makedirs(checkpoint, exist_ok=True)
        tmp = os.path.join(checkpoint, key + ".tmp")
        with open(tmp, "w") as fh:
            json.dump({"record": rec, "timings": times}, fh)
        os.replace(tmp, os.path.join(checkpoint, key + ".json"))
    return rec, times


def decide(law, n, budget, checker=None, checkpoint=None, label=""):
    """All cases of (law, n) in order, stopping at the first verified model. Returns (summary, records, timings)."""
    records, timings = [], []
    verdict = None
    for i, (case, lam, ell) in enumerate(cases(n)):
        rec, t = solve_case(law, n, case, lam, ell, budget, checker, checkpoint)
        rec["index"] = i
        records.append(rec)
        timings.append(t)
        print(f"[{label}] n={n} {case} {lam}/{ell}: {rec['status']} {rec['conflicts']} {rec.get('drat_trim', '')}",
              file=sys.stderr, flush=True)
        if rec["status"] == "SAT" and rec["model_verified"]:
            verdict = "model found"
            break
    if verdict is None:
        if all(r["status"] == "UNSAT" and r.get("drat_trim") == "VERIFIED" for r in records):
            verdict = "no model (every case certified)"
        elif all(r["status"] == "UNSAT" for r in records):
            verdict = "no model (not all proofs checked)"
        else:
            verdict = "UNDECIDED"
    print(f"[{label}] VERDICT n={n}: {verdict} after {len(records)} of {len(cases(n))} cases", file=sys.stderr,
          flush=True)
    summary = {"law": law, "n": n, "verdict": verdict, "cases_total": len(cases(n)), "cases_run": len(records),
               "unknown": [r["index"] for r in records if r["status"] == "UNKNOWN"],
               "rejected": [r["index"] for r in records if r.get("drat_trim") == "NOT VERIFIED"],
               "max_conflicts": max(r["conflicts"] for r in records),
               "proof_lines": sum(r.get("proof_lines", 0) for r in records)}
    return summary, records, timings
