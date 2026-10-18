"""EXP-C03-03: the divisibility phenomenon - lifted loops versus terminating non-multiples."""

import itertools
import json

from lab.paths import RESULTS
from systems.rewriting import reachable
from systems.srs_termination import (bounded_evidence, check_loop, find_loop_forward_closures, find_loop_strategies,
                                     lift_zeros, mirror, rule)

META = {
    "id": "EXP-C03-03",
    "cycle": "C03",
    "title": "Divisibility: loops lift along 0 -> 0^p, non-multiples look terminating",
    "agent": "Mathematical Explorer",
    "question": "Why do (2,2,3,4) and (2,2,3,6) loop while (2,2,3,5) and (2,2,3,7) apparently terminate?",
    "hypothesis": "H-C03-4: 0^p 1^q -> 1^r 0^s is non-terminating iff (a) r >= 2q and s >= 2p, or (b) s >= 2p, "
                  "q < r < 2q and p | s, or (c) r >= 2q, p < s < 2p and q | r; otherwise it terminates. "
                  "Mechanism for (b): every rule (1, q, r, k) with q < r < 2q, k >= 2 loops, and the morphism "
                  "0 -> 0^p maps it onto (p, q, r, kp).",
    "assumptions": ["loop certificates re-checked step by step", "'terminating from u' is certified by a finite "
                    "reachable set (finitely branching rewriting: finite reachable set + no cycle = no infinite "
                    "derivation from u)"],
    "methodology": "Part A: loops for the base family (1, q, r, k), q <= 5, q < r < 2q, k <= 6. Part B: lift every "
                   "base loop to (p, q, r, kp), p <= 4, and verify. Part C: for p in {2,3}, q in {2,3,4}, "
                   "q < r < 2q, 2p <= s <= 3p+2: loop search, reachable sets from every 0^a 1^b (a <= 3p, b <= 3q+2) "
                   "and from every word of length <= 12 containing the left-hand side (reachable words up to 720 letters). Part D: re-examine the 29 "
                   "unknown rules of EXP-C03-02 using mirrors and lifts. (Reachable-set probes are run for the "
                   "non-divisible rules only; for divisible rules the loop certificate is the evidence.)",
    "falsification": "A base rule (1, q, r, k) without a loop although infinite growth is observed; a non-multiple "
                     "rule with a loop or an infinite reachable set; a multiple without a loop.",
}


def find_loop(l, r):
    c = find_loop_forward_closures(l, r, max_len=60, max_pairs=60_000)
    return c if c is not None else find_loop_strategies(l, r)


def reach_profile(l, r, amax, bmax, limit=30_000):
    big, largest = [], 0
    for a in range(l.count("0"), amax + 1):
        for b in range(l.count("1"), bmax + 1):
            R = reachable("0" * a + "1" * b, [(l, r)], limit=limit)
            if R is None:
                big.append([a, b])
            else:
                largest = max(largest, len(R))
    return big, largest


