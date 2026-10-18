"""EXP-C02-01: integer bases emerge as normal forms of the exchange rule b[k] -> [k+1]."""

from systems.exchange import explore, stabilize_carry, trim

META = {
    "id": "EXP-C02-01",
    "cycle": "C02",
    "title": "Integer bases as normal forms of the exchange rule b tokens -> 1 token one level up",
    "agent": "Mathematical Explorer",
    "question": "Starting from n tokens at level 0 (a unary numeral), what does the exchange rule "
                "b[k] -> [k+1] produce, and does the order of exchanges matter?",
    "hypothesis": "Every derivation terminates in the same configuration, namely the base-b digits of n, "
                  "after exactly (n - s_b(n))/(b - 1) exchanges, s_b the base-b digit sum.",
    "assumptions": ["configurations = multisets of levels (C01)", "b = 2..5"],
    "methodology": "Exhaustive derivation graphs from n tokens (all orders of exchange) for small n; fast "
                   "stabilisation compared with base-b digits for n <= 20000.",
    "falsification": "Two different normal forms, unequal derivation lengths, a cycle, or a mismatch with "
                     "base-b digits.",
}


def base_digits(n, b):
    out = []
    while n:
        out.append(n % b)
        n //= b
    return tuple(out)


def run():
    exhaustive, fast_fail = [], []
    for b, nmax in ((2, 40), (3, 30), (4, 30), (5, 30)):
        rule = [(0, None, {0: b}, {1: 1})]
        for n in range(0, nmax + 1):
            r = explore((n,), rule)
            ok = (not r["has_cycle"] and len(r["sinks"]) == 1 and r["sinks"][0] == trim(base_digits(n, b))
                  and r["min_len"] == r["max_len"] == (n - sum(base_digits(n, b))) // (b - 1))
            exhaustive.append({"b": b, "n": n, "states": r["states"], "ok": ok})
        for n in range(0, 20001):
            c, f, t = stabilize_carry((n,), b, (1,))
            if not t or c != trim(base_digits(n, b)):
                fast_fail.append((b, n))
    bad = [e for e in exhaustive if not e["ok"]]
    return {
        "exhaustive_cases": len(exhaustive),
        "exhaustive_failures": bad,
        "largest_state_space": max(e["states"] for e in exhaustive),
        "fast_failures": fast_fail[:10],
        "summary": [
            f"{len(exhaustive)} exhaustive derivation graphs (b = 2..5): {len(bad)} failures; largest graph "
            f"{max(e['states'] for e in exhaustive)} configurations",
            f"fast stabilisation vs base-b digits for n <= 20000, b = 2..5: {len(fast_fail)} mismatches",
        ],
    }
