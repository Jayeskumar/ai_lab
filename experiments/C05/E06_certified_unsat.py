"""EXP-C05-06: DRUP-certified non-membership (UNSAT) for new spectrum gaps found in EXP-C05-03."""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time

from pysat.solvers import Glucose4

from lab.paths import RESULTS
from systems.magma import MagmaSAT, parse

from experiments.C05.E03_frontier_push import LAWS, latin_rows

META = {
    "id": "EXP-C05-06",
    "cycle": "C05",
    "title": "Certified UNSAT: DRUP proofs checked by drat-trim for new spectrum gaps",
    "agent": "Formal Verifier",
    "question": "Can the non-memberships found by SAT beyond the ETP notes be certified by an independent proof "
                "checker instead of trusting the solver?",
    "hypothesis": "Each such UNSAT instance yields a DRUP refutation that drat-trim verifies.",
    "assumptions": ["drat-trim (github.com/marijnheule/drat-trim, master; built locally with gcc -O2), located via "
                    "the DRAT_TRIM environment variable or the scratchpad build path",
                    "the CNF includes two sound additions: 'rows are permutations' for laws x = y*(...) (Lean: "
                    "left_mul_bijective_of_law) and the relabelling symmetry break 0*0 in {0,1}",
                    "Glucose 4 (pysat) with proof logging, conflict budget 3e6 per instance (exceeded = no certificate)"],
    "methodology": "Rebuild the exact CNF of EXP-C05-03 for each (law, n) reported UNSAT beyond the notes, solve "
                   "with Glucose4(with_proof=True), write DIMACS + DRUP files, run drat-trim, record its verdict and "
                   "the SHA-256 of both files.",
    "falsification": "drat-trim rejecting a proof (or Glucose finding a model) would contradict EXP-C05-03.",
}

DEFAULT_DRAT = "/tmp/claude-0/-home-user-ai-lab/5e93bf16-791a-5608-a61f-d865140bf384/scratchpad/drat/drat-trim"


def drat_path():
    p = os.environ.get("DRAT_TRIM") or shutil.which("drat-trim") or DEFAULT_DRAT
    return p if os.path.exists(p) else None


def run():
    checker = drat_path()
    e03 = json.load(open(RESULTS / "EXP-C05-03.json"))["results"]
    out = []
    t0 = time.time()
    for row in e03["rows"]:
        num = row["etp_number"]
        t = LAWS[num][0]
        law = (parse(t), "x")
        for n in row["decided_beyond_notes"]:
            if row["status_n_2_10"][str(n)] != "UNSAT":
                continue
            sat = MagmaSAT(n, [law])
            if t.startswith("y("):
                sat.clauses += latin_rows(sat)
            sat.clauses.append([sat.v[0, 0, 0], sat.v[0, 0, 1]])
            nv = sat.pool.top
            with Glucose4(bootstrap_with=sat.clauses, with_proof=True) as g:
                g.conf_budget(3_000_000)
                ok = g.solve_limited()
                proof = g.get_proof() if ok is False else None
            status = {True: "SAT", False: "UNSAT", None: "BUDGET EXCEEDED (no certificate)"}[ok]
            rec = {"law": num, "n": n, "glucose": status, "clauses": len(sat.clauses), "variables": nv}
            if ok is False and checker:
                with tempfile.TemporaryDirectory() as d:
                    cnf = os.path.join(d, "f.cnf")
                    prf = os.path.join(d, "f.drup")
                    with open(cnf, "w") as fh:
                        fh.write(f"p cnf {nv} {len(sat.clauses)}\n")
                        for c in sat.clauses:
                            fh.write(" ".join(map(str, c)) + " 0\n")
                    with open(prf, "w") as fh:
                        fh.write("\n".join(proof) + "\n")
                    res = subprocess.run([checker, cnf, prf], capture_output=True, text=True, timeout=3000)
                    verdict = "VERIFIED" if "s VERIFIED" in res.stdout else "NOT VERIFIED"
                    rec.update({"drat_trim": verdict,
                                "cnf_sha256": hashlib.sha256(open(cnf, "rb").read()).hexdigest(),
                                "proof_lines": len(proof)})
            elif ok is False:
                rec["drat_trim"] = "checker unavailable"
            out.append(rec)
    verified = [r for r in out if r.get("drat_trim") == "VERIFIED"]
    return {
        "checker": checker,
        "instances": out,
        "timings": {"seconds": round(time.time() - t0, 1)},
        "summary": [f"{len(out)} new UNSAT instances re-solved with proof logging; drat-trim VERIFIED "
                    f"{len(verified)}: {[(r['law'], r['n']) for r in verified]}",
                    f"not verified / other: {[(r['law'], r['n'], r.get('drat_trim')) for r in out if r not in verified]}"],
    }
