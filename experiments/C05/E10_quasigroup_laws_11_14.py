"""EXP-C05-10: the next open orders (11-14) of the six ETP laws x = y*(S*y), whose finite models are quasigroups.

For x = y * (S * y) both translations of a finite model are bijective (Lean: right_mul_bijective_of_law,
proofs/lean/Infinity/C05_QuasigroupLaws.lean), so the case split of systems/magma_split.py runs with Latin rows
and columns and three levels of division clauses; at order 10 these laws took seconds per case (EXP-C05-09). The
orders treated here are those not settled by linear models over GF(q) (EXP-C05-07, which gives members at every
prime power listed there) or by direct products of known models. Order 12 of law 1083 is a control: 3 and 4 are
in its spectrum (EXP-C05-03), so the direct product of the two models has order 12.
"""

import os
from multiprocessing import get_context

from experiments.C05.E03_frontier_push import LAWS
from systems.magma_split import decide, drat_path

META = {
    "id": "EXP-C05-10",
    "cycle": "C05",
    "title": "Open orders 11-14 of the quasigroup laws 1076, 1110, 1279, 1286, 1313 (certified case split)",
    "agent": "Formal Verifier",
    "question": "Do the ETP laws 1076, 1110, 1279, 1286, 1313 - whose finite models are quasigroups - have models of "
                "the orders 11-14 that linear models and direct products leave open?",
    "hypothesis": "H-C05-I: the case split decides every pair within 4 million conflicts per case; the control 1083 "
                  "at order 12 has a model.",
    "assumptions": ["as EXP-C05-09; Latin columns by right_mul_bijective_of_law",
                    "orders with a linear model over GF(q) (EXP-C05-07) are members and are not re-decided",
                    "spectra are closed under direct products (any equational law)"],
    "methodology": "Decide each pair with systems.magma_split.decide (cases of Lemma 8 in their fixed order, stop at "
                   "the first verified model, otherwise every case refuted with a drat-trim-verified DRAT proof); 3 "
                   "worker processes; per-case checkpoints (EXP_CHECKPOINT).",
    "falsification": "The control without a model, a rejected proof, or an UNKNOWN case leaves the pair undecided.",
}

# open after EXP-C05-07 (linear models) and products: 11 and 13 are primes without a linear model for these laws
TARGETS = [(1313, 14), (1076, 12), (1110, 12), (1279, 12), (1286, 12), (1313, 12),
           (1110, 13), (1279, 13), (1076, 11), (1313, 11)]
CONTROLS = {(1083, 12): ("model", "direct product of the models of orders 3 and 4 (EXP-C05-03)")}
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
    verdicts = {k: v["verdict"] for k, v in out.items() if v["role"] == "target"}
    return {
        "pairs": out,
        "target_verdicts": verdicts,
        "control_errors": control_errors,
        "checker": bool(drat_path()),
        "timings": timings,
        "summary": [
            "targets: " + "; ".join(f"{k}: {v}" for k, v in verdicts.items()),
            f"controls agreeing with their known answers: {len(CONTROLS) - len(control_errors)} of {len(CONTROLS)}"
            + (f" (disagreeing: {control_errors})" if control_errors else ""),
            f"cases run: {sum(v['cases_run'] for v in out.values())}; UNSAT cases certified by drat-trim: "
            f"{sum(sum(r.get('drat_trim') == 'VERIFIED' for r in v['records']) for v in out.values())}; rejected "
            f"proofs: {sum(len(v['rejected']) for v in out.values())}; UNKNOWN cases: "
            f"{sum(len(v['unknown']) for v in out.values())}",
        ],
    }
