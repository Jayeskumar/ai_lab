"""EXP-C05-11: law 677 at order 12 - a certified reduction to an explicit list of hard cases.

Whether law 677, x = y(x((yx)y)), has a model of order 12 is open in every source (ETP Zulip, January 2026:
exhaustive search is the only known method; the ETP's last open finite implication 677 => 255 makes the
spectrum of 677 of interest). By Lemma 8 of proofs/paper/C05.md a model of order 12 exists iff one of 195 case
CNFs is satisfiable. This experiment runs every case with a small conflict budget (200,000): each case refuted
within the budget is certified by a DRAT proof that drat-trim verifies; the others are listed. The result is the
statement "677 has a model of order 12 iff one of the listed CNFs (rebuilt by systems.magma_split.build) is
satisfiable", a hand-off for a finer split; it decides nothing about order 12 by itself.
"""

import os
from multiprocessing import get_context

from systems.magma_split import cases, drat_path, solve_case

META = {
    "id": "EXP-C05-11",
    "cycle": "C05",
    "title": "Law 677 at order 12: certified reduction of the 195 case CNFs to the hard ones",
    "agent": "Formal Verifier",
    "question": "Which of the 195 case CNFs of Lemma 8 for law 677 at order 12 can be refuted cheaply, with a "
                "certificate, and which remain?",
    "hypothesis": "No model is found within 200,000 conflicts per case; most cases are refuted and the difficulty "
                  "is concentrated in a small set (an exploratory triage found 57 hard cases).",
    "assumptions": ["Lemma 8 (complete case split) and Lemma 9 (division clauses) of proofs/paper/C05.md; Latin rows "
                    "only (finite models of 677 need not be right-cancellative)",
                    "CaDiCaL 1.5.3, 200,000 conflicts per case; drat-trim for every UNSAT",
                    "per-case checkpoints (EXP_CHECKPOINT) may be used to resume"],
    "methodology": "Run all 195 cases (3 worker processes, fixed order of results); certify UNSAT cases; verify any "
                   "model on its table; list the UNKNOWN cases with their CNF hashes.",
    "falsification": "A verified model would settle the question (677 would have a model of order 12); a rejected "
                     "proof would expose an error.",
}

LAW = "y(x((yx)y))"
N = 12
BUDGET = 200_000
WORKERS = 3


def _job(item):
    i, (case, lam, ell) = item
    rec, t = solve_case(LAW, N, case, lam, ell, BUDGET, drat_path(), os.environ.get("EXP_CHECKPOINT"))
    rec["index"] = i
    return rec, t


def run():
    items = list(enumerate(cases(N)))
    with get_context("fork").Pool(WORKERS) as pool:
        done = pool.map(_job, items, chunksize=1)
    records = [r for r, _ in done]
    timings = {str(r["index"]): t for r, t in done}
    unsat = [r for r in records if r["status"] == "UNSAT"]
    hard = [r for r in records if r["status"] == "UNKNOWN"]
    models = [r for r in records if r["status"] == "SAT" and r.get("model_verified")]
    return {
        "law": "x = y(x((yx)y))",
        "n": N,
        "budget": BUDGET,
        "records": records,
        "hard_cases": [{"index": r["index"], "case": r["case"], "lam": r["lam"], "ell": r["ell"],
                        "cnf_sha256": r["cnf_sha256"]} for r in hard],
        "models": [r["model"] for r in models],
        "timings": timings,
        "summary": [
            f"677 at order 12: {len(records)} cases; refuted and certified by drat-trim: "
            f"{sum(r.get('drat_trim') == 'VERIFIED' for r in unsat)} of {len(unsat)} UNSAT; models found: "
            f"{len(models)}; undecided within {BUDGET} conflicts: {len(hard)} "
            f"({sum(r['case'] == 'idempotent' for r in hard)} idempotent, "
            f"{sum(r['case'] != 'idempotent' for r in hard)} non-idempotent)",
            "so 677 has a model of order 12 iff one of the listed hard case CNFs is satisfiable" if not models else
            "a model of order 12 was found",
        ],
    }
