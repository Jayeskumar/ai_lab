"""EXP-C03-01: termination survey of 0^p 1^q -> 1^r 0^s for p, q, r, s in 1..4."""

import itertools

from systems.srs_termination import (bounded_evidence, check_loop, check_matrix, find_loop_forward_closures,
                                     find_matrix_interpretation, rule)

META = {
    "id": "EXP-C03-01",
    "cycle": "C03",
    "title": "Termination survey of the 256 rules 0^p 1^q -> 1^r 0^s (p, q, r, s <= 4)",
    "agent": "Mathematical Explorer",
    "question": "Which rules 0^p 1^q -> 1^r 0^s terminate, and what separates terminating from looping rules?",
    "hypothesis": "Three competing hypotheses are tested. H-C03-1 (naive): terminates iff s <= p or r <= q "
                  "(some letter count never grows). H-C03-2 (director's first guess): terminates iff r < 2q or "
                  "s < 2p. H-C03-3 (after the first loops): non-terminating iff s > p, r > q and "
                  "(r >= 2q or s >= 2p).",
    "assumptions": ["System A over {0,1}; one rule", "loop search = forward closures with right and left "
                    "extensions, words <= 40 letters, <= 40000 closure pairs",
                    "matrix interpretations over N: d = 2 (entries 0..4) and upper-triangular d = 3 (0..3), "
                    "d = 4 (0..1)"],
    "methodology": "For each rule: (1) proven regions by counting (s < p or r < q) or conservation (s = p or "
                   "r = q); (2) forward-closure loop search, every certificate re-checked step by step; (3) if no "
                   "loop, exhaustive matrix-interpretation search, certificate re-checked in exact arithmetic; "
                   "(4) otherwise bounded evidence: reachable sets from all words of length <= 12 containing "
                   "the left-hand side.",
    "falsification": "A loop certificate for a rule predicted terminating, or a termination certificate for a "
                     "rule predicted non-terminating.",
}

TIERS = [(2, list(range(5)), False), (3, list(range(4)), True), (4, [0, 1], True)]


def region(p, q, r, s):
    if s < p or r < q:
        return "count-decreasing"
    if s == p or r == q:
        return "conserving"
    return "both-growing"


def run():
    rows = []
    for p, q, r, s in itertools.product(range(1, 5), repeat=4):
        l, rr = rule(p, q, r, s)
        row = {"rule": [p, q, r, s], "region": region(p, q, r, s)}
        loop = find_loop_forward_closures(l, rr, max_len=40, max_pairs=40_000)
        if loop is not None:
            assert check_loop(l, rr, loop)
            row["status"] = "NON-TERMINATING"
            row["certificate"] = {"kind": "loop", **loop}
        else:
            mats = None
            for d, ent, ut in TIERS:
                mats = find_matrix_interpretation(p, q, r, s, d=d, entries=ent, upper_triangular=ut)
                if mats:
                    break
            if mats is not None:
                assert check_matrix(l, rr, mats)
                row["status"] = "TERMINATING"
                row["certificate"] = {"kind": "matrix", "dimension": len(mats["0"]), "M0": mats["0"],
                                      "M1": mats["1"]}
            elif row["region"] != "both-growing":
                row["status"] = "TERMINATING"
                row["certificate"] = {"kind": "counting/conservation proof (proofs/paper/C03.md)"}
            else:
                row["status"] = "UNKNOWN"
                row["certificate"] = {"kind": "bounded evidence", **bounded_evidence(l, rr, max_word=12)}
        rows.append(row)
    st = {tuple(r["rule"]): r["status"] for r in rows}

    def pred1(p, q, r, s):
        return "TERMINATING" if (s <= p or r <= q) else "NON-TERMINATING"

    def pred2(p, q, r, s):
        return "TERMINATING" if (r < 2 * q or s < 2 * p) else "NON-TERMINATING"

    def pred3(p, q, r, s):
        return "NON-TERMINATING" if (s > p and r > q and (r >= 2 * q or s >= 2 * p)) else "TERMINATING"

    verdict = {}
    for name, f in (("H-C03-1", pred1), ("H-C03-2", pred2), ("H-C03-3", pred3)):
        contra = [list(k) for k, v in st.items() if v != "UNKNOWN" and v != f(*k)]
        verdict[name] = {"contradicted_by": contra[:12], "n_contradictions": len(contra),
                         "unknown_rules_predicted": sorted({f(*k) for k, v in st.items() if v == "UNKNOWN"})}
    sym = [list(k) for k, v in st.items() if st[(k[1], k[0], k[3], k[2])] != v]
    counts = {}
    for r in rows:
        key = f"{r['region']} / {r['status']} / {r['certificate']['kind'].split(' ')[0]}"
        counts[key] = counts.get(key, 0) + 1
    return {
        "rows": rows,
        "status_counts": counts,
        "hypotheses": verdict,
        "symmetry_violations": sym,
        "unknown": [r["rule"] for r in rows if r["status"] == "UNKNOWN"],
        "summary": [
            f"256 rules: {sum(r['status'] == 'TERMINATING' for r in rows)} terminating (certified), "
            f"{sum(r['status'] == 'NON-TERMINATING' for r in rows)} non-terminating (loop certificates), "
            f"{sum(r['status'] == 'UNKNOWN' for r in rows)} unknown",
            f"contradictions: H-C03-1 {verdict['H-C03-1']['n_contradictions']}, H-C03-2 "
            f"{verdict['H-C03-2']['n_contradictions']}, H-C03-3 {verdict['H-C03-3']['n_contradictions']}",
            f"unknown rules: {[r['rule'] for r in rows if r['status'] == 'UNKNOWN']}",
            f"reversal-complement symmetry violations: {len(sym)}",
        ],
    }
