"""EXP-C12-03: subtraction games with sparse infinite move sets - growth and P-position density."""

from math import isqrt

from systems.relational_games import grundy_subtraction, primes_upto

META = {
    "id": "EXP-C12-03",
    "cycle": "C12",
    "title": "Sparse subtraction sets: Grundy growth and the density of P-positions",
    "agent": "Mathematical Inventor",
    "question": "Do subtraction games whose move sets are sparse (squares, triangular numbers, Fibonacci numbers, "
                "primes) keep a positive proportion of losing positions?",
    "hypothesis": "H-C12-2 (bold): for every such game the P-positions have positive density.",
    "assumptions": ["n <= 2e5", "densities measured at N/16, N/8, N/4, N/2, N"],
    "methodology": "Exact Grundy values (bitset method); P-position density and maximal Grundy value by scale; "
                   "implementation check that no two P-positions differ by an element of the move set.",
    "falsification": "A game whose P-density provably tends to 0 (e.g. by a difference-set theorem) refutes H-C12-2.",
}

N = 200_000


def run():
    fib = [1, 2]
    while fib[-1] <= N:
        fib.append(fib[-1] + fib[-2])
    sets = {
        "squares": [k * k for k in range(1, isqrt(N) + 1)],
        "triangular": [k * (k + 1) // 2 for k in range(1, 700) if k * (k + 1) // 2 <= N],
        "Fibonacci": fib,
        "primes": primes_upto(N),
    }
    rows = {}
    for name, S in sets.items():
        g = grundy_subtraction(N, S)
        scales = [N // 16, N // 8, N // 4, N // 2, N]
        dens = {str(c): round(sum(1 for n in range(c + 1) if g[n] == 0) / (c + 1), 6) for c in scales}
        mx = {str(c): max(g[: c + 1]) for c in scales}
        P = [n for n in range(N + 1) if g[n] == 0]
        Sset = set(S)
        # implementation check on the first 3000 P-positions
        clash = next(((a, b) for i, b in enumerate(P[:3000]) for a in P[:i] if (b - a) in Sset), None)
        rows[name] = {"P_density_by_scale": dens, "max_grundy_by_scale": mx, "P_difference_clash": clash,
                      "first_P": P[:25]}
    return {"N": N, "rows": rows,
            "summary": [f"{k}: P-density {v['P_density_by_scale']}, max g {v['max_grundy_by_scale']}, clash "
                        f"{v['P_difference_clash']}" for k, v in rows.items()]}
