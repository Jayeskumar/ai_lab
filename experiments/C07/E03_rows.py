"""EXP-C07-03: are the rows of mex operations additively periodic? The Jacobsthal row of D[x^y]."""

import numpy as np

from lab import oeis
from systems.mex import additive_period, all_specs, spec_name, table

META = {
    "id": "EXP-C07-03",
    "cycle": "C07",
    "title": "Rows of mex operations: additive periodicity, and a Jacobsthal block-swap row",
    "agent": "Mathematical Explorer",
    "question": "Is every row b -> f(a, b) (a = 1..5) of every mex operation eventually additively periodic, "
                "f(a, b + p) = f(a, b) + s, as for Wythoff's game? What is row 2 of D[x^y]?",
    "hypothesis": "H-C07-4 (bold): every row of every mex operation of the family is eventually additively "
                  "periodic. H-C07-5 (from inspection of EXP-C07-02): row 2 of D[x^y], g(b) = mex(G u (b XOR G)) "
                  "with G = {g(b') : b' < b}, satisfies g(b) = b + J_k for J_(k+1) <= b < J_(k+1) + J_k and "
                  "g(b) = b - J_k for J_(k+1) + J_k <= b < J_(k+2) (k >= 1), J the Jacobsthal numbers.",
    "assumptions": ["rows a = 1..5 computed to b < 1500 for the first spec of each of the 134 distinct "
                    "operations of EXP-C07-01; a row counts as additively periodic if a period p <= 375 holds "
                    "on a checked tail of length >= max(200, 3p)",
                    "row 2 of D[x^y] recomputed to b < 2^15 by an independent bitset algorithm"],
    "methodology": "Rectangular mex tables (5 x 1500); additive_period on each row; independent recursion "
                   "g(b) = least v with v not in G and v XOR b not in G (bitsets); comparison with the "
                   "Jacobsthal block-swap formula; OEIS checks of the row and of |g(b) - b|.",
    "falsification": "H-C07-4: a row without additive period. H-C07-5: any b < 2^15 violating the formula.",
}

B = 1500


def jacobsthal_row(nb):
    """Independent computation of g(b) = min{v : v not in G, v ^ b not in G}, G = {g(b') : b' < b}."""
    size = 1 << (int(nb).bit_length() + 1)
    used = np.zeros(size, dtype=bool)
    idx = np.arange(size)
    g = np.zeros(nb, dtype=np.int64)
    for b in range(nb):
        bad = used | used[idx ^ b]
        v = int(np.argmin(bad))
        g[b] = v
        used[v] = True
    return g


def jacobsthal_formula(nb):
    J = [0, 1]
    while J[-1] < 4 * nb:
        J.append(J[-1] + 2 * J[-2])
    f = np.zeros(nb, dtype=np.int64)
    for k in range(1, len(J) - 2):
        s, L = J[k + 1], J[k]
        for b in range(s, min(s + L, nb)):
            f[b] = b + L
        for b in range(s + L, min(J[k + 2], nb)):
            f[b] = b - L
    return f


def run():
    seen, rows = set(), []
    for spec in all_specs():
        key = table(spec, 64).tobytes()
        if key in seen:
            continue
        seen.add(key)
        T = table(spec, 6, B)
        per = {a: additive_period(T[a]) for a in range(1, 6)}
        rows.append({"spec": spec_name(spec), "periods": {str(a): (list(v) if v else None) for a, v in per.items()}})
    n_rows = 5 * len(rows)
    n_periodic = sum(1 for r in rows for v in r["periods"].values() if v)
    fully = [r["spec"] for r in rows if all(r["periods"].values())]
    none_ = [r["spec"] for r in rows if not any(r["periods"].values())]
    # the Jacobsthal row
    nb = 1 << 15
    g = jacobsthal_row(nb)
    f = jacobsthal_formula(nb)
    T2 = table((False, False, (3,)), 3, 1500)[2]
    mism = np.nonzero(g != f)[0]
    is_involution = bool(np.array_equal(g[g[g < nb]], np.arange(nb)[g < nb]))
    look_row = oeis.novelty_check(g[:40].tolist())
    look_abs = oeis.novelty_check(np.abs(g - np.arange(nb))[1:41].tolist())
    return {
        "n_operations": len(rows),
        "rows_tested": n_rows,
        "rows_additively_periodic": n_periodic,
        "operations_all_rows_periodic": len(fully),
        "operations_no_row_periodic": none_,
        "rows": rows,
        "jacobsthal": {"n": nb, "independent_vs_mex_table_agree_1500": bool(np.array_equal(g[:1500], T2)),
                       "formula_mismatches": int(mism.size), "first_mismatch": int(mism[0]) if mism.size else None,
                       "involution_on_range": is_involution, "first_terms": g[:32].tolist(),
                       "oeis_row": {"status": look_row["status"], "hits": look_row.get("hits", [])[:3]},
                       "oeis_abs_offset": {"status": look_abs["status"], "hits": look_abs.get("hits", [])[:3]}},
        "summary": [f"{n_periodic}/{n_rows} rows (a = 1..5, b < {B}) additively periodic; {len(fully)} of "
                    f"{len(rows)} operations have all five rows periodic; {len(none_)} have none",
                    f"D[x^y] row 2: independent algorithm = mex table (b < 1500): "
                    f"{bool(np.array_equal(g[:1500], T2))}; Jacobsthal block-swap formula mismatches for b < {nb}: "
                    f"{int(mism.size)}; involution: {is_involution}",
                    f"OEIS: row {look_row['status']}, |g(b)-b| {look_abs['status']}"],
    }
