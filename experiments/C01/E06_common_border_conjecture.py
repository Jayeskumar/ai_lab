"""EXP-C01-06: the common-border formula for class counts modulo one relation."""

import itertools

from lab.seqtools import series_coefficients
from systems.rewriting import length_preserving_classes, words

META = {
    "id": "EXP-C01-06",
    "cycle": "C01",
    "title": "Common-border formula for one-relation class counts (test on old and new cases)",
    "agent": "Mathematical Explorer",
    "question": "Is the number of classes of length-n words modulo u <-> v determined by the common borders "
                "of u and v?",
    "hypothesis": "H-C01-7: with k = |u| = |v|, q = alphabet size and c(x) = 1 + sum over words b that are "
                  "borders of both u and v of x^(k-|b|), the class counts are the coefficients of "
                  "c(x) / (x^k + (1 - q x) c(x)) (= the number of length-n words avoiding any single word "
                  "whose autocorrelation is c).",
    "assumptions": ["System A; length-preserving single relations u != v",
                    "binary k = 2..6 (n <= 12, k = 6 restricted to 'hard' pairs), ternary k = 2..4 "
                    "(n <= 7, k = 4 restricted to hard pairs)"],
    "methodology": "Exact class counts by union-find. 'Hard' pairs are those where neither border set "
                   "contains the other (the case not covered by the proved containment theorem); for k <= 5 "
                   "binary and k <= 3 ternary all pairs are tested.",
    "falsification": "Any relation whose exact class counts differ from the formula.",
}


def borders(w):
    return {w[:i] for i in range(1, len(w)) if w[:i] == w[-i:]}


def predicted(u, v, q, N):
    k = len(u)
    common = borders(u) & borders(v)
    c = [0] * k
    c[0] = 1
    for b in common:
        c[k - len(b)] += 1
    den = [0] * (k + 1)
    for i, ci in enumerate(c):           # (1 - q x) c(x)
        den[i] += ci
        if i + 1 <= k:
            den[i + 1] -= q * ci
    den[k] += 1                           # + x^k
    return series_coefficients(c, den, N + 1)[1:], sorted(common, key=len)


CASES = [("ab", 2, 12, False), ("ab", 3, 12, False), ("ab", 4, 12, False), ("ab", 5, 12, False),
         ("ab", 6, 12, True), ("abc", 2, 7, False), ("abc", 3, 7, False), ("abc", 4, 7, True)]


def run():
    results, failures = [], []
    by_case = {}
    for alphabet, k, N, hard_only in CASES:
        q = len(alphabet)
        tested = hard = contained = 0
        for u, v in itertools.combinations(list(words(alphabet, k)), 2):
            bu, bv = borders(u), borders(v)
            is_hard = not (bu <= bv or bv <= bu)
            if hard_only and not is_hard:
                continue
            counts = [len(length_preserving_classes([(u, v)], alphabet, n)) for n in range(1, N + 1)]
            pred, common = predicted(u, v, q, N)
            tested += 1
            hard += is_hard
            contained += not is_hard
            ok = counts == pred
            if not ok:
                failures.append({"alphabet": alphabet, "relation": [u, v], "counts": counts, "predicted": pred,
                                 "common_borders": common})
            if is_hard:
                results.append({"alphabet": alphabet, "relation": [u, v], "common_borders": common,
                                "counts_head": counts[:N], "ok": ok})
        by_case[f"{alphabet}/k={k}/n<={N}{'/hard-only' if hard_only else ''}"] = {
            "tested": tested, "hard": hard, "border-containment": contained}
    return {
        "by_case": by_case,
        "hard_examples": results[:60],
        "n_hard_tested": len(results),
        "failures": failures[:30],
        "n_failures": len(failures),
        "summary": [
            f"relations tested per case: {by_case}",
            f"hard relations (neither border set contains the other): {len(results)}; failures of H-C01-7: "
            f"{len(failures)}",
        ],
    }
