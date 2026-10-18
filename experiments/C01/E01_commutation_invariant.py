"""EXP-C01-01: the complete invariant of the commutation congruence."""

from math import comb

from systems.rewriting import (knuth_bendix, length_preserving_classes, normal_form, parikh, words)

META = {
    "id": "EXP-C01-01",
    "cycle": "C01",
    "title": "Commutation congruence: classes, complete invariant and normal forms",
    "agent": "Mathematical Explorer",
    "question": "In System A with the swap relations xy <-> yx, what distinguishes two words that "
                "cannot be transformed into each other?",
    "hypothesis": "Two words are congruent iff, for every symbol s, deleting all other symbols gives the "
                  "same word s...s (equal symbol projections). The shortlex-completed system {yx -> xy : "
                  "x < y} is finite and its normal forms are the sorted words.",
    "assumptions": ["System A axioms A1-A3", "alphabet sizes 2-4", "words of bounded length (exact, since "
                    "the relations preserve length)"],
    "methodology": "For every alphabet/length slice, compute the exact congruence classes by union-find over "
                   "single swap steps; compare the partition with the projection partition; run shortlex "
                   "Knuth-Bendix completion and compare normal forms with sorted words.",
    "falsification": "Any slice where a class contains two words with different projections, or two words "
                     "with equal projections lie in different classes, or completion fails/normal form differs.",
}

SLICES = {"ab": 10, "abc": 7, "abcd": 5}


def run():
    out = {"slices": [], "summary": []}
    all_ok = True
    for alphabet, max_len in SLICES.items():
        rels = [(x + y, y + x) for x in alphabet for y in alphabet if x < y]
        rules, complete = knuth_bendix(rels, alphabet)
        for L in range(0, max_len + 1):
            classes = length_preserving_classes(rels, alphabet, L)
            proj = {}
            for w in words(alphabet, L):
                proj.setdefault(parikh(w, alphabet), set()).add(w)
            class_sets = sorted(sorted(c) for c in classes)
            proj_sets = sorted(sorted(c) for c in proj.values())
            same_partition = class_sets == proj_sets
            nf_sorted = all(normal_form(w, rules) == "".join(sorted(w)) for w in words(alphabet, L))
            predicted = comb(L + len(alphabet) - 1, len(alphabet) - 1)
            ok = same_partition and nf_sorted and len(classes) == predicted
            all_ok &= ok
            out["slices"].append({"alphabet": alphabet, "length": L, "words": len(alphabet) ** L,
                                  "classes": len(classes), "predicted_classes": predicted,
                                  "partition_equals_projection_partition": same_partition,
                                  "normal_forms_are_sorted_words": nf_sorted})
        out.setdefault("completions", {})[alphabet] = {"rules": rules, "complete": complete}
        all_ok &= complete and sorted(rules) == sorted((y + x, x + y) for x in alphabet for y in alphabet if x < y)
    out["all_checks_passed"] = all_ok
    n = len(out["slices"])
    out["summary"] = [
        f"{n} alphabet/length slices checked exactly (up to {sum(len(a) ** L for a, L in SLICES.items())} words "
        f"in the largest slices); all checks passed: {all_ok}",
        "completion of the swap relations is finite: {yx -> xy | x<y}; normal forms = sorted words",
    ]
    return out
