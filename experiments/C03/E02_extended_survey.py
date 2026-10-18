"""EXP-C03-02: extended survey (p, q, r, s <= 5) with two independent loop finders."""

import itertools

from systems.srs_termination import (bounded_evidence, check_loop, check_matrix, find_loop_forward_closures,
                                     find_loop_strategies, find_matrix_interpretation, rule)

META = {
    "id": "EXP-C03-02",
    "cycle": "C03",
    "title": "Extended termination survey of 0^p 1^q -> 1^r 0^s for p, q, r, s <= 5",
    "agent": "Mathematical Skeptic",
    "question": "Does H-C03-3 survive a larger family and a stronger loop finder, and are any growing rules "
                "provably terminating by matrix interpretations?",
    "hypothesis": "H-C03-3: the rule is non-terminating iff r > q, s > p and (r >= 2q or s >= 2p); "
                  "equivalently it terminates iff r <= q or s <= p or (r < 2q and s < 2p).",
    "assumptions": ["count-decreasing (s < p or r < q) and conserving (s = p or r = q) rules are terminating by "
                    "the theorems of proofs/paper/C03.md and are not re-searched",
                    "both-growing rules: forward closures (<= 40 letters, <= 40000 pairs), then leftmost/"
                    "rightmost strategies from 0^a 1^b (a <= 3p, b <= max(4q^2, 3q), <= 3000 steps, <= 6000 "
                    "letters), then matrix interpretations (d = 2 entries 0..4; upper-triangular d = 3 entries "
                    "0..3), then bounded evidence from all words of length <= 12"],
    "methodology": "As in EXP-C03-01 with the additional strategy-based loop finder; every certificate is "
                   "re-checked independently.",
    "falsification": "A loop for a rule with r < 2q and s < 2p (or with r <= q or s <= p), or a matrix "
                     "termination proof for a rule predicted non-terminating.",
}

TIERS = [(2, list(range(5)), False), (3, list(range(4)), True)]


def run():
    rows = []
    for p, q, r, s in itertools.product(range(1, 6), repeat=4):
        l, rr = rule(p, q, r, s)
        row = {"rule": [p, q, r, s]}
        if s < p or r < q:
            row.update(region="count-decreasing", status="TERMINATING", certificate={"kind": "counting proof"})
        elif s == p or r == q:
            row.update(region="conserving", status="TERMINATING", certificate={"kind": "conservation proof"})
        else:
            row["region"] = "both-growing"
            loop = find_loop_forward_closures(l, rr, max_len=40, max_pairs=40_000)
            method = "forward closures"
            if loop is None:
                loop = find_loop_strategies(l, rr)
                method = "strategy"
            if loop is not None:
                assert check_loop(l, rr, loop)
                row.update(status="NON-TERMINATING", certificate={"kind": "loop", "method": method,
                                                                  "start": loop["start"],
                                                                  "steps": loop["steps"],
                                                                  "end_length": len(loop["end"])})
            else:
                mats = None
                for d, ent, ut in TIERS:
                    mats = find_matrix_interpretation(p, q, r, s, d=d, entries=ent, upper_triangular=ut)
                    if mats:
                        break
                if mats is not None:
                    assert check_matrix(l, rr, mats)
                    row.update(status="TERMINATING", certificate={"kind": "matrix", "M0": mats["0"],
                                                                  "M1": mats["1"]})
                else:
                    row.update(status="UNKNOWN", certificate={"kind": "bounded evidence",
                                                              **bounded_evidence(l, rr, max_word=12)})
        rows.append(row)
    st = {tuple(r["rule"]): r["status"] for r in rows}

    def pred3(p, q, r, s):
        return "NON-TERMINATING" if (s > p and r > q and (r >= 2 * q or s >= 2 * p)) else "TERMINATING"

    def pred2(p, q, r, s):
        return "TERMINATING" if (r < 2 * q or s < 2 * p) else "NON-TERMINATING"

    def pred1(p, q, r, s):
        return "TERMINATING" if (s <= p or r <= q) else "NON-TERMINATING"

    hyp = {}
    for name, f in (("H-C03-1", pred1), ("H-C03-2", pred2), ("H-C03-3", pred3)):
        contra = [list(k) for k, v in st.items() if v != "UNKNOWN" and v != f(*k)]
        hyp[name] = {"n_contradictions": len(contra), "examples": contra[:10]}
    unknown = [r for r in rows if r["status"] == "UNKNOWN"]
    unknown_pred = {tuple(r["rule"]): pred3(*r["rule"]) for r in unknown}
    sym = [list(k) for k, v in st.items() if st[(k[1], k[0], k[3], k[2])] != v]
    loops = [r for r in rows if r["status"] == "NON-TERMINATING"]
    return {
        "rows": rows,
        "hypotheses": hyp,
        "unknown_rules": [r["rule"] for r in unknown],
        "unknown_predicted_by_H3": sorted(set(unknown_pred.values())),
        "unknown_max_derivation_len12": {str(r["rule"]): r["certificate"]["max_derivation"].get(12)
                                         for r in unknown},
        "loops_by_method": {m: sum(r["certificate"]["method"] == m for r in loops)
                            for m in ("forward closures", "strategy")},
        "longest_loop_steps": max(len(r["certificate"]["steps"]) for r in loops),
        "symmetry_violations": sym,
        "summary": [
            f"625 rules: {sum(v == 'TERMINATING' for v in st.values())} terminating (proved or certified), "
            f"{len(loops)} non-terminating (loop certificates: "
            f"{sum(r['certificate']['method'] == 'forward closures' for r in loops)} by forward closures, "
            f"{sum(r['certificate']['method'] == 'strategy' for r in loops)} by strategies), {len(unknown)} unknown",
            f"contradictions: H-C03-1 {hyp['H-C03-1']['n_contradictions']}, H-C03-2 {hyp['H-C03-2']['n_contradictions']}, "
            f"H-C03-3 {hyp['H-C03-3']['n_contradictions']}; H-C03-3 predicts {sorted(set(unknown_pred.values()))} "
            f"for all unknown rules",
            f"matrix-certified growing rules: {sum(r['region'] == 'both-growing' and r['status'] == 'TERMINATING' for r in rows)}; "
            f"symmetry violations: {len(sym)}",
        ],
    }
