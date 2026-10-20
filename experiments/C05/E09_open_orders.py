"""EXP-C05-09: the orders n <= 10 that EXP-C05-03 left undecided, for every open ETP law of the form x = y * T.

The certified case split of EXP-C05-08 (proofs/paper/C05.md, Lemmas 7-9; systems/magma_split.py) applies to every
law x = y * T: rows of finite models are permutations, and for T = S * y also the columns (Lemma 7, generalised in
Lean as right_mul_bijective_of_law). Each (law, n) is decided by running its cases in a fixed order until a model
is found (re-checked on its table) or every case is refuted by a DRAT proof that drat-trim verifies. Controls at
the same sizes, whose answers are known from EXP-C05-03, EXP-C05-06, EXP-C05-07 or the ETP notes, are decided the
same way. Laws 1516 and 1719 have another shape and are not treated.
"""

import os
from multiprocessing import get_context

from experiments.C05.E03_frontier_push import LAWS
from systems.magma_split import decide, drat_path

META = {
    "id": "EXP-C05-09",
    "cycle": "C05",
    "title": "Open orders of the ETP laws x = y*T: certified case split for every (law, n <= 10) left UNKNOWN by EXP-C05-03",
    "agent": "Formal Verifier",
    "question": "Which of the orders n <= 10 left UNKNOWN by EXP-C05-03 are in the spectra of the open ETP laws "
                "467, 501, 670, 704, 883, 907, 1076, 1083, 1110, 1279, 1286?",
    "hypothesis": "H-C05-H: the case split of EXP-C05-08 decides all 15 open pairs within a budget of 4 million "
                  "conflicts per case, and agrees with every control.",
    "assumptions": ["rows of finite models of x = y*T are permutations (Lean: left_mul_bijective_of_law); for "
                    "T = S*y also the columns (Lean: right_mul_bijective_of_law)",
                    "the case split of proofs/paper/C05.md Lemma 8 is complete; the division clauses of Lemma 9, "
                    "generalised in systems/magma_split.py, are implied",
                    "CaDiCaL 1.5.3 with proof logging, fixed conflict budget per case; drat-trim for every UNSAT",
                    "per-case results may be resumed from a checkpoint directory (EXP_CHECKPOINT); every case is "
                    "deterministic, so resuming does not change the results"],
    "methodology": "For each pair (targets first, then controls) run the cases of Lemma 8 in their fixed order and stop "
                   "at the first model (verified on its table); otherwise certify every case UNSAT with drat-trim. "
                   "3 worker processes, one pair per worker at a time.",
    "falsification": "A control that disagrees with its known answer, or a proof that drat-trim rejects, would expose an "
                     "error; a target with an UNKNOWN case and no model stays undecided.",
}

TARGETS = [(467, 10), (501, 10), (670, 10), (704, 10), (907, 10), (1076, 10), (1083, 10), (1110, 10), (1279, 10),
           (1286, 10), (883, 9), (1076, 9), (670, 8), (907, 8), (1286, 8)]
# control -> known answer and its source
CONTROLS = {(704, 9): ("no model", "ETP notes: 'no 9'"), (1279, 9): ("no model", "ETP notes: 'no 9'"),
            (1076, 8): ("no model", "EXP-C05-06 (DRUP-certified)"),
            (467, 9): ("model", "EXP-C05-03"), (501, 9): ("model", "EXP-C05-03"),
            (670, 9): ("model", "EXP-C05-07 (linear model)"), (907, 9): ("model", "ETP notes"),
            (1083, 9): ("model", "EXP-C05-03"), (1110, 9): ("model", "EXP-C05-03"),
            (1286, 9): ("model", "EXP-C05-03"), (704, 8): ("model", "EXP-C05-03"),
            (883, 8): ("model", "EXP-C05-03"), (1279, 8): ("model", "EXP-C05-03")}
BUDGET = {8: 2_000_000, 9: 4_000_000, 10: 4_000_000}
WORKERS = 3


def _job(pair):
    num, n = pair
    return decide(LAWS[num][0], n, BUDGET[n], drat_path(), os.environ.get("EXP_CHECKPOINT"), label=f"{num}/{n}")


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
