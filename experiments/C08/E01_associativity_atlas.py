"""EXP-C08-01: associativity atlas of circle products on recurrence numeration systems."""

from systems.circle import BaseSequence, two_term

META = {
    "id": "EXP-C08-01",
    "cycle": "C08",
    "title": "Associativity atlas of circle products a o b = sum d_i(a) d_j(b) G_(i+j+s)",
    "agent": "Mathematical Explorer",
    "question": "For which base sequences G and index shifts s is the digit-convolution ('circle') product "
                "associative?",
    "hypothesis": "H-C08-1 (inventor's guess): Knuth's Fibonacci product is an isolated miracle - for other "
                  "recurrences or shifts associativity fails.",
    "assumptions": ["greedy expansions", "two-term recurrences G_(k+1) = p G_k + q G_(k-1), p,q in 1..3, several "
                    "initial values G_1; three-term recurrences; geometric sequences as control", "shifts s = 0..5",
                    "all triples a, b, c in [1, 22]"],
    "methodology": "Exhaustive check of (a o b) o c = a o (b o c) on the cube [1,22]^3 for every (G, s); record the "
                   "first failure (lexicographic) and the failure rate.",
    "falsification": "Associative cases other than Knuth's (G = Fibonacci, s = 2) refute H-C08-1.",
}

N = 22


def families():
    seqs = []
    for p in (1, 2, 3):
        for q in (1, 2, 3):
            for g1 in sorted({p + 1, 2, 3, 4, 5}):
                if g1 >= 2:
                    seqs.append(two_term(p, q, g1))
    seqs.append(BaseSequence("tribonacci 1,2,4", [1, 2, 4], (1, 1, 1)))
    seqs.append(BaseSequence("G(k+1)=G(k)+G(k-2); 1,2,3", [1, 2, 3], (1, 0, 1)))
    seqs.append(BaseSequence("G(k+1)=2G(k)+G(k-1)+G(k-2); 1,3,8", [1, 3, 8], (2, 1, 1)))
    seqs.append(BaseSequence("G(k+1)=G(k)+G(k-1)+G(k-2)+G(k-3); 1,2,4,8", [1, 2, 4, 8], (1, 1, 1, 1)))
    seqs.append(BaseSequence("powers of 2", [1], (2,)))
    seqs.append(BaseSequence("powers of 3", [1], (3,)))
    return seqs


def run():
    rows = []
    for G in families():
        for s in range(0, 6):
            first, fails, total = None, 0, 0
            for a in range(1, N + 1):
                for b in range(1, N + 1):
                    ab = G.circle(a, b, s)
                    for c in range(1, N + 1):
                        total += 1
                        if G.circle(ab, c, s) != G.circle(a, G.circle(b, c, s), s):
                            fails += 1
                            if first is None:
                                first = (a, b, c)
            rows.append({"G": G.name, "G_head": G.G[:8], "s": s, "associative_on_cube": fails == 0,
                         "fail_rate": round(fails / total, 5), "first_failure": first})
    assoc = [(r["G"], r["s"]) for r in rows if r["associative_on_cube"]]
    return {
        "N": N,
        "rows": rows,
        "associative_cases": assoc,
        "summary": [f"{len(rows)} (G, s) pairs tested on [1,{N}]^3; associative: {len(assoc)}"] +
                   [f"  {g} | s={s}" for g, s in assoc],
    }
