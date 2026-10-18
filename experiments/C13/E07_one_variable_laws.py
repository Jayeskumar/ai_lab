"""EXP-C13-07: anchored spectra of all one-variable laws t1(x) = t2(x) with at most 5 leaves per side, N <= 12."""

import itertools
import time

from systems.anchored import affine_roots, affine_system, anchored_status, divisors, pstr
from systems.magma import fill, shapes, to_str

META = {
    "id": "EXP-C13-07",
    "cycle": "C13",
    "title": "Spectra of one-variable laws and the failure of divisor-closure",
    "agent": "Mathematical Explorer",
    "question": "For every law t1(x) = t2(x) with t1 != t2 one-variable terms of at most 5 leaves, which N <= 12 "
                "admit an anchored model? Which spectra violate divisor-closure, and is every spectrum either {1} or "
                "cofinite?",
    "hypothesis": "H-C13-5 (bold): every one-variable law has anchored spectrum {1} or a cofinite set (all N beyond "
                  "some bound), because such a law only constrains the orbit of each element under its own "
                  "diagonal maps.",
    "assumptions": ["253 laws (23 terms with <= 5 leaves; unordered pairs)", "N = 1..12, complete SAT (conflict "
                    "budget 2,000,000; UNKNOWN recorded)", "cofiniteness is only suggested, not proved, by N <= 12"],
    "methodology": "MagmaSAT with the anchor for every law and N; divisor-closure violations (N, d); spectra "
                   "patterns; affine roots for comparison.",
    "falsification": "A law whose spectrum up to 12 is neither {1} nor of the form 'all N >= n0 plus a set of small "
                     "N' (e.g. a law with models exactly at the even sizes).",
}


def one_var_terms(max_leaves):
    out = []
    for k in range(0, max_leaves):
        for sh in shapes(k):
            out.append(fill(sh, ["x"] * (k + 1)))
    return out


def run():
    t0 = time.perf_counter()
    terms = one_var_terms(5)
    rows, violations, unknown = [], [], []
    patterns = {}
    for t1, t2 in itertools.combinations(terms, 2):
        law = (t1, t2)
        sysm = affine_system(law)
        st = {}
        for n in range(1, 13):
            if affine_roots(sysm, n) if sysm else True:
                st[n] = "SAT"
            else:
                st[n], _ = anchored_status([law], n)
        spec = [n for n in st if st[n] == "SAT"]
        unk = [n for n in st if st[n] == "UNKNOWN"]
        v = [(n, d) for n in spec for d in divisors(n)[1:-1] if st[d] == "UNSAT"]
        name = f"{to_str(t1)} = {to_str(t2)}"
        missing = [n for n in range(1, 13) if st[n] == "UNSAT"]
        rows.append({"law": name, "spectrum_le12": spec, "missing_le12": missing, "unknown": unk,
                     "affine_system": [pstr(p) for p in sysm], "violations": v})
        patterns.setdefault(tuple(missing), []).append(name)
        if v:
            violations.append({"law": name, "pairs": v, "missing": missing})
        if unk:
            unknown.append(name)
    # spectrum shapes
    trivial = [r["law"] for r in rows if r["spectrum_le12"] == [1]]
    cofinite_like = [r["law"] for r in rows if r["spectrum_le12"] != [1] and
                     all(st_n in r["spectrum_le12"] for st_n in range(7, 13))]
    other = [r["law"] for r in rows if r["law"] not in trivial and r["law"] not in cofinite_like]
    pat = sorted(((len(v), list(k), v[:3]) for k, v in patterns.items()), reverse=True)
    return {"n_laws": len(rows), "rows": rows, "violations": violations, "unknown": unknown,
            "trivial_only": trivial, "models_for_all_7_to_12": cofinite_like, "other": other,
            "missing_patterns": [{"count": c, "missing_le12": m, "examples": e} for c, m, e in pat],
            "runtime_s": round(time.perf_counter() - t0, 1),
            "summary": [f"{len(rows)} one-variable laws; spectrum {{1}}: {len(trivial)}; models for every N in 7..12: "
                        f"{len(cofinite_like)}; other: {len(other)} {other[:4]}",
                        f"divisor-closure violations: {len(violations)} e.g. "
                        f"{[(v['law'], v['missing']) for v in violations[:4]]}",
                        "missing-size patterns (count, missing N<=12): " +
                        "; ".join(f"{c}x{m}" for c, m, _ in pat[:10]),
                        f"UNKNOWN: {len(unknown)}"]}
