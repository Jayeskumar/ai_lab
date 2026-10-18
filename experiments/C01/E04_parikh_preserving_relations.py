"""EXP-C01-04: do single counting-preserving relations generate full counting equivalence?"""

from systems.rewriting import length_preserving_classes, parikh, words

META = {
    "id": "EXP-C01-04",
    "cycle": "C01",
    "title": "Single Parikh-preserving relations versus the Parikh (counting) equivalence",
    "agent": "Mathematical Inventor",
    "question": "If a relation u <-> v only rearranges symbols, does it eventually identify all words with the "
                "same symbol counts (on long enough words)?",
    "hypothesis": "H-C01-4 (inventor's conjecture, deliberately bold): for every relation u <-> v over {a,b} "
                  "with u != v and equal symbol counts, the generated congruence coincides with Parikh "
                  "equivalence on all words of length >= |u|.",
    "assumptions": ["System A over {a,b}", "relations of length 3 and 4", "words of length <= 11"],
    "methodology": "For each relation (up to swapping sides) compute exact congruence classes of each length "
                   "(length-preserving, so exact), and compare their number and content with Parikh classes.",
    "falsification": "A word of length >= |u| whose class is strictly smaller than its Parikh class.",
}


def run():
    rows = []
    for length in (3, 4):
        ws = list(words("ab", length))
        rels = [(u, v) for u in ws for v in ws if u < v and parikh(u, "ab") == parikh(v, "ab")]
        for u, v in rels:
            counts, cex = [], None
            for L in range(1, 12):
                classes = length_preserving_classes([(u, v)], "ab", L)
                counts.append(len(classes))
                if cex is None and L >= length:
                    for c in classes:
                        w = min(c)
                        full = {x for x in words("ab", L) if parikh(x, "ab") == parikh(w, "ab")}
                        if set(c) != full:
                            cex = {"word": w, "class": sorted(c), "parikh_class_size": len(full)}
                            break
            rows.append({"relation": [u, v], "class_counts_len_1_to_11": counts,
                         "parikh_counts_len_1_to_11": [L + 1 for L in range(1, 12)],
                         "first_counterexample": cex})
    refuted = [r for r in rows if r["first_counterexample"] is not None]
    return {
        "relations_tested": len(rows),
        "rows": rows,
        "refuting_relations": len(refuted),
        "summary": [
            f"{len(rows)} Parikh-preserving relations of length 3-4 tested on words up to length 11",
            f"{len(refuted)} of them give a word whose class is smaller than its Parikh class "
            f"(e.g. {rows[0]['relation']}: {rows[0]['first_counterexample']})",
        ],
    }
