"""EXP-C01-08: in-lab replication of the Historian's computations (review of C01, 2026-10-18)."""

import itertools
import json

from lab.paths import RESULTS
from systems.rewriting import critical_pairs, length_preserving_classes, normal_form, words

from experiments.C01.E06_common_border_conjecture import borders, predicted

META = {
    "id": "EXP-C01-08",
    "cycle": "C01",
    "title": "Replication of the novelty audit's computations: confluence criterion, open cases, two common borders",
    "agent": "Mathematical Skeptic",
    "question": "Do the Historian's scratch computations (run outside the repository) reproduce inside the lab?",
    "hypothesis": "(a) {u -> v} (|u| = |v|) is confluent iff Borders(u) is contained in Borders(v) (Kurth 1987); "
                  "(b) all 527 relations left open by EXP-C01-07 have no common border; among the hard relations "
                  "of EXP-C01-06 exactly 12 have a common border (one each); (c) the common-border formula holds for "
                  "hard relations with two common borders (k = 8).",
    "assumptions": ["(a) binary k <= 7, ternary k <= 4, all ordered pairs", "(c) n <= 13"],
    "methodology": "(a) local confluence = all critical pairs of the single terminating rule join; (b) recompute "
                   "common borders for the relations of EXP-C01-06/07; (c) exact class counts by union-find.",
    "falsification": "Any mismatch in (a), any open relation with c != 1, a different count in (b), or a failure "
                     "of the formula in (c).",
}


def confluent(u, v):
    rules = [(u, v)]
    return all(normal_form(a, rules) == normal_form(b, rules) for a, b in critical_pairs((u, v), (u, v)))


def run():
    # (a) confluence criterion
    mism, total = [], 0
    for alphabet, kmax in (("ab", 7), ("abc", 4)):
        for k in range(1, kmax + 1):
            ws = list(words(alphabet, k))
            for u in ws:
                bu = borders(u)
                for v in ws:
                    if u == v:
                        continue
                    total += 1
                    if confluent(u, v) != (bu <= borders(v)):
                        mism.append([u, v])
    # (b) open relations of EXP-C01-07 and hard relations of EXP-C01-06's ranges
    open_rel = json.load(open(RESULTS / "EXP-C01-07.json"))["results"]["open_relations"]
    open_c = {}
    for o in open_rel:
        u, v = o["relation"]
        n_common = len(borders(u) & borders(v))
        open_c[n_common] = open_c.get(n_common, 0) + 1
    hard_by_common, hard_common_list = {}, []
    for alphabet, k in [("ab", kk) for kk in range(2, 7)] + [("abc", kk) for kk in range(2, 5)]:
        for u, v in itertools.combinations(list(words(alphabet, k)), 2):
            bu, bv = borders(u), borders(v)
            if bu <= bv or bv <= bu:
                continue
            c = len(bu & bv)
            hard_by_common[c] = hard_by_common.get(c, 0) + 1
            if c:
                hard_common_list.append([u, v])
    # (c) two common borders at k = 8
    tests = [("aaaaaaaa", "aabaabaa"), ("aaaabaaa", "aabaabaa"), ("aaabaaaa", "aabaabaa")]
    two_border = []
    for u, v in tests:
        N = 13
        counts = [len(length_preserving_classes([(u, v)], "ab", n)) for n in range(1, N + 1)]
        pred, common = predicted(u, v, 2, N)
        two_border.append({"relation": [u, v], "common_borders": common, "agree_n_le_13": counts == pred,
                           "counts": counts})
    return {
        "a_pairs_checked": total,
        "a_mismatches": mism[:10],
        "a_n_mismatches": len(mism),
        "b_open_relations_by_number_of_common_borders": {str(k): v for k, v in open_c.items()},
        "b_hard_relations_by_number_of_common_borders": {str(k): v for k, v in hard_by_common.items()},
        "b_hard_relations_with_common_border": hard_common_list,
        "c_two_common_borders": two_border,
        "summary": [
            f"(a) {total} ordered pairs: confluence iff border containment, mismatches {len(mism)}",
            f"(b) open relations by #common borders: {open_c}; hard relations by #common borders: {hard_by_common}",
            f"(c) two-common-border relations (k = 8, n <= 13): agree = {[t['agree_n_le_13'] for t in two_border]}",
        ],
    }
