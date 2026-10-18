"""EXP-C08-03: deep associativity tests - large shifts, large inputs, non-monotone thresholds."""

import random

from systems.circle import BaseSequence, two_term

META = {
    "id": "EXP-C08-03",
    "cycle": "C08",
    "title": "Deep tests: shifts up to 20, inputs up to 1e6, Knuth's product up to 1e9",
    "agent": "Mathematical Skeptic",
    "question": "Do the associative shifts found on small inputs survive large inputs? Do slow Pisot systems "
                "become associative at larger shifts? Is the non-monotone threshold real?",
    "hypothesis": "Associative (G, s) pairs from EXP-C08-02 remain associative on large inputs; the three Pisot "
                  "sequences without an associative shift <= 8 become associative for some larger s.",
    "assumptions": ["exhaustive [1,14]^3 plus 4000 random triples in [1,1e6]^3 per (G, s); Knuth s=2: 20000 "
                    "random triples in [1,1e9]^3"],
    "methodology": "Same circle-product implementation; seeded random triples; record first counterexample.",
    "falsification": "A counterexample on large inputs for a pair previously considered associative.",
    "seed": 20261018,
}

CASES = [
    ("Fibonacci 1,2,3,5", two_term(1, 1, 2), range(0, 9)),
    ("1,3,4,7,11 (G1=3)", two_term(1, 1, 3), range(0, 9)),
    ("1,4,5,9,14 (G1=4)", two_term(1, 1, 4), range(0, 9)),
    ("2,2-recurrence 1,2,6,16", two_term(2, 2, 2), range(0, 11)),
    ("3,3-recurrence 1,5,18", two_term(3, 3, 5), range(6, 17)),
    ("G(k+1)=G(k)+G(k-2) 1,2,3", BaseSequence("G(k+1)=G(k)+G(k-2); 1,2,3", [1, 2, 3], (1, 0, 1)), range(6, 21)),
    ("G(k+1)=G(k)+G(k-3) 1,2,3,4", BaseSequence("G(k+1)=G(k)+G(k-3); 1,2,3,4", [1, 2, 3, 4], (1, 0, 0, 1)), range(8, 21)),
    ("4-bonacci 1,2,4,8", BaseSequence("4-bonacci", [1, 2, 4, 8], (1, 1, 1, 1)), range(6, 15)),
]


def first_failure(G, s, rng):
    for a in range(1, 15):
        for b in range(1, 15):
            ab = G.circle(a, b, s)
            for c in range(1, 15):
                if G.circle(ab, c, s) != G.circle(a, G.circle(b, c, s), s):
                    return (a, b, c)
    for _ in range(4000):
        a, b, c = (rng.randint(1, 10**6) for _ in range(3))
        if G.circle(G.circle(a, b, s), c, s) != G.circle(a, G.circle(b, c, s), s):
            return (a, b, c)
    return None


def run():
    rng = random.Random(META["seed"])
    rows = {}
    for name, G, shifts in CASES:
        rows[name] = {str(s): first_failure(G, s, rng) for s in shifts}
    F = two_term(1, 1, 2)
    knuth_bad = None
    for _ in range(20000):
        a, b, c = (rng.randint(1, 10**9) for _ in range(3))
        if F.circle(F.circle(a, b, 2), c, 2) != F.circle(a, F.circle(b, c, 2), 2):
            knuth_bad = (a, b, c)
            break
    summary = [f"Knuth's product (s=2), 20000 random triples up to 1e9: {'no failure' if knuth_bad is None else knuth_bad}"]
    for name, res in rows.items():
        good = [s for s, bad in res.items() if bad is None]
        summary.append(f"{name}: associative shifts {good}")
    return {"rows": rows, "knuth_large_failure": knuth_bad, "summary": summary}
