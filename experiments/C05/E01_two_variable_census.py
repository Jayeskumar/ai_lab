"""EXP-C05-01: spectra of all nontrivial two-variable identities t = x with 2-4 operations."""

import time

from systems.magma import (classify_trivially, identities_t_eq_x, is_quasigroup, mirror, models_up_to_iso,
                           spectrum, to_str)

META = {
    "id": "EXP-C05-01",
    "cycle": "C05",
    "title": "Spectrum census of two-variable identities t = x (2-4 operations), sizes 1-6",
    "agent": "Mathematical Explorer",
    "question": "Which sizes of finite magmas can satisfy a single invented identity t(x, y) = x?",
    "hypothesis": "H-C05-1 (bold): every identity t = x has spectrum {1} or all positive integers - single "
                  "identities cannot carve out arithmetic restrictions on the size of a model.",
    "assumptions": ["System B: magmas without any assumed law", "identities up to renaming of variables",
                    "'nontrivial' = x occurs in t but is neither its leftmost nor its rightmost leaf (otherwise a "
                    "projection is a model of every size, or x is absent and only n = 1 works)",
                    "SAT (CaDiCaL via pysat), conflict budget 1e6 per instance"],
    "methodology": "For each nontrivial identity: SAT model existence for n = 1..6; exhaustive model enumeration "
                   "with isomorphism rejection for n <= 3; record whether all enumerated models are quasigroups. "
                   "Mirror images (t read right-to-left) are paired; their spectra must agree. (Larger n are "
                   "enumerated, and n = 7..10 decided, only for restricted identities in EXP-C05-02.)",
    "falsification": "Any identity whose spectrum within 1..6 is neither {1} nor everything refutes H-C05-1.",
}

SIZES = range(1, 7)


def run():
    rows = []
    t0 = time.time()
    for k in (2, 3, 4):
        for t, _ in identities_t_eq_x(k, ("x", "y")):
            if classify_trivially(t) != "nontrivial":
                continue
            law = (t, "x")
            spec = spectrum([law], SIZES, conf_budget=1_000_000)
            counts = {}
            all_qg = True
            for n in (1, 2, 3):
                if spec[n] != "SAT":
                    counts[n] = [0, 0, True]
                    continue
                total, iso, complete, reps = models_up_to_iso([law], n, limit=50_000)
                counts[n] = [total, iso, complete]
                all_qg &= all(is_quasigroup(T) for T in reps)
            pattern = "".join({"SAT": "1", "UNSAT": "0", "UNKNOWN": "?"}[spec[n]] for n in SIZES)
            rows.append({"identity": to_str(t) + " = x", "ops": k, "mirror": to_str(mirror(t)) + " = x",
                         "spectrum_1_6": pattern, "models_total_iso_complete_n1_3": counts,
                         "all_small_models_quasigroups": all_qg})
    by_pattern = {}
    for r in rows:
        by_pattern.setdefault(r["spectrum_1_6"], []).append(r["identity"])
    mirror_mismatch = []
    idx = {r["identity"]: r for r in rows}
    for r in rows:
        m = idx.get(r["mirror"])
        if m is not None and m["spectrum_1_6"] != r["spectrum_1_6"]:
            mirror_mismatch.append((r["identity"], r["mirror"]))
    restricted = {p: ids for p, ids in by_pattern.items() if p not in ("111111", "100000")}
    return {
        "n_identities": len(rows),
        "rows": rows,
        "patterns": {p: len(v) for p, v in sorted(by_pattern.items())},
        "restricted_patterns": restricted,
        "mirror_mismatches": mirror_mismatch,
        "timings": {"seconds": round(time.time() - t0, 1)},
        "summary": [
            f"{len(rows)} nontrivial identities; spectrum patterns over n=1..6: "
            f"{ {p: len(v) for p, v in sorted(by_pattern.items())} }",
            f"identities with a restricted spectrum (neither {{1}} nor all): {sum(len(v) for v in restricted.values())}",
            f"mirror pairs with different spectra (must be 0): {len(mirror_mismatch)}",
        ],
    }
