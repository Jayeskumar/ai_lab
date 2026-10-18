"""EXP-C01-07: computer-assisted proofs of the common-border formula, one relation at a time."""

import itertools

from systems.automata import avoid_dfa, count_accepted
from systems.rewriting import (critical_pairs, knuth_bendix, length_preserving_classes, normal_form,
                               shortlex_key, words)

from experiments.C01.E06_common_border_conjecture import borders, predicted

META = {
    "id": "EXP-C01-07",
    "cycle": "C01",
    "title": "Automatic proofs of the common-border class-count formula via finite completion",
    "agent": "Formal Verifier",
    "question": "For which relations u <-> v can H-C01-7 be proved for ALL lengths n by a finite certificate?",
    "hypothesis": "For most small relations some shortlex order (alphabet permutation, read left-to-right "
                  "or right-to-left) yields a finite convergent completion; its irreducible words then give a "
                  "rational count sequence that can be compared with the formula exactly.",
    "assumptions": ["Newman's lemma and the critical-pair lemma for string rewriting",
                    "Cayley-Hamilton bound on the order of DFA count recurrences"],
    "methodology": "For each relation and each of 2*q! shortlex orders: run bounded Knuth-Bendix; on success, "
                   "independently re-verify convergence (rules decreasing, all critical pairs joinable, u and v "
                   "have equal normal forms); build the Aho-Corasick DFA of the left-hand sides (s live "
                   "states); compare s + k + 5 count terms with the formula (sufficient for equality of all "
                   "terms); cross-check against brute-force class counts for n <= 8.",
    "falsification": "A verified convergent completion whose irreducible-word counts differ from the formula "
                     "would refute H-C01-7 for that relation.",
}

CASES = [("ab", 2, False), ("ab", 3, False), ("ab", 4, False), ("ab", 5, False), ("ab", 6, True),
         ("abc", 2, False), ("abc", 3, False), ("abc", 4, True)]


def verify_convergent(rules, order, u, v):
    key = lambda w: shortlex_key(w, order)
    if any(not key(l) > key(r) for l, r in rules):
        return False, "rule not decreasing"
    if any(len(l) != len(r) for l, r in rules):
        return False, "rule not length-preserving"
    for r1 in rules:
        for r2 in rules:
            for a, b in critical_pairs(r1, r2):
                if normal_form(a, rules) != normal_form(b, rules):
                    return False, f"critical pair not joinable: {a} / {b}"
    if normal_form(u, rules) != normal_form(v, rules):
        return False, "u and v have different normal forms"
    return True, "ok"


def try_prove(u, v, alphabet):
    q, k = len(alphabet), len(u)
    for perm in itertools.permutations(alphabet):
        order = "".join(perm)
        for direction in ("ltr", "rtl"):
            uu, vv = (u, v) if direction == "ltr" else (u[::-1], v[::-1])
            rules, complete = knuth_bendix([(uu, vv)], order, max_rules=120, max_steps=6000, max_word=4 * k)
            if not complete:
                continue
            ok, why = verify_convergent(rules, order, uu, vv)
            if not ok:
                return {"status": "BUG", "why": why, "order": order, "direction": direction}
            delta, start, s = avoid_dfa([l for l, _ in rules], alphabet)
            N = s + k + 5
            counts = count_accepted(delta, start, N)[1:]
            pred, common = predicted(u, v, q, N)
            brute = [len(length_preserving_classes([(u, v)], alphabet, n)) for n in range(1, 9)]
            return {"status": "PROVEN" if counts == pred else "REFUTED", "order": order, "direction": direction,
                    "n_rules": len(rules), "dfa_states": s, "terms_compared": N,
                    "brute_force_agrees": brute == counts[:8], "rules": rules if len(rules) <= 6 else rules[:6]}
    return {"status": "NO FINITE COMPLETION FOUND"}


def run():
    per_case, open_cases, bugs, refuted = {}, [], [], []
    for alphabet, k, hard_only in CASES:
        tally = {}
        for u, v in itertools.combinations(list(words(alphabet, k)), 2):
            bu, bv = borders(u), borders(v)
            hard = not (bu <= bv or bv <= bu)
            if hard_only and not hard:
                continue
            res = try_prove(u, v, alphabet)
            st = res["status"]
            label = ("hard " if hard else "containment ") + st
            tally[label] = tally.get(label, 0) + 1
            if st == "BUG":
                bugs.append({"relation": [u, v], **res})
            elif st == "REFUTED":
                refuted.append({"relation": [u, v], **res})
            elif st != "PROVEN":
                open_cases.append({"alphabet": alphabet, "relation": [u, v], "hard": hard})
            elif not res["brute_force_agrees"]:
                bugs.append({"relation": [u, v], "why": "brute force disagrees", **res})
        per_case[f"{alphabet}/k={k}{'/hard-only' if hard_only else ''}"] = tally
    n_proven = sum(v for t in per_case.values() for lab, v in t.items() if lab.endswith("PROVEN"))
    n_total = sum(v for t in per_case.values() for v in t.values())
    return {
        "per_case": per_case,
        "open_relations": open_cases,
        "n_open": len(open_cases),
        "refuted": refuted,
        "bugs": bugs,
        "summary": [
            f"{n_total} relations attempted; {n_proven} proved for all n by verified finite completion; "
            f"{len(open_cases)} without a finite completion (formula still only checked for n <= 12/7); "
            f"refutations: {len(refuted)}; internal inconsistencies: {len(bugs)}",
            f"per case: {per_case}",
        ],
    }
