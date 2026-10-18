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
                    "floating-point evaluation of nu'(n) = n psi + n*: safe because the only exact boundary hits "
                    "are n = 1 (nu' = psi^2) and n = 2 (nu' = psi^3), both irreducible, and otherwise "
                    "|nu'(n) - boundary| = |(n-1) psi - p| >= 0.4/n >> 1e-10 for n <= 1e6 (psi badly approximable)"],
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


def run():
    reps = products_upto(N)
    lo, hi = PSI ** 3, PSI ** 2          # product zone for nu'
    violations, forced, zone, zone_irr = [], 0, 0, 0
    scale = {}
    for n in range(1, N + 1):
        c = nu_conj(n)
        in_zone = lo < c < hi
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
