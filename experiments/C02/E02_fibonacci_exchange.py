"""EXP-C02-02: the Fibonacci exchange system and the Zeckendorf representation."""

import itertools

from systems.exchange import FIBONACCI_RULES, explore, fib_weights, trim, value, zeckendorf_config

META = {
    "id": "EXP-C02-02",
    "cycle": "C02",
    "title": "Fibonacci exchange rules: termination, confluence and derivation lengths",
    "agent": "Mathematical Explorer",
    "question": "With exchanges [k]+[k+1] -> [k+2], 2[k] -> [k+1]+[k-2] (and boundary versions), do all "
                "orders of exchange reach the Zeckendorf representation, and how long do they take?",
    "hypothesis": "H-C02-F: from every configuration the system terminates and reaches a unique normal form, "
                  "the Zeckendorf representation of its value (weights 1,2,3,5,8,...); unlike the binary rule, "
                  "derivation lengths depend on the order of exchanges.",
    "assumptions": ["weights w_k = F(k+2)", "unary starts n <= 40; all configurations of value <= 26"],
    "methodology": "Exhaustive derivation graphs (cycle detection, sinks, min/max lengths) from unary starts "
                   "and from every configuration of small value.",
    "falsification": "A cycle, two sinks, or a sink different from the greedy Zeckendorf representation.",
}


def configs_of_value(v, w):
    """All configurations (count vectors) with weighted value exactly v."""
    out = []

    def rec(k, rem, cur):
        if k < 0:
            if rem == 0:
                out.append(trim(cur))
            return
        for x in range(rem // w[k] + 1):
            cur[k] = x
            rec(k - 1, rem - x * w[k], cur)
        cur[k] = 0

    L = max(i for i in range(len(w)) if w[i] <= max(v, 1)) + 1
    rec(L - 1, v, [0] * L)
    return out


def run():
    w = fib_weights(40)
    unary, bad = [], []
    for n in range(0, 41):
        r = explore((n,), FIBONACCI_RULES)
        ok = not r["has_cycle"] and r["sinks"] == [zeckendorf_config(n)]
        unary.append({"n": n, "states": r["states"], "min_len": r.get("min_len"), "max_len": r.get("max_len"),
                      "ok": ok})
        if not ok:
            bad.append(n)
    general_checked, general_bad = 0, []
    for v in range(0, 27):
        for c in configs_of_value(v, w):
            r = explore(c, FIBONACCI_RULES)
            general_checked += 1
            if r["has_cycle"] or r["sinks"] != [zeckendorf_config(v)] or value(c, w) != v:
                general_bad.append({"start": c, "sinks": r["sinks"]})
    return {
        "unary": unary,
        "min_len_seq": [u["min_len"] for u in unary],
        "max_len_seq": [u["max_len"] for u in unary],
        "unary_failures": bad,
        "general_configurations_checked": general_checked,
        "general_failures": general_bad[:10],
        "summary": [
            f"unary starts n <= 40: {len(bad)} failures (unique normal form = Zeckendorf, no cycles)",
            f"all {general_checked} configurations of value <= 26: {len(general_bad)} failures",
            f"min derivation lengths n=0..15: {[u['min_len'] for u in unary[:16]]}",
            f"max derivation lengths n=0..15: {[u['max_len'] for u in unary[:16]]}",
        ],
    }
