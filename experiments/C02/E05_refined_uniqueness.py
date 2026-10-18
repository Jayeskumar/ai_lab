"""EXP-C02-05: refined uniqueness theorem for emergent bases (after the refutation in EXP-C02-04)."""

import itertools
from math import gcd

import numpy as np
import sympy as sp

from systems.exchange import stabilize_carry, trim

from experiments.C02.E04_uniqueness_and_addition import TERMINATING, min_poly, x

META = {
    "id": "EXP-C02-05",
    "cycle": "C02",
    "title": "Refined uniqueness: primitive irreducible carry polynomials on the reachable sublattice",
    "agent": "Mathematical Skeptic",
    "question": "Exactly which terminating carry rules have unique stable representations?",
    "hypothesis": "H-C02-4': let g = gcd{j : b_j > 0} and P~(y) = sum_i b_(gi) y^i - m. If P~ is primitive and "
                  "irreducible over Q, distinct stable configurations supported on multiples of g have distinct "
                  "values; if P~ is not primitive, two such configurations with equal value exist.",
    "assumptions": ["the 31 terminating rules", "all stable configurations supported on gZ with at most L "
                    "supported levels (m^L <= 2e5)"],
    "methodology": "Exact integer evaluation modulo the minimal polynomial (as in EXP-C02-04) restricted to "
                   "levels 0, g, 2g, ...; compare collisions with the primitive/irreducible prediction.",
    "falsification": "A collision for a primitive irreducible P~, or no collision for a non-primitive P~.",
}

y = sp.Symbol("y")


def run():
    rows, bad = [], []
    for m, b in TERMINATING:
        J = len(b)
        g = 0
        for j, bj in enumerate(b, start=1):
            if bj:
                g = gcd(g, j)
        Pt = sp.Poly(sum(b[g * i - 1] * y ** i for i in range(1, J // g + 1)) - m, y)
        content = int(gcd(m, *[b[g * i - 1] for i in range(1, J // g + 1)]))
        primitive = content == 1
        irreducible = len(sp.factor_list(Pt)[1]) == 1 and sp.factor_list(Pt)[1][0][1] == 1
        gpoly = min_poly(m, b)
        deg = gpoly.degree()
        L = 1
        while m ** (L + 1) <= 200_000:
            L += 1
        levels = [g * i for i in range(L)]
        red = [sp.Poly(x ** k, x).rem(gpoly) for k in levels]
        coeffs = [([sp.Rational(c) for c in reversed(rk.all_coeffs())] + [sp.Integer(0)] * deg)[:deg] for rk in red]
        D = 1
        for row in coeffs:
            for c in row:
                D = sp.ilcm(D, c.q)
        D = int(D)
        M = np.array([[int(c * D) for c in row] for row in coeffs], dtype=np.int64)
        assert int(np.abs(M).max()) * (m - 1) * L < 2 ** 62
        digits = np.array(list(itertools.product(range(m), repeat=L)), dtype=np.int64)
        vals = digits @ M
        # collisions among ALL stable configurations (any value), via exact value vectors
        keys = {}
        collisions = 0
        example = None
        for i in range(len(digits)):
            key = tuple(int(t) for t in vals[i])
            if key in keys:
                collisions += 1
                if example is None:
                    example = [[int(t) for t in digits[keys[key]]], [int(t) for t in digits[i]]]
            else:
                keys[key] = i
        predicted_unique = primitive and irreducible
        row = {"m": m, "b": list(b), "g": g, "P_tilde": str(Pt.as_expr()), "content": content,
               "primitive": primitive, "irreducible": irreducible, "L": L, "collisions": collisions,
               "example_collision_digits_on_gZ": example}
        # check the normal forms of 1..300 are supported on gZ
        off = [n for n in range(1, 301) if any(c and k % g for k, c in enumerate(stabilize_carry((n,), m, b)[0]))]
        row["normal_forms_off_lattice"] = off[:5]
        rows.append(row)
        if predicted_unique and collisions:
            bad.append({"rule": [m, list(b)], "why": "collision despite primitive irreducible", "ex": example})
        if not primitive and not collisions:
            bad.append({"rule": [m, list(b)], "why": "non-primitive but no collision found"})
        if off:
            bad.append({"rule": [m, list(b)], "why": "normal form off the lattice"})
    reducible_primitive = [r for r in rows if r["primitive"] and not r["irreducible"]]
    return {
        "rows": rows,
        "violations": bad,
        "primitive_irreducible": sum(r["primitive"] and r["irreducible"] for r in rows),
        "non_primitive": sum(not r["primitive"] for r in rows),
        "primitive_reducible": [(r["m"], r["b"], r["collisions"]) for r in reducible_primitive],
        "summary": [
            f"{len(rows)} terminating rules: {sum(r['primitive'] and r['irreducible'] for r in rows)} with primitive "
            f"irreducible P~ (all collision-free: {all(r['collisions'] == 0 for r in rows if r['primitive'] and r['irreducible'])}), "
            f"{sum(not r['primitive'] for r in rows)} non-primitive (all with collisions: "
            f"{all(r['collisions'] > 0 for r in rows if not r['primitive'])}), "
            f"{len(reducible_primitive)} primitive but reducible",
            f"violations of H-C02-4': {len(bad)}",
        ],
    }
