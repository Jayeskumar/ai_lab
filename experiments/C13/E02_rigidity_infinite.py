"""EXP-C13-02: are the infinite affine spectra the true anchored spectra? (search for non-affine models)"""

import time

from systems.anchored import affine_classes, law_from_key, law_size, law_str, pstr, rigidity_profile

META = {
    "id": "EXP-C13-02",
    "cycle": "C13",
    "title": "Affine rigidity of laws with infinite non-trivial affine spectra",
    "agent": "Mathematical Skeptic",
    "question": "For laws whose affine spectrum is infinite but not all N (golden, x^2+x+1, -1 square, 2 square, "
                "odd, plastic, tribonacci, ...), does every anchored model of size N <= 8 come from an affine "
                "table x*y = x + a*y + 1? If so, the true spectrum agrees with the arithmetic set for N <= 8.",
    "hypothesis": "H-C13-2 (bold): for every law with at most 4 leaves per side (3 variables) or 5 leaves per side "
                  "(2 variables) whose affine spectrum is infinite and not all N, every anchored model is affine.",
    "assumptions": ["the 3 shortest laws of every such affine class (3var<=4 and 2var<=5 families of EXP-C13-01)",
                    "N = 2..8; SAT with all affine tables blocked; conflict budget 300,000; UNKNOWN recorded",
                    "a first run (4 laws per class, N <= 9, budget 2,000,000) was stopped after 17 CPU-minutes"],
    "methodology": "For each selected law and N, add one blocking clause per affine table x + a*y + 1 to the "
                   "anchored SAT encoding; SAT means a non-affine model exists (the table is recorded for N <= 5), "
                   "UNSAT means every model is affine.",
    "falsification": "A non-affine anchored model of any selected law.",
}


def run():
    t0 = time.perf_counter()
    selected = []
    for fam, (vars_, ml) in {"3var_le4": (("x", "y", "z"), 4), "2var_le5": (("x", "y"), 5)}.items():
        classes = affine_classes(vars_, ml, nmax=120)
        for spec, items in classes.items():
            if len(spec) == 120 or spec[-1] < 60:      # all N, or finite (handled in EXP-C13-03)
                continue
            keys = sorted((k for _, ks in items for k in ks), key=lambda k: (law_size(k), k))[:3]
            for k in keys:
                selected.append((fam, spec, k))
    rows = []
    for fam, spec, k in selected:
        prof = rigidity_profile([law_from_key(k)], range(2, 9), budget=300_000)
        rows.append({"family": fam, "law": law_str(k), "affine_spectrum_head": list(spec[:12]),
                     "profile": prof,
                     "non_affine_N": [n for n, p in prof.items() if p["non_affine"] == "SAT"],
                     "unknown_N": [n for n, p in prof.items() if p["non_affine"] == "UNKNOWN"]})
    rigid = [r["law"] for r in rows if not r["non_affine_N"] and not r["unknown_N"]]
    nonrigid = [(r["law"], r["non_affine_N"]) for r in rows if r["non_affine_N"]]
    return {"n_laws": len(rows), "rows": rows, "rigid": rigid, "non_rigid": nonrigid,
            "timings": {"total_s": round(time.perf_counter() - t0, 1)},
            "summary": [f"{len(rows)} laws from infinite non-trivial affine classes tested for N = 2..8",
                        f"rigid (no non-affine model, no UNKNOWN): {len(rigid)}",
                        f"non-rigid: {len(nonrigid)} e.g. {nonrigid[:6]}",
                        f"UNKNOWN instances: {sum(len(r['unknown_N']) for r in rows)}"]}
