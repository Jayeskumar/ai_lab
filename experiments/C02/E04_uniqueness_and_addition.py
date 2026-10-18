"""EXP-C02-04: are integer-valued stable configurations unique?  Addition by merge-and-stabilise."""

import itertools
import random

import numpy as np
import sympy as sp

from systems.exchange import positive_root, stabilize_carry, trim

META = {
    "id": "EXP-C02-04",
    "cycle": "C02",
    "title": "Uniqueness of stable representations in emergent bases; addition by merging",
    "agent": "Mathematical Explorer",
    "question": "In a terminating carry system, can an integer have a stable representation other than the "
                "normal form of its unary numeral? Does merging two normal forms and stabilising add them?",
    "hypothesis": "H-C02-4: for every terminating carry rule (sum b < m), distinct stable configurations of "
                  "length <= L have distinct values, so each integer has exactly one stable representation. "
                  "H-C02-5: stab(rep(a) + rep(b)) = rep(a + b).",
    "assumptions": ["the 31 terminating rules of EXP-C02-03", "exact arithmetic in Q(r) modulo the minimal "
                    "polynomial of r", "all stable configurations with at most L levels (m^L <= 2e5)"],
    "methodology": "Enumerate every stable configuration up to L levels, reduce sum c_k x^k modulo the minimal "
                   "polynomial of r, keep those whose value is an integer, group by value. Addition: 2000 "
                   "random pairs per rule.",
    "falsification": "Two stable configurations with the same integer value; a merged sum that stabilises to "
                     "something other than rep(a+b).",
    "seed": 11,
}

TERMINATING = [(m, b) for m in (2, 3, 4) for J in (1, 2, 3) for b in itertools.product(range(4), repeat=J)
               if b[-1] != 0 and sum(b) < m]

x = sp.Symbol("x")


def min_poly(m, b):
    P = sp.Poly(sum(bj * x ** j for j, bj in enumerate(b, start=1)) - m, x)
    r = positive_root(m, b)
    for fac, _ in sp.factor_list(P)[1]:
        if abs(complex(fac.as_expr().subs(x, sp.Float(str(r), 40)))) < 1e-25:
            return sp.Poly(fac, x)
    raise RuntimeError("no factor vanishes at r")


def run():
    rng = random.Random(META["seed"])
    rows, h4_bad, h5_bad = [], [], []
    for m, b in TERMINATING:
        g = min_poly(m, b)
        deg = g.degree()
        L = 1
        while m ** (L + 1) <= 200_000:
            L += 1
        # reduce monomials x^k modulo g once, as integer vectors scaled by a common denominator D
        red = [sp.Poly(x ** k, x).rem(g) for k in range(L)]
        coeffs = [([sp.Rational(c) for c in reversed(rk.all_coeffs())] + [sp.Integer(0)] * deg)[:deg] for rk in red]
        D = 1
        for row in coeffs:
            for c in row:
                D = sp.ilcm(D, c.q)
        D = int(D)
        M = np.array([[int(c * D) for c in row] for row in coeffs], dtype=np.int64)   # L x deg
        assert int(np.abs(M).max()) * (m - 1) * L < 2 ** 62
        digits = np.array(list(itertools.product(range(m), repeat=L)), dtype=np.int64)  # m^L x L
        vals = digits @ M                                                              # exact in int64
        ok = (vals[:, 0] % D == 0) & digits.any(axis=1)
        if deg > 1:
            ok &= np.all(vals[:, 1:] == 0, axis=1)
        by_value = {}
        for i in np.nonzero(ok)[0]:
            by_value.setdefault(int(vals[i, 0]) // D, []).append(trim(tuple(int(t) for t in digits[i])))
        multi = {v: cs for v, cs in by_value.items() if len(cs) > 1}
        mismatched = [v for v, cs in by_value.items() if len(cs) == 1 and
                      stabilize_carry((v,), m, b)[0] != cs[0]]
        row = {"m": m, "b": list(b), "minpoly_degree": deg, "L": L, "integer_valued_configs":
               sum(len(c) for c in by_value.values()), "values_with_multiple_configs": len(multi),
               "examples": {str(v): [list(c) for c in cs] for v, cs in list(multi.items())[:3]},
               "single_config_not_normal_form": mismatched[:5]}
        rows.append(row)
        if multi or mismatched:
            h4_bad.append({"m": m, "b": list(b), "n_values": len(multi), "examples": row["examples"]})
        for _ in range(2000):
            a, c = rng.randint(0, 5000), rng.randint(0, 5000)
            ra = stabilize_carry((a,), m, b)[0]
            rc = stabilize_carry((c,), m, b)[0]
            n = max(len(ra), len(rc))
            merged = tuple((ra[i] if i < len(ra) else 0) + (rc[i] if i < len(rc) else 0) for i in range(n))
            if stabilize_carry(merged, m, b)[0] != stabilize_carry((a + c,), m, b)[0]:
                h5_bad.append({"m": m, "b": list(b), "a": a, "c": c})
                break
    return {
        "rules": rows,
        "h4_counterexample_rules": h4_bad,
        "h5_failures": h5_bad,
        "summary": [
            f"{len(rows)} terminating rules; rules where some integer has two stable configurations (length <= L): "
            f"{len(h4_bad)}",
            f"merge-and-stabilise addition failures over 2000 random pairs per rule: {len(h5_bad)}",
        ],
    }
