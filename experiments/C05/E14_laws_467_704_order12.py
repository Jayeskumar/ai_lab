"""EXP-C05-14: order 12 of the ETP laws 467 and 704 (certified case split, Latin rows only).

The orders 11-13 that linear models over GF(q) (EXP-C05-07) and direct products leave open for the laws 467, 501,
670, 704, 883 and 907 are 467/12, 501/11, 501/12, 670/12, 670/13, 704/12, 883/12 and 907/12. Exploratory probes
(12 sampled case CNFs per pair, 300,000 conflicts, no certificates) found 467/12 and 704/12 easy, a model of 501 at
order 12 (recorded in EXP-C05-15, which also settles 501 completely), and hard cases (UNKNOWN at 300,000, and for
883 at 1,000,000 conflicts with Latin columns) for 670/12, 670/13, 883/12 and 907/12, which are left for a finer
split. The case split runs with Latin rows and the left-inverse division clauses only (Lemma 8 and 9 of
proofs/paper/C05.md); for 704 the columns are Latin too (Lean: law704_right_bijective), but the plain encoding is
used, so the result does not depend on that lemma.

Controls: the decision procedure must find models of 467 and 704 at order 11 (both in case 12 of 139), and every
linear model of the six laws over GF(11) and GF(13) must satisfy the CNF of its own case (systems.magma_split.admits).
"""

import os
import time
from multiprocessing import get_context

from experiments.C05.E03_frontier_push import LAWS
from experiments.C05.E10_quasigroup_laws_11_14 import linear_models
from systems.magma_split import admits, decide, drat_path

META = {
    "id": "EXP-C05-14",
    "cycle": "C05",
    "title": "Order 12 of the ETP laws 467 and 704 (certified case split, Latin rows only)",
    "agent": "Formal Verifier",
    "question": "Do the ETP laws 467, x = y(x(x(yy))), and 704, x = y(y((xx)y)), have models of order 12?",
    "hypothesis": "H-C05-L: neither has a model of order 12, and the case split decides both within 4 million "
                  "conflicts per case; the decision controls have models and every known model at orders 11 and 13 "
                  "of the six laws satisfies the CNF of its case.",
    "assumptions": ["Lemma 8 and Lemma 9 of proofs/paper/C05.md (Latin rows; no column constraint)",
                    "orders with a linear model over GF(q) (EXP-C05-07) are members and are not re-decided",
                    "spectra are closed under direct products (any equational law)",
                    "CaDiCaL 1.5.3, 4,000,000 conflicts per case; drat-trim for every UNSAT; per-case checkpoints "
                    "(EXP_CHECKPOINT) may be used to resume"],
    "methodology": "Decide each pair with systems.magma_split.decide (cases of Lemma 8 in their fixed order, stop at "
                   "the first verified model, otherwise every case refuted with a drat-trim-verified DRAT proof); 3 "
                   "worker processes. Known-model controls with systems.magma_split.admits.",
    "falsification": "A decision control without a model, a known model excluded by its case CNF, a rejected proof, "
                     "or an UNKNOWN case (which leaves its pair undecided).",
}

TARGETS = [(467, 12), (704, 12)]
CONTROLS = {(467, 11): ("model", "linear model over GF(11), EXP-C05-07"),
            (704, 11): ("model", "linear models over GF(11), EXP-C05-07")}
LAWS_ROWS = (467, 501, 670, 704, 883, 907)
BUDGET = 4_000_000
WORKERS = 3


def _job(pair):
    num, n = pair
    return decide(LAWS[num][0], n, BUDGET, drat_path(), os.environ.get("EXP_CHECKPOINT"), label=f"{num}/{n}")


def run():
    pairs = TARGETS + list(CONTROLS)
    with get_context("fork").Pool(WORKERS) as pool:
        done = pool.map(_job, pairs, chunksize=1)
    out, timings, control_errors = {}, {}, []
    for (num, n), (summary, records, times) in zip(pairs, done):
        key = f"{num}/{n}"
        out[key] = {"role": "target" if (num, n) in TARGETS else "control", **summary,
                    "law": f"x = {LAWS[num][0]}", "records": records}
        timings[key] = times
        if (num, n) in CONTROLS:
            expected, source = CONTROLS[(num, n)]
            got = "model" if summary["verdict"] == "model found" else (
                "no model" if summary["verdict"].startswith("no model") else "undecided")
            out[key]["expected"] = f"{expected} ({source})"
            if got != expected:
                control_errors.append(key)
    checks, t0 = [], time.perf_counter()
    for num in LAWS_ROWS:
        for q in (11, 13):
            for ab, T in linear_models(LAWS[num][0], q):
                checks.append({"law": num, "model": f"linear over GF({q}), (a, b) = {ab}", **admits(LAWS[num][0], T)})
    timings["known_model_checks_s"] = round(time.perf_counter() - t0, 2)
    excluded = [c for c in checks if not (c["admitted"] and c["satisfies_law"])]
    verdicts = {k: v["verdict"] for k, v in out.items() if v["role"] == "target"}
    return {
        "pairs": out,
        "target_verdicts": verdicts,
        "control_errors": control_errors,
        "known_model_checks": checks,
        "checker": bool(drat_path()),
        "timings": timings,
        "summary": [
            "targets: " + "; ".join(f"{k}: {v}" for k, v in verdicts.items()),
            f"decision controls agreeing with their known answers: {len(CONTROLS) - len(control_errors)} of "
            f"{len(CONTROLS)}" + (f" (disagreeing: {control_errors})" if control_errors else ""),
            f"known models at orders 11 and 13 satisfying the CNF of their case: {len(checks) - len(excluded)} of "
            f"{len(checks)}",
            f"cases run: {sum(v['cases_run'] for v in out.values())}; UNSAT cases certified by drat-trim: "
            f"{sum(sum(r.get('drat_trim') == 'VERIFIED' for r in v['records']) for v in out.values())}; rejected "
            f"proofs: {sum(len(v['rejected']) for v in out.values())}; UNKNOWN cases: "
            f"{sum(len(v['unknown']) for v in out.values())}",
        ],
    }
