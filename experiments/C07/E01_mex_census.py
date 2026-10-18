"""EXP-C07-01: census of the 512 mex-defined operations (Conway's nim-sum and nim-product are two of them)."""

import hashlib

import numpy as np

from systems.mex import (NIM_PRODUCT, NIM_SUM, all_specs, associativity_violations, closed_below,
                         distributes_over_xor, identity_elements, is_commutative, is_latin, spec_name, table)

META = {
    "id": "EXP-C07-01",
    "cycle": "C07",
    "title": "Census of mex-defined binary operations: closure, associativity, identities, distributivity",
    "agent": "Mathematical Explorer",
    "question": "Which operations f(a,b) = mex V(a,b) of the family (L, R, D) (options f(a',b), f(a,b') and XOR "
                "combinations of f(a',b), f(a,b'), f(a',b')) are associative, commutative, closed on initial "
                "segments, have identities, distribute over XOR?",
    "hypothesis": "H-C07-1 (bold): apart from trivial operations, the only associative operations of the family are "
                  "Conway's nim-sum and nim-product. H-C07-2 (bold): every commutative operation of the family is "
                  "closed on the 'Fermat' segments [0, 2^(2^m)), m = 0, 1, 2, like the nimbers.",
    "assumptions": ["tables computed for a, b < 64", "associativity tested on all evaluable triples in [0,16)^3 and "
                    "[0,64)^3 (triples whose intermediate value is >= 64 are skipped and counted)",
                    "properties on finite windows only; an operation is called associative here if no violation "
                    "is found on the evaluated triples"],
    "methodology": "Compute the 64 x 64 table of every spec (vectorised mex, cross-checked against a plain-set "
                   "implementation); group identical tables; record commutativity, closure on [0, 2^j), "
                   "associativity violations, identities, XOR-distributivity and the Latin property on [0, 16).",
    "falsification": "H-C07-1: an associative non-trivial operation other than XOR and nim-product. H-C07-2: a "
                     "commutative operation not closed on [0,2), [0,4) or [0,16).",
}

N = 64


def fingerprint(T):
    return hashlib.sha256(np.ascontiguousarray(T).tobytes()).hexdigest()[:16]


def run():
    groups = {}
    for spec in all_specs():
        T = table(spec, N)
        fp = fingerprint(T)
        g = groups.setdefault(fp, {"specs": [], "table": T})
        g["specs"].append(spec_name(spec))
    rows = []
    xor = np.arange(N)[:, None] ^ np.arange(N)[None, :]
    nimprod = table(NIM_PRODUCT, N)
    for fp, g in groups.items():
        T = g["table"]
        closed = [k for k in (1, 2, 4, 8, 16, 32, 64) if closed_below(T, k)]
        v16, e16 = associativity_violations(T, 16)
        v64, e64 = associativity_violations(T, 64)
        row = {
            "fingerprint": fp,
            "specs": g["specs"],
            "n_specs": len(g["specs"]),
            "commutative": is_commutative(T),
            "closed_segments": closed,
            "assoc_violations_16": [v16, e16],
            "assoc_violations_64": [v64, e64],
            "identities_16": identity_elements(T, 16) if 16 in closed else None,
            "xor_distributive_16": distributes_over_xor(T, 16) if 16 in closed else None,
            "latin_16": is_latin(T, 16) if 16 in closed else None,
            "max_value": int(T.max()),
            "row1": T[1, :24].tolist(),
            "diag": [int(T[i, i]) for i in range(24)],
            "is_xor": bool(np.array_equal(T, xor)),
            "is_nim_product": bool(np.array_equal(T, nimprod)),
            "is_zero": bool((T == 0).all()),
        }
        row["associative_window"] = (v16 == 0 and v64 == 0)
        rows.append(row)
    rows.sort(key=lambda r: (-r["associative_window"], -r["n_specs"]))
    assoc = [r for r in rows if r["associative_window"]]
    comm = [r for r in rows if r["commutative"]]
    comm_not_fermat = [r["specs"][0] for r in comm if not all(k in r["closed_segments"] for k in (2, 4, 16))]
    return {
        "n_specs": len(all_specs()),
        "n_distinct_operations": len(rows),
        "n_commutative": len(comm),
        "n_associative_on_window": len(assoc),
        "associative": [{"specs": r["specs"][:6], "n_specs": r["n_specs"], "is_xor": r["is_xor"],
                         "is_nim_product": r["is_nim_product"], "is_zero": r["is_zero"], "row1": r["row1"][:12],
                         "diag": r["diag"][:12], "closed": r["closed_segments"]} for r in assoc],
        "commutative_not_closed_on_2_4_16": comm_not_fermat,
        "rows": rows,
        "summary": [
            f"512 specs -> {len(rows)} distinct operations on [0,64)^2; commutative: {len(comm)}; "
            f"associative on the tested windows: {len(assoc)}",
            "associative operations: " + "; ".join(
                f"{r['specs'][0]} (x{r['n_specs']}, xor={r['is_xor']}, nimprod={r['is_nim_product']}, zero={r['is_zero']})"
                for r in assoc),
            f"commutative operations not closed on [0,2), [0,4), [0,16): {len(comm_not_fermat)}",
        ],
    }
