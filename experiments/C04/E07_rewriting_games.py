"""EXP-C04-07: rewriting games - a move rewrites once, the player who cannot move loses."""

from collections import Counter

from systems.derivations import (GraphLimit, all_rules, classify_termination, derivation_graph, graph_values)
from systems.rewriting import words

from experiments.C04.E05_random_descent import normal_form_counts

META = {
    "id": "EXP-C04-07",
    "cycle": "C04",
    "title": "Rewriting games: parity for random-descent rules, run decomposition for unary left-hand sides",
    "agent": "Mathematical Explorer",
    "question": "What do the Sprague-Grundy values of rewriting games look like?",
    "hypothesis": "H-C04-4: for random-descent rules g(w) = D(w) mod 2 (D the unique derivation length), so "
                  "P-positions are exactly the words with even D (for ab -> ba: an even number of inversions). "
                  "H-C04-5: for a rule a^k -> u the game is the disjoint sum of a take-and-break game on the "
                  "maximal a-runs, g(w) = XOR over runs of G(run length). H-C04-6 (bold): every rewriting game "
                  "in the family has Grundy values <= 3 on words of length <= 10.",
    "assumptions": ["the 162 terminating rules", "all words of length <= 10 (<= 8 for the doubling rules)"],
    "methodology": "Grundy values by mex over the exact derivation graph. For unary left-hand sides the run game "
                   "G is computed independently from its definition (heap n, rewrite position i, resulting heaps "
                   "i + e_0, e_1, ..., n - k - i + e_t from the a-blocks e_j of u).",
    "falsification": "A random-descent word with g != D mod 2; a word whose Grundy value differs from the XOR of "
                     "run values; a Grundy value >= 4.",
}


def run_game_grundy(k, u, n_max):
    """Grundy values of the heap game induced by the rule a^k -> u on a single a-run."""
    blocks = u.split("b")
    G = [0] * (n_max + 1)
    for n in range(n_max + 1):
        opts = set()
        for i in range(0, n - k + 1):
            if len(blocks) == 1:                       # u = a^j: the run just changes length
                heaps = [n - k + len(u)]
            else:
                heaps = [i + len(blocks[0])] + [len(x) for x in blocks[1:-1]] + [n - k - i + len(blocks[-1])]
            x = 0
            for h in heaps:
                if h > n_max:
                    raise ValueError("heap grows beyond table")
                x ^= G[h]
            opts.add(x)
        g = 0
        while g in opts:
            g += 1
        G[n] = g
    return G


def run():
    term = [r for r in all_rules() if classify_termination(r)["status"] == "TERMINATING"]
    rows, parity_fail, decomposition_fail = [], [], []
    for rule in term:
        N = 10
        while True:
            starts = [w for L in range(0, N + 1) for w in words("ab", L)]
            try:
                succ = derivation_graph(starts, rule, limit=400_000)
                break
            except GraphLimit:
                N -= 1
        vals = graph_values(succ)
        nfc = normal_form_counts(succ)
        rd = all(vals[w][0] == vals[w][1] and nfc[w] == 1 for w in starts)
        gmax = max(vals[w][2] for w in starts)
        dist = Counter(vals[w][2] for w in starts)
        row = {"rule": list(rule), "N": N, "random_descent": rd, "max_grundy": gmax,
               "grundy_distribution": {str(g): c for g, c in sorted(dist.items())},
               "p_fraction": round(dist[0] / len(starts), 4)}
        if rd:
            bad = [w for w in starts if vals[w][2] != vals[w][0] % 2]
            if bad:
                parity_fail.append({"rule": list(rule), "word": bad[0]})
        l, u = rule
        for letter, other in (("a", "b"), ("b", "a")):
            if set(l) == {letter} and "".join(sorted(set(u))) in ("", other, letter, "ab"):
                uu = u.replace(letter, "a").replace(other, "b") if letter == "b" else u
                if letter == "b":
                    uu = u.translate(str.maketrans("ab", "ba"))
                try:
                    G = run_game_grundy(len(l), uu, 3 * N + 3)
                except ValueError:
                    break
                mism = 0
                for w in starts:
                    ww = w if letter == "a" else w.translate(str.maketrans("ab", "ba"))
                    x = 0
                    for run_ in ww.split("b"):
                        x ^= G[len(run_)]
                    if x != vals[w][2]:
                        mism += 1
                row["run_game_grundy_head"] = G[:16]
                row["decomposition_mismatches"] = mism
                if mism:
                    decomposition_fail.append(list(rule))
        rows.append(row)
    high = sorted(rows, key=lambda r: -r["max_grundy"])[:12]
    return {
        "rows": rows,
        "parity_failures": parity_fail,
        "decomposition_failures": decomposition_fail,
        "n_unary_rules_decomposed": sum(1 for r in rows if "decomposition_mismatches" in r),
        "max_grundy_overall": max(r["max_grundy"] for r in rows),
        "max_grundy_histogram": dict(Counter(r["max_grundy"] for r in rows)),
        "highest_grundy_rules": [{"rule": r["rule"], "max_grundy": r["max_grundy"], "rd": r["random_descent"]}
                                 for r in high],
        "summary": [
            f"{len(rows)} rewriting games; random-descent rules violating g = D mod 2: {len(parity_fail)}",
            f"unary-lhs rules checked against the run decomposition: "
            f"{sum(1 for r in rows if 'decomposition_mismatches' in r)}, failures: {len(decomposition_fail)}",
            f"histogram of max Grundy value per rule: {dict(sorted(Counter(r['max_grundy'] for r in rows).items()))}",
            f"highest: {[(r['rule'], r['max_grundy']) for r in high[:5]]}",
        ],
    }
