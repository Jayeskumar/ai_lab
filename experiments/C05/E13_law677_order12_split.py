"""EXP-C05-13: law 677 at order 12 - the 57 hard cases of EXP-C05-11, each split by right cancellation.

EXP-C05-11 refuted 138 of the 195 case CNFs of Lemma 8 (proofs/paper/C05.md) for law 677 at order 12, with
certificates, and left 57. Every finite magma with Latin rows either has Latin columns too (a quasigroup) or has a
value missing from some column, so each remaining case is refuted iff both of its parts are
(systems.magma_split.build, part = "quasigroup" / "non-quasigroup"). In the quasigroup part the column division
clauses of Lemma 9 also apply. An exploratory probe refuted all 57 quasigroup parts within 276,000 conflicts and
left the non-quasigroup part of the first case undecided after 1,000,000; the non-quasigroup parts are therefore
run with a triage budget of 1,000,000 conflicts, to list the ones that need a finer split.
"""

import hashlib
import json
import os
from multiprocessing import get_context

from lab.paths import RESULTS
from systems.magma_split import _cnf_text, build, drat_path, solve_case

META = {
    "id": "EXP-C05-13",
    "cycle": "C05",
    "title": "Law 677 at order 12: the 57 hard cases of EXP-C05-11 split into quasigroup and non-quasigroup parts",
    "agent": "Formal Verifier",
    "question": "Are the 57 case CNFs that EXP-C05-11 left undecided refuted once each is split into its quasigroup "
                "part (Latin columns) and its non-quasigroup part (a value missing from some column)?",
    "hypothesis": "H-C05-K: every quasigroup part is refuted with a certificate (so 677 has no quasigroup model of "
                  "order 12); the non-quasigroup parts are open.",
    "assumptions": ["Lemma 8 and Lemma 9 of proofs/paper/C05.md; EXP-C05-11 for the other 138 cases",
                    "the 57 cases are rebuilt by systems.magma_split.build and must match the SHA-256 hashes listed "
                    "by EXP-C05-11", "CaDiCaL 1.5.3, 4,000,000 conflicts per quasigroup part and 1,000,000 per "
                    "non-quasigroup part (triage); drat-trim for every UNSAT",
                    "per-part checkpoints (EXP_CHECKPOINT) may be used to resume"],
    "methodology": "For each hard case of EXP-C05-11 check the hash of its rebuilt CNF, then solve its two parts "
                   "(3 worker processes, fixed order of results); certify UNSAT parts; verify any model on its table.",
    "falsification": "A verified model (677 would have a model of order 12), a rejected proof, or a quasigroup part "
                     "left UNKNOWN.",
}

LAW = "y(x((yx)y))"
N = 12
BUDGET = {"quasigroup": 4_000_000, "non-quasigroup": 1_000_000}
WORKERS = 3
PARTS = ("quasigroup", "non-quasigroup")


def _job(item):
    h, part = item
    rec, t = solve_case(LAW, N, h["case"], tuple(h["lam"]), h["ell"], BUDGET[part], drat_path(),
                        os.environ.get("EXP_CHECKPOINT"), part=part)
    rec["index"] = h["index"]
    return rec, t


def run():
    hard = json.load(open(RESULTS / "EXP-C05-11.json"))["results"]["hard_cases"]
    for h in hard:
        sat, _ = build(LAW, N, h["case"], tuple(h["lam"]), h["ell"])
        assert hashlib.sha256(_cnf_text(sat).encode()).hexdigest() == h["cnf_sha256"], h
    items = [(h, part) for h in hard for part in PARTS]
    with get_context("fork").Pool(WORKERS) as pool:
        done = pool.map(_job, items, chunksize=1)
    records = [r for r, _ in done]
    timings = {f"{r['index']}/{r['part']}": t for r, t in done}
    by_part = {p: [r for r in records if r["part"] == p] for p in PARTS}
    refuted = {p: [r for r in rs if r["status"] == "UNSAT" and r.get("drat_trim") == "VERIFIED"]
               for p, rs in by_part.items()}
    models = [r for r in records if r["status"] == "SAT" and r.get("model_verified")]
    open_parts = [{"index": r["index"], "part": r["part"], "case": r["case"], "lam": r["lam"], "ell": r["ell"],
                   "cnf_sha256": r["cnf_sha256"], "status": r["status"]}
                  for r in records if not (r["status"] == "UNSAT" and r.get("drat_trim") == "VERIFIED")]
    cases_refuted = sum(all(r["status"] == "UNSAT" and r.get("drat_trim") == "VERIFIED"
                            for r in records if r["index"] == h["index"]) for h in hard)
    if models:
        verdict = "a model of order 12 was found"
    elif cases_refuted == len(hard):
        verdict = "with EXP-C05-11, every case of Lemma 8 is refuted: 677 has no model of order 12"
    elif len(refuted["quasigroup"]) == len(hard):
        verdict = "with EXP-C05-11, 677 has no quasigroup model of order 12; non-quasigroup parts remain open"
    else:
        verdict = "undecided"
    return {
        "law": "x = y(x((yx)y))",
        "n": N,
        "budget": BUDGET,
        "records": records,
        "open_parts": open_parts,
        "models": [r["model"] for r in models],
        "timings": timings,
        "summary": [
            f"57 hard cases x 2 parts: quasigroup parts refuted and certified {len(refuted['quasigroup'])} of "
            f"{len(hard)}; non-quasigroup parts refuted and certified {len(refuted['non-quasigroup'])} of "
            f"{len(hard)}; models: {len(models)}; parts not refuted: {len(open_parts)}",
            verdict,
        ],
    }
