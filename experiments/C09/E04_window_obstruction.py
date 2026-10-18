"""EXP-C09-04: the conjugate-window obstruction to circle factorisation (falsification test)."""

import math

from systems.circle_arith import factorizations, products_upto, shadow

META = {
    "id": "EXP-C09-04",
    "cycle": "C09",
    "title": "Window obstruction: irreducibility forced by the conjugate coordinate",
    "agent": "Formal Verifier",
    "question": "Do the window bounds of C08 force irreducibility and bound factorisation lengths?",
    "hypothesis": "T-C09-A: if f = frac((n+1)/phi) lies outside (psi^2... precisely outside (1/phi - psi^2, "
                  "1/phi - psi^3) = (0.2361, 0.8541), then n is circle-irreducible; such n have density 1/phi^2. "
                  "T-C09-B: every factorisation of n into r irreducibles satisfies |nu'(n)| < |psi|^r, where "
                  "nu'(n) = n*psi + n*.",
    "assumptions": ["n <= 10^6 for T-C09-A; factorisations for n <= 2e5 for T-C09-B",
                    "zone membership decided exactly by integer sign tests in Z[sqrt5] (revised after the Skeptic's "
                    "review - the first version used floating point, which put the boundary point n = 1 inside the "
                    "open zone); the length bound of T-C09-B is still evaluated in floating point",
                    "factorisation sets computed exactly (the first version truncated them at 64 per n)"],
    "methodology": "Scan n <= 10^6: compute f exactly via integer square roots; check every n with f outside the "
                   "product zone is irreducible; measure densities by scale; within the product zone measure the "
                   "irreducible fraction. For T-C09-B compare max factorisation length with log|nu'|/log|psi|.",
    "falsification": "A reducible n with f outside (0.2361, 0.8541); a factorisation longer than the bound.",
}

PHI = (1 + 5 ** 0.5) / 2
PSI = (1 - 5 ** 0.5) / 2
N = 10**6


def nu_conj(n):
    return n * PSI + shadow(n)


def sign_minus_sqrt5(a: int, b: int) -> int:
    """Exact sign of a - b*sqrt(5) for integers a, b."""
    if a >= 0 and b <= 0:
        return 0 if a == 0 and b == 0 else 1
    if a <= 0 and b >= 0:
        return -1
    d = a * a - 5 * b * b
    return (d > 0) - (d < 0) if a > 0 else (d < 0) - (d > 0)


def in_product_zone(n: int) -> bool:
    """psi^3 < nu'(n) < psi^2, decided exactly: nu'(n) = (n + 2n*)/2 - (n/2) sqrt5, psi^2 = (3 - sqrt5)/2,
    psi^3 = 2 - sqrt5. (The first version compared floats and put the boundary point n = 1 inside.)"""
    m = n + 2 * shadow(n)
    return sign_minus_sqrt5(m - 4, n - 2) > 0 and sign_minus_sqrt5(m - 3, n - 1) < 0


def run():
    reps = products_upto(N)
    violations, forced, zone, zone_irr = [], 0, 0, 0
    scale = {}
    for n in range(1, N + 1):
        in_zone = in_product_zone(n)
        if not in_zone:
            forced += 1
            if n in reps:
                violations.append(n)
        else:
            zone += 1
            zone_irr += n not in reps
        if n in (10**3, 10**4, 10**5, 10**6):
            scale[str(n)] = {"forced_irreducible_density": round(forced / n, 6),
                             "irreducible_fraction_in_product_zone": round(zone_irr / max(zone, 1), 6)}
    M = 200_000
    fact = factorizations(M, {k: v for k, v in reps.items() if k <= M})
    length_viol = []
    for n in range(1, M + 1):
        r = max(len(f) for f in fact[n])
        if not abs(nu_conj(n)) < abs(PSI) ** r:
            length_viol.append((n, r, nu_conj(n)))
    return {
        "violations_T_C09_A": violations[:10],
        "n_violations_T_C09_A": len(violations),
        "forced_irreducible_density_limit": round(PSI ** 2, 6),
        "by_scale": scale,
        "violations_T_C09_B": length_viol[:10],
        "summary": [
            f"T-C09-A: {len(violations)} reducible numbers outside the product zone (n <= 1e6); forced-irreducible "
            f"density at 1e6 = {scale['1000000']['forced_irreducible_density']} (limit 1/phi^2 = {PSI**2:.6f})",
            f"irreducible fraction inside the product zone by scale: "
            f"{ {k: v['irreducible_fraction_in_product_zone'] for k, v in scale.items()} }",
            f"T-C09-B (length bound |nu'| < |psi|^r): {len(length_viol)} violations for n <= {M}",
        ],
    }
