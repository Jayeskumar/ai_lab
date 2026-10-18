"""EXP-C09-03: the norm homomorphism of the circle semigroup into (Z, x)."""

from sympy import factorint, isprime

from systems.circle_arith import circ, products_upto, shadow

META = {
    "id": "EXP-C09-03",
    "cycle": "C09",
    "title": "Norm map N(n) = n*^2 + n n* - n^2 and circle irreducibility",
    "agent": "Mathematical Inventor",
    "question": "Can ordinary multiplication detect circle factorisations through the norm of nu(n) in Z[phi]?",
    "hypothesis": "H-C09-3: N(a o b) = N(a) N(b) for all a, b (proved from the embedding); |N(n)| <= sqrt(5) n; and "
                  "every n whose |N(n)| is 1 or a rational prime is circle-irreducible except n = 1's multiples "
                  "by units.",
    "assumptions": ["n <= 10^5 for statistics; multiplicativity checked on all a, b <= 400"],
    "methodology": "Compute N(n) = s^2 + n s - n^2 with s = n*; verify multiplicativity; bound |N(n)|/n; compare "
                   "irreducibility with the primality of |N(n)|.",
    "falsification": "A failure of multiplicativity, or a reducible n with prime |N(n)|.",
}


def norm(n):
    s = shadow(n)
    return s * s + n * s - n * n


def run():
    mult_fail = [(a, b) for a in range(1, 401) for b in range(1, 401) if norm(circ(a, b)) != norm(a) * norm(b)]
    M = 10**5
    reps = products_upto(M)
    ratio = max(abs(norm(n)) / n for n in range(1, M + 1))
    prime_norm_reducible = [n for n in range(2, M + 1) if n in reps and isprime(abs(norm(n)))][:10]
    unit_norm = [n for n in range(1, M + 1) if abs(norm(n)) == 1][:20]
    irr = [n for n in range(1, M + 1) if n not in reps]
    irr_prime_norm = sum(1 for n in irr if isprime(abs(norm(n))))
    zero_norm = [n for n in range(1, M + 1) if norm(n) == 0]
    return {
        "multiplicativity_failures": mult_fail[:5],
        "n_multiplicativity_failures": len(mult_fail),
        "max_abs_norm_over_n": round(ratio, 6),
        "first_norms": [norm(n) for n in range(1, 31)],
        "unit_norm_elements": unit_norm,
        "zero_norm_elements": zero_norm[:5],
        "reducible_with_prime_norm": prime_norm_reducible,
        "irreducibles_with_prime_norm": irr_prime_norm,
        "n_irreducibles": len(irr),
        "summary": [
            f"multiplicativity N(a o b) = N(a)N(b) on a, b <= 400: {len(mult_fail)} failures",
            f"max |N(n)|/n for n <= 1e5: {round(ratio, 4)} (sqrt 5 = 2.2361); elements of norm +-1: {unit_norm[:8]}",
            f"reducible n with prime |N(n)|: {prime_norm_reducible[:5]}; irreducibles with prime |N(n)|: "
            f"{irr_prime_norm}/{len(irr)}",
        ],
    }
