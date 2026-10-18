"""EXP-C09-01: irreducible elements of Knuth's circle semigroup."""

from lab import oeis
from systems.circle_arith import circ, products_upto, shadow

META = {
    "id": "EXP-C09-01",
    "cycle": "C09",
    "title": "Irreducibles ('circle primes') of (N>=1, o) up to 10^6",
    "agent": "Mathematical Explorer",
    "question": "Which positive integers are not circle products a o b, and how dense are they?",
    "hypothesis": "H-C09-1 (inventor): since a o b ~ sqrt(5) a b grows like ordinary multiplication, circle "
                  "irreducibles should thin out like primes (density -> 0).",
    "assumptions": ["Knuth's product (s = 2); exact formula a o b = ab + a b* + a* b validated in EXP-C08/C09 setup"],
    "methodology": "Enumerate all a <= b with a o b <= N (N = 10^6); record counts of irreducibles in dyadic ranges, "
                   "the density trend, the first irreducibles and multiply-represented products; OEIS checks.",
    "falsification": "Irreducible density not decreasing towards 0 across scales 10^2..10^6.",
}

N = 10**6


def run():
    reps = products_upto(N)
    irr = [n for n in range(1, N + 1) if n not in reps]
    checkpoints = [10**k for k in range(2, 7)]
    density = {str(c): round(sum(1 for n in irr if n <= c) / c, 6) for c in checkpoints}
    multi = sorted((n, r) for n, r in reps.items() if len(r) > 1)[:15]
    o_irr = oeis.novelty_check(irr[:40])
    red = sorted(reps)[:40]
    o_red = oeis.novelty_check(red)
    return {
        "N": N,
        "n_irreducible": len(irr),
        "n_reducible": len(reps),
        "density_of_irreducibles": density,
        "first_irreducibles": irr[:60],
        "first_reducibles": red,
        "first_multiply_represented": [[n, r] for n, r in multi],
        "max_representations": max(len(r) for r in reps.values()),
        "oeis_irreducibles": {"status": o_irr["status"], "hits": o_irr.get("hits", [])[:3]},
        "oeis_reducibles": {"status": o_red["status"], "hits": o_red.get("hits", [])[:3]},
        "summary": [
            f"up to {N}: {len(irr)} irreducible, {len(reps)} reducible; density of irreducibles at 10^2..10^6: {density}",
            f"first irreducibles {irr[:20]}",
            f"OEIS irreducibles: {o_irr['status']} {[h['anumber'] for h in o_irr.get('hits', [])[:3]]}; "
            f"reducibles: {o_red['status']} {[h['anumber'] for h in o_red.get('hits', [])[:3]]}",
        ],
    }
