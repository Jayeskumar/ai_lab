"""EXP-C01-05: counting congruence classes modulo one length-preserving relation."""

import itertools

from lab.seqtools import guess_recurrence, series_coefficients
from systems.rewriting import knuth_bendix, length_preserving_classes, words

META = {
    "id": "EXP-C01-05",
    "cycle": "C01",
    "title": "Class counts modulo one relation u <-> v: the unbordered-side theorem and its exceptions",
    "agent": "Mathematical Explorer",
    "question": "Why do all length-3 relations give F(n+3)-1 classes and most length-4 relations give "
                "partial sums of tribonacci numbers? Which relations are exceptions?",
    "hypothesis": "H-C01-5: if |u| = |v| = k, u != v and u is unbordered (no proper prefix equals a suffix), "
                  "then the number of classes of length-n words over a q-letter alphabet equals [x^n] "
                  "1/(1 - q x + x^k), i.e. the number of length-n words avoiding u.",
    "assumptions": ["System A", "alphabets of size 2 (k = 2..5, n <= 12) and 3 (k = 2..3, n <= 7)",
                    "exact classes (relations preserve length)"],
    "methodology": "Exhaustive over all unordered pairs {u, v} of distinct words of length k. Exact class "
                   "counts by union-find; compare with the series coefficients; for relations whose sides are "
                   "both bordered, record counts, the minimal linear recurrence fitted to them, and whether "
                   "shortlex completion terminates.",
    "falsification": "Any relation with an unbordered side whose class counts differ from the series.",
}

CASES = [("ab", 2, 12), ("ab", 3, 12), ("ab", 4, 12), ("ab", 5, 12), ("abc", 2, 7), ("abc", 3, 7)]


def bordered(w):
    return any(w[:i] == w[-i:] for i in range(1, len(w)))


def run():
    rows, failures = [], []
    for alphabet, k, N in CASES:
        q = len(alphabet)
        generic = series_coefficients([1], [1, -q] + [0] * (k - 2) + [1], N + 1)[1:]
        ws = list(words(alphabet, k))
        for u, v in itertools.combinations(ws, 2):
            counts = [len(length_preserving_classes([(u, v)], alphabet, n)) for n in range(1, N + 1)]
            ub = (not bordered(u)) or (not bordered(v))
            row = {"alphabet": alphabet, "k": k, "relation": [u, v], "unbordered_side": ub,
                   "counts": counts, "matches_generic": counts == generic}
            if ub and counts != generic:
                failures.append(row)
            if not ub:
                rec = guess_recurrence(counts)
                row["fitted_recurrence"] = [str(c) for c in rec[0]] if rec else None
                rules, complete = knuth_bendix([(u, v)], alphabet, max_rules=60, max_steps=4000)
                row["shortlex_completion"] = {"complete": complete, "n_rules": len(rules),
                                              "rules": rules[:8]}
            rows.append(row)
    both_bordered = [r for r in rows if not r["unbordered_side"]]
    exceptions = [r for r in both_bordered if not r["matches_generic"]]
    return {
        "cases": [list(c) for c in CASES],
        "n_relations": len(rows),
        "n_with_unbordered_side": sum(r["unbordered_side"] for r in rows),
        "theorem_failures": failures,
        "both_bordered": both_bordered,
        "both_bordered_matching_generic": [r["relation"] for r in both_bordered if r["matches_generic"]],
        "exceptions": [{"alphabet": r["alphabet"], "relation": r["relation"], "counts": r["counts"],
                        "fitted_recurrence": r.get("fitted_recurrence")} for r in exceptions],
        "summary": [
            f"{len(rows)} relations tested; {sum(r['unbordered_side'] for r in rows)} have an unbordered side; "
            f"failures of H-C01-5: {len(failures)}",
            f"{len(both_bordered)} relations have both sides bordered; {len(exceptions)} of them deviate from "
            f"the generic count 1/(1-qx+x^k)",
        ],
    }
