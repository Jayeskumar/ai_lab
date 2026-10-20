"""EXP-C05-10: the next open orders (11-13) of the six ETP laws x = y*(S*y), whose finite models are quasigroups.

For x = y * (S * y) both translations of a finite model are bijective (Lean: right_mul_bijective_of_law,
proofs/lean/Infinity/C05_QuasigroupLaws.lean), so the case split of systems/magma_split.py runs with Latin rows
and columns and three levels of division clauses; at order 10 these laws took seconds per case (EXP-C05-09). The
orders treated here are those not settled by linear models over GF(q) (EXP-C05-07, which gives members at every
prime power listed there) or by direct products of known models. Order 14 of law 1313 was dropped from this
experiment after its first case exceeded the budget (4 million conflicts) in a trial run; it needs a finer split.

Controls. Every known model at the target sizes - all linear models x*y = ax + by over GF(11) and GF(13) of the six
laws, and the product of the linear models of law 1083 over GF(3) and GF(4) (order 12) - is relabelled as in
Lemma 8 and must satisfy the CNF of its case (systems.magma_split.admits), so the extra clauses provably do not
exclude it; in addition the full decision procedure must find a model for 1110 and 1279 at order 11. (Order 12 of
1083 was first run as a decision control, but its known model lies in case 189 of 195 and the earlier cases need
up to 1.6 million conflicts each, about a day in all; the known-model check tests the same encoding directly.)
"""

import os
import time
from multiprocessing import get_context

import numpy as np

from experiments.C05.E03_frontier_push import LAWS
from experiments.C05.E07_finite_field_models import coefficients, field_tables
from systems.magma import parse
from systems.magma_split import admits, decide, drat_path

META = {
    "id": "EXP-C05-10",
    "cycle": "C05",
    "title": "Open orders 11-13 of the quasigroup laws 1076, 1110, 1279, 1286, 1313 (certified case split)",
    "agent": "Formal Verifier",
    "question": "Do the ETP laws 1076, 1110, 1279, 1286, 1313 - whose finite models are quasigroups - have models of "
                "the orders 11-13 that linear models and direct products leave open?",
    "hypothesis": "H-C05-I: the case split decides every pair within 4 million conflicts per case; the decision "
                  "controls 1110 and 1279 at order 11 have models, and every known model at orders 11-13 satisfies "
                  "the CNF of its case.",
    "assumptions": ["as EXP-C05-09; Latin columns by right_mul_bijective_of_law",
                    "orders with a linear model over GF(q) (EXP-C05-07) are members and are not re-decided",
                    "spectra are closed under direct products (any equational law)"],
    "methodology": "Decide each pair with systems.magma_split.decide (cases of Lemma 8 in their fixed order, stop at "
                   "the first verified model, otherwise every case refuted with a drat-trim-verified DRAT proof); 3 "
                   "worker processes; per-case checkpoints (EXP_CHECKPOINT). Known-model controls with "
                   "systems.magma_split.admits.",
    "falsification": "A decision control without a model, a known model excluded by its case CNF, a rejected proof, "
                     "or an UNKNOWN case.",
}

# open after EXP-C05-07 (linear models) and products: 11 and 13 are primes without a linear model for these laws
TARGETS = [(1076, 12), (1110, 12), (1279, 12), (1286, 12), (1313, 12),
           (1110, 13), (1279, 13), (1076, 11), (1313, 11)]
CONTROLS = {(1110, 11): ("model", "linear models over GF(11), EXP-C05-07"),
            (1279, 11): ("model", "linear models over GF(11), EXP-C05-07")}
LAWS_QG = (1076, 1083, 1110, 1279, 1286, 1313)
BUDGET = 4_000_000
WORKERS = 3


def _job(pair):
    num, n = pair
    return decide(LAWS[num][0], n, BUDGET, drat_path(), os.environ.get("EXP_CHECKPOINT"), label=f"{num}/{n}")


def linear_models(law, q):
    """All tables x*y = a x + b y over GF(q) satisfying x = law, with their (a, b)."""
    add, mul, _ = field_tables(q)
    a, b = (m.ravel() for m in np.meshgrid(np.arange(q), np.arange(q), indexing="ij"))
    al, be = coefficients(parse(law), add, mul, a, b)
    return [((int(a[h]), int(b[h])), add[mul[int(a[h])][:, None], mul[int(b[h])][None, :]])
            for h in np.nonzero((al == 1) & (be == 0))[0]]


def known_models():
    out = []
    for num in LAWS_QG:
        for q in (11, 13):
            out += [(num, f"linear over GF({q}), (a, b) = {ab}", T) for ab, T in linear_models(LAWS[num][0], q)]
    (_, A), (_, B) = linear_models(LAWS[1083][0], 3)[0], linear_models(LAWS[1083][0], 4)[0]
    product = [[int(A[x // 4, y // 4]) * 4 + int(B[x % 4, y % 4]) for y in range(12)] for x in range(12)]
    out.append((1083, "product of the linear models over GF(3) and GF(4)", product))
    return out


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
    for num, source, T in known_models():
        checks.append({"law": num, "model": source, **admits(LAWS[num][0], T)})
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
            f"known models at orders 11-13 satisfying the CNF of their case: {len(checks) - len(excluded)} of "
            f"{len(checks)}",
            f"cases run: {sum(v['cases_run'] for v in out.values())}; UNSAT cases certified by drat-trim: "
            f"{sum(sum(r.get('drat_trim') == 'VERIFIED' for r in v['records']) for v in out.values())}; rejected "
            f"proofs: {sum(len(v['rejected']) for v in out.values())}; UNKNOWN cases: "
            f"{sum(len(v['unknown']) for v in out.values())}",
        ],
    }
