"""EXP-C09-02: factorisation into circle irreducibles - uniqueness, lengths, elasticity."""

from systems.circle_arith import factorizations, products_upto

META = {
    "id": "EXP-C09-02",
    "cycle": "C09",
    "title": "Factorisations in Knuth's circle semigroup: uniqueness and lengths",
    "agent": "Mathematical Explorer",
    "question": "Is factorisation into circle irreducibles unique? Do all factorisations of n have the same length?",
    "hypothesis": "H-C09-2 (bold): factorisation into circle irreducibles is unique (the semigroup embeds into the "
                  "UFD Z[phi]).",
    "assumptions": ["all n <= 200000", "factorisation sets truncated at 64 per n (never reached for the reported "
                    "minima)"],
    "methodology": "Dynamic programming over all representations n = a o b with irreducible-multiset "
                   "concatenation; report the smallest n with two factorisations, with two different lengths, "
                   "and the maximum elasticity (max length / min length).",
    "falsification": "Any n with two distinct multisets of irreducibles.",
}

N = 200_000


def run():
    reps = products_upto(N)
    fact = factorizations(N, reps)
    non_unique = [n for n in range(1, N + 1) if len(fact[n]) > 1]
    diff_len = [n for n in non_unique if len({len(f) for f in fact[n]}) > 1]
    elast = max(((max(len(f) for f in fact[n]) / min(len(f) for f in fact[n])), n) for n in range(1, N + 1))
    first = non_unique[0] if non_unique else None
    max_len = max(max(len(f) for f in fs) for fs in fact.values())
    return {
        "N": N,
        "n_with_multiple_factorizations": len(non_unique),
        "first_non_unique": first,
        "first_non_unique_factorizations": sorted(map(list, fact[first])) if first else None,
        "first_different_lengths": diff_len[0] if diff_len else None,
        "first_different_lengths_factorizations": sorted(map(list, fact[diff_len[0]])) if diff_len else None,
        "n_with_different_lengths": len(diff_len),
        "max_elasticity": [elast[0], elast[1]],
        "max_factorization_length": max_len,
        "truncation_hits": sum(len(f) >= 64 for f in fact.values()),
        "summary": [
            f"n <= {N}: {len(non_unique)} with >= 2 factorisations; first: {first} = "
            f"{sorted(map(list, fact[first])) if first else None}",
            f"first with factorisations of different lengths: {diff_len[0] if diff_len else None}; "
            f"count {len(diff_len)}; max elasticity {elast[0]} at n = {elast[1]}",
        ],
    }
