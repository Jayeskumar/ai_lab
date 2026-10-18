"""EXP-C04-05: which one-rule systems have random descent?"""

from collections import Counter, deque

from systems.derivations import (GraphLimit, all_rules, borders, classify_termination, critical_peaks,
                                 derivation_graph, equal_length_joinable, graph_values)
from systems.rewriting import words

META = {
    "id": "EXP-C04-05",
    "cycle": "C04",
    "title": "Random descent of one-rule systems: unbordered left-hand sides versus critical peaks",
    "agent": "Mathematical Inventor",
    "question": "When do all maximal derivations from every word have the same length (random descent)?",
    "hypothesis": "H-C04-1 (bold): a terminating one-rule system has random descent iff its left-hand side is "
                  "unbordered. H-C04-2: a terminating one-rule system has random descent iff each of its critical "
                  "peaks (r s <- p b s -> p r for l = p b = b s) is joinable by two derivations of EQUAL length.",
    "assumptions": ["the 162 terminating rules of EXP-C04-01", "all words of length <= 11 (<= 8 for the four "
                    "doubling rules)"],
    "methodology": "Exact min/max derivation lengths and the set of reachable normal forms per word from the "
                   "derivation graph; random descent = all maximal derivations from each word have the same length "
                   "AND the same normal form (van Oostrom); critical peaks joined by breadth-first search over exact "
                   "step counts.",
    "falsification": "H-C04-1: a bordered rule with random descent or an unbordered one without. H-C04-2: "
                     "disagreement between observed random descent and the critical-peak test.",
}


def normal_form_counts(succ):
    """Number of distinct normal forms reachable from each word (acyclic graph)."""
    pred = {w: [] for w in succ}
    rem = {}
    for w, s in succ.items():
        rem[w] = len(s)
        for x in s:
            pred[x].append(w)
    ready = deque(w for w, k in rem.items() if k == 0)
    nfs = {}
    while ready:
        w = ready.popleft()
        nfs[w] = frozenset([w]) if not succ[w] else frozenset().union(*(nfs[x] for x in succ[w]))
        for p in pred[w]:
            rem[p] -= 1
            if rem[p] == 0:
                ready.append(p)
    return {w: len(v) for w, v in nfs.items()}


def run():
    term = [r for r in all_rules() if classify_termination(r)["status"] == "TERMINATING"]
    rows = []
    for rule in term:
        N = 11
        while True:
            starts = [w for L in range(0, N + 1) for w in words("ab", L)]
            try:
                succ = derivation_graph(starts, rule, limit=400_000)
                break
            except GraphLimit:
                N -= 1
        vals = graph_values(succ)
        nfc = normal_form_counts(succ)
        rd_fail = [w for w in starts if vals[w][0] != vals[w][1]]
        conf_fail = [w for w in starts if nfc[w] != 1]
        peaks = critical_peaks(rule)
        joins = [equal_length_joinable(p["left"], p["right"], rule) for p in peaks]
        rows.append({
            "rule": list(rule), "N": N, "bordered": bool(borders(rule[0])),
            "length_uniform": not rd_fail, "first_non_uniform_word": rd_fail[0] if rd_fail else None,
            "confluent": not conf_fail, "first_non_confluent": conf_fail[0] if conf_fail else None,
            "random_descent": (not rd_fail) and (not conf_fail),
            "critical_peaks": [{**p, "equal_length_join_k": k} for p, k in zip(peaks, joins)],
            "local_rd": all(k is not None for k in joins),
        })
    h1_bad = [r for r in rows if r["random_descent"] != (not r["bordered"])]
    h2_bad = [r for r in rows if r["random_descent"] != r["local_rd"]]
    rd_not_conf = [r for r in rows if r["length_uniform"] and not r["confluent"]]
    table = Counter((r["bordered"], r["random_descent"], r["confluent"]) for r in rows)
    return {
        "rows": rows,
        "table_bordered_rd_confluent": {f"bordered={a},RD={b},confluent={c}": n for (a, b, c), n in table.items()},
        "h1_counterexamples": [{"rule": r["rule"], "bordered": r["bordered"], "random_descent": r["random_descent"]}
                               for r in h1_bad],
        "h2_disagreements": [r["rule"] for r in h2_bad],
        "length_uniform_but_not_confluent": [r["rule"] for r in rd_not_conf],
        "summary": [
            f"{len(rows)} terminating rules; (bordered, RD, confluent) counts: "
            f"{ {f'{a}/{b}/{c}': n for (a, b, c), n in sorted(table.items())} }",
            f"H-C04-1 counterexamples: {len(h1_bad)} (e.g. {[r['rule'] for r in h1_bad[:4]]}); unbordered rules "
            f"without RD: {sum(1 for r in rows if not r['bordered'] and not r['random_descent'])}",
            f"H-C04-2 disagreements (RD vs equal-length joinable critical peaks): {len(h2_bad)}; length-uniform "
            f"but not confluent: {len(rd_not_conf)}",
        ],
    }
