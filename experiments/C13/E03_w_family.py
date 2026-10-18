"""EXP-C13-03: the W-family (xy)z = x(y W(z)) - polynomial spectra a*P(a) = 1 (test of Theorem 3)."""

import time

from lab import oeis
from systems.anchored import (affine_form, affine_roots, affine_spectrum, affine_system, anchored_status,
                              is_affine_table, pstr)
from systems.magma import MagmaSAT, fill, shapes, to_str

META = {
    "id": "EXP-C13-03",
    "cycle": "C13",
    "title": "Anchored models of (xy)z = x(y W(z)) for every one-variable term W with at most 5 leaves",
    "agent": "Formal Verifier",
    "question": "Are the anchored models of (xy)z = x(y W(z)) exactly the affine tables x + a*y + 1 with "
                "a*c_W(a) = 1 (mod N), c_W(a) = sum over leaves of a^(right depth), as Theorem 3 of "
                "proofs/paper/C13.md asserts? Which arithmetic sets do these laws realise?",
    "hypothesis": "H-C13-4 (derived): for all 23 terms W with <= 5 leaves and all N <= 9 the number of anchored models "
                  "equals the number of roots of a*c_W(a) - 1 modulo N, and every model is affine.",
    "assumptions": ["complete SAT enumeration of anchored models (limit 100) for N = 1..9",
                    "spectra up to 200 from the root condition; OEIS lookups for the distinct polynomials"],
    "methodology": "For each W: build the law, compute c_W and the root counts; enumerate all anchored models with "
                   "MagmaSAT and test each for affinity and for the root condition; compare counts.",
    "falsification": "A model count differing from the root count, or a non-affine model.",
}


def one_var_terms(max_leaves):
    out = []
    for k in range(0, max_leaves):
        for sh in shapes(k):
            out.append(fill(sh, ["z"] * (k + 1)))
    return out


def c_poly(W):
    C, _ = affine_form(W)
    return dict(C).get("z", ())


def anchor(n):
    return lambda S: [[S.v[x, 0, (x + 1) % n]] for x in range(n)]


def run():
    t0 = time.perf_counter()
    rows, mismatches = [], []
    seen_P = {}
    for W in one_var_terms(5):
        law = ((("x", "y"), "z"), ("x", ("y", W)))
        P = c_poly(W)
        sysm = affine_system(law)
        counts = {}
        for N in range(1, 10):
            tables, complete = MagmaSAT(N, [law], extra=anchor(N)).enumerate(limit=100)
            roots = affine_roots(sysm, N)
            aff = [is_affine_table(T) for T in tables]
            ok = complete and len(tables) == len(roots) and all(f for f, _ in aff) and \
                sorted(a for _, a in aff) == sorted(roots)
            counts[N] = {"models": len(tables), "roots": len(roots), "ok": ok}
            if not ok:
                mismatches.append({"W": to_str(W), "N": N, "models": len(tables), "roots": len(roots)})
        spec = affine_spectrum(sysm, 200)
        key = P
        if key not in seen_P:
            seen_P[key] = {"P": pstr(P), "F": pstr((-1,) + tuple(P)), "spectrum_head": spec[:20], "W": to_str(W)}
        rows.append({"W": to_str(W), "P": pstr(P), "counts": counts, "spectrum_head": spec[:16]})
    lookups = {}
    for P, info in seen_P.items():
        spec = affine_spectrum(affine_system(((("x", "y"), "z"), ("x", ("y", _term_with_P(info["W"]))))), 300)
        if len(spec) >= 8 and len(spec) < 300:
            r = oeis.novelty_check(spec[:40])
            lookups[info["P"]] = {"status": r.get("status"), "hits": [h["anumber"] + " " + h["name"][:80]
                                                                       for h in r.get("hits", [])[:3]],
                                  "spectrum_head": spec[:16]}
    return {"rows": rows, "mismatches": mismatches, "distinct_P": list(seen_P.values()), "oeis": lookups,
            "runtime_s": round(time.perf_counter() - t0, 1),
            "summary": [f"{len(rows)} terms W; N = 1..9; mismatches with Theorem 3: {len(mismatches)}",
                        f"{len(seen_P)} distinct polynomials P = c_W: " + ", ".join(v["P"] for v in seen_P.values()),
                        "OEIS: " + "; ".join(f"[{k}] {v['status']} {v['hits'][:1]}" for k, v in lookups.items())]}


def _term_with_P(wstr):
    from systems.magma import parse
    return parse(wstr)
