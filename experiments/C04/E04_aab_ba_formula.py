"""EXP-C04-04: derivational complexity of aab -> ba is n - Theta(log n) (non-rational)."""

from systems.derivations import derivation_graph, graph_values
from systems.rewriting import normal_form, words

META = {
    "id": "EXP-C04-04",
    "cycle": "C04",
    "title": "The rule aab -> ba is a truncated binary exchange system: D(n) = max_m (n-m) - ceil((n-m)/2^m)",
    "agent": "Mathematical Explorer",
    "question": "Why does the derivational complexity of aab -> ba admit no linear recurrence?",
    "hypothesis": "H-C04-L: writing w = a^x0 b a^x1 ... b a^xm, each step is the carry 2[k] -> [k+1] (k < m) with "
                  "level m a sink; hence D(n) = max over m of (n - m) - ceil((n - m)/2^m), i.e. "
                  "n - D(n) = min_m (m + ceil((n-m)/2^m)) = log2(n) + O(1). Predicted first terms where D stalls: "
                  "n = 4, 7, 12, 21, 38, ...",
    "assumptions": ["random descent of aab -> ba (unbordered left-hand side, CLM-C04-05)",
                    "exhaustive derivation graphs up to n = 17 (EXP-C04-03)"],
    "methodology": "(1) Exhaustive derivation graphs for n <= 14 (independent of the reduction). (2) For n <= 21, "
                   "one leftmost derivation per word (valid by random descent) over all 2^n words. (3) Per-word "
                   "check of the configuration formula D(w) = T - s2(V mod 2^m) - floor(V/2^m).",
    "falsification": "Any n <= 21 where the maximum over words differs from the formula, or any word whose "
                     "derivation length differs from the configuration formula.",
}

RULE = ("aab", "ba")


def formula_D(n):
    best = 0
    for m in range(0, n + 1):
        T = n - m
        if T > 0:
            best = max(best, T - (-(-T // (2 ** m))))
        if 2 ** m >= T:      # from here on the value is T - 1, which decreases with m
            break
    return best


def kappa(n):
    k = 0
    while 2 ** k + k < n:
        k += 1
    return k


def config_length(w):
    runs = w.split("b")
    m = len(runs) - 1
    T = sum(len(x) for x in runs)
    V = sum(len(x) << k for k, x in enumerate(runs))
    return T - bin(V % (1 << m)).count("1") - (V >> m)


def leftmost_length(w):
    steps = 0
    while True:
        i = w.find("aab")
        if i < 0:
            return steps
        w = w[:i] + "ba" + w[i + 3:]
        steps += 1


def run():
    graph_mismatch = []
    starts = [w for L in range(0, 15) for w in words("ab", L)]
    vals = graph_values(derivation_graph(starts, RULE, limit=2_000_000))
    for w in starts:
        if not (vals[w][0] == vals[w][1] == config_length(w)):
            graph_mismatch.append(w)
    sim, word_mismatch = [], 0
    for n in range(0, 22):
        best = 0
        for w in words("ab", n):
            d = leftmost_length(w)
            if d != config_length(w):
                word_mismatch += 1
            best = max(best, d)
        sim.append(best)
    pred = [formula_D(n) for n in range(0, 22)]
    stalls = [n for n in range(1, 60) if formula_D(n) == formula_D(n - 1) and n >= 3]
    closed_form_ok = all(formula_D(n) == n - 1 - kappa(n) for n in range(1, 20001))
    stalls_closed = all((formula_D(n) == formula_D(n - 1)) == any(n == 2 ** k + k + 1 for k in range(1, 20))
                        for n in range(3, 20001))
    return {
        "D_simulated_n0_21": sim,
        "D_formula_n0_21": pred,
        "agree": sim == pred,
        "graph_vs_configuration_mismatches": len(graph_mismatch),
        "simulation_vs_configuration_mismatches": word_mismatch,
        "predicted_stalls_up_to_59": stalls,
        "closed_form_n_minus_1_minus_kappa_ok_n_le_20000": closed_form_ok,
        "stalls_exactly_at_2k_plus_k_plus_1_n_le_20000": stalls_closed,
        "n_minus_D_formula_up_to_64": [n - formula_D(n) for n in range(65)],
        "summary": [
            f"max derivation length over all 2^n words, n <= 21: {sim}",
            f"formula agrees for all n <= 21: {sim == pred}; per-word configuration formula mismatches: "
            f"graph (n <= 14) {len(graph_mismatch)}, simulation (n <= 21) {word_mismatch}",
            f"n where D(n) = D(n-1) (n >= 3, n < 60): {stalls}",
            f"closed form D(n) = n - 1 - min{{k : 2^k + k >= n}} (n <= 20000): {closed_form_ok}; stalls exactly at "
            f"n = 2^k + k + 1: {stalls_closed}",
        ],
    }