def run():
    # Part A: base family
    base, base_missing = {}, []
    for q in range(2, 6):
        for r in range(q + 1, 2 * q):
            for k in range(2, 7):
                l, rr = rule(1, q, r, k)
                c = find_loop(l, rr)
                if c is not None and check_loop(l, rr, c):
                    base[(q, r, k)] = c
                else:
                    base_missing.append([1, q, r, k])
    # Part B: lifts
    lifted_ok, lifted_bad = 0, []
    for (q, r, k), c in base.items():
        for p in range(2, 5):
            L = lift_zeros(c, p, q, r, k)
            if check_loop(*rule(p, q, r, k * p), L) and check_loop(*rule(q, p, k * p, r), mirror(L, p, q, r, k * p)):
                lifted_ok += 1
            else:
                lifted_bad.append([p, q, r, k * p])
    # Part C: divisible vs non-divisible
    partC = []
    for p in (2, 3):
        for q in (2, 3, 4):
            for r in range(q + 1, 2 * q):
                for s in range(2 * p, 3 * p + 3):
                    l, rr = rule(p, q, r, s)
                    loop = find_loop(l, rr)
                    if loop is None and s % p == 0 and (q, r, s // p) in base:
                        loop = lift_zeros(base[(q, r, s // p)], p, q, r, s // p)
                        loop = loop if check_loop(l, rr, loop) else None
                    row = {"rule": [p, q, r, s], "p_divides_s": s % p == 0, "loop_found": loop is not None}
                    if s % p:
                        big, largest = reach_profile(l, rr, 3 * p, 3 * q + 2)
                        ev = bounded_evidence(l, rr, max_word=12, limit=200_000, max_len_factor=60)
                        row.update({"starts_with_huge_reachable_set": len(big),
                                    "largest_finite_reachable_set": largest,
                                    "words_len_le_12_all_finite": ev["finite"] == ev["words"]})
                    partC.append(row)
    cons = [r for r in partC if r["p_divides_s"] != r["loop_found"]]
    nondiv_clean = all(r["starts_with_huge_reachable_set"] == 0 and r["words_len_le_12_all_finite"]
                       for r in partC if not r["p_divides_s"])
    # Part D: the unknowns of EXP-C03-02
    prev = json.load(open(RESULTS / "EXP-C03-02.json"))["results"]
    st = {tuple(r["rule"]): r for r in prev["rows"]}
    resolved, still = {}, []
    for k in map(tuple, prev["unknown_rules"]):
        p, q, r, s = k
        m = (q, p, s, r)
        cert = None
        if st[m]["status"] == "NON-TERMINATING":
            mc = st[m]["certificate"]
            cand = mirror({"start": mc["start"], "steps": mc["steps"]}, *m)
            if check_loop(*rule(*k), cand):
                cert = "mirror of " + str(list(m))
        if cert is None and p > 1 and s % p == 0 and (q, r, s // p) in base:
            if check_loop(*rule(*k), lift_zeros(base[(q, r, s // p)], p, q, r, s // p)):
                cert = f"lift of (1,{q},{r},{s // p})"
        if cert:
            resolved[str(list(k))] = cert
        else:
            still.append(list(k))

    def pred4(p, q, r, s):
        nt = (r >= 2 * q and s >= 2 * p) or (s >= 2 * p and q < r < 2 * q and s % p == 0) or \
             (r >= 2 * q and p < s < 2 * p and r % q == 0)
        return "NON-TERMINATING" if nt else "TERMINATING"

    final = {}
    for k, row in st.items():
        status = row["status"]
        if str(list(k)) in resolved:
            status = "NON-TERMINATING"
        final[k] = status
    contra4 = [list(k) for k, v in final.items() if v != "UNKNOWN" and v != pred4(*k)]
    still_pred = sorted({pred4(*k) for k in map(tuple, still)})
    return {
        "base_loops_found": len(base), "base_missing": base_missing,
        "lifts_verified": lifted_ok, "lift_failures": lifted_bad,
        "partC": partC, "partC_inconsistent_with_divisibility": cons, "nondivisible_all_evidence_terminating": nondiv_clean,
        "unknowns_resolved_as_looping": resolved, "unknowns_remaining": still,
        "H-C03-4_contradictions_on_625": contra4, "H-C03-4_prediction_for_remaining_unknowns": still_pred,
        "summary": [
            f"base family (1,q,r,k), q<=5, q<r<2q, k<=6: {len(base)} loops found, missing: {base_missing}",
            f"lifted loops verified (p=2..4, both orientations): {lifted_ok}, failures: {len(lifted_bad)}",
            f"part C: {len(partC)} rules; divisibility predicts loop-finding exactly: {len(cons) == 0} "
            f"(mismatches {cons[:4]}); all non-multiples terminate from every tested start: {nondiv_clean}",
            f"EXP-C03-02 unknowns resolved as looping: {len(resolved)}; remaining {len(still)}: {still}",
            f"H-C03-4 contradictions on the 625 rules: {len(contra4)}; prediction for remaining unknowns: {still_pred}",
        ],
    }
