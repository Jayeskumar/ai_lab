"""EXP-C12-05: does the Grundy value of a divisibility-type game depend only on the prime signature?"""

import json

from lab.paths import RESULTS
from systems.relational_games import smallest_prime_factor

META = {
    "id": "EXP-C12-05",
    "cycle": "C12",
    "title": "Prime-signature hypothesis for divisibility and coprimality games",
    "agent": "Mathematical Inventor",
    "question": "Games G01-G06 are defined by multiplicative relations; is their Grundy value a function of the "
                "prime signature (sorted exponent vector) alone?",
    "hypothesis": "H-C12-1 (bold): for each of G01-G06, g(n) depends only on the prime signature of n.",
    "assumptions": ["n <= 5000"],
    "methodology": "Group n by prime signature and look for two numbers with equal signature and different "
                   "Grundy values.",
    "falsification": "Two numbers with the same signature and different Grundy values.",
}


def signature(n, spf):
    exps = []
    while n > 1:
        p, e = spf[n], 0
        while n % p == 0:
            n //= p
            e += 1
        exps.append(e)
    return tuple(sorted(exps, reverse=True))


def run():
    seqs = json.load(open(RESULTS / "artifacts" / "EXP-C12-01" / "grundy_sequences.json"))
    spf = smallest_prime_factor(5000)
    out = {}
    for name in [k for k in seqs if k[:3] in ("G01", "G02", "G03", "G04", "G05", "G06")]:
        g = seqs[name]
        first = {}
        cex = None
        for n in range(1, 5001):
            sig = signature(n, spf)
            if sig in first and g[first[sig]] != g[n]:
                cex = {"n1": first[sig], "n2": n, "signature": list(sig), "g1": g[first[sig]], "g2": g[n]}
                break
            first.setdefault(sig, n)
        out[name] = {"signature_dependent_up_to_5000": cex is None, "counterexample": cex}
    return {"rows": out,
            "summary": [f"{k}: signature-only = {v['signature_dependent_up_to_5000']} {v['counterexample'] or ''}"
                        for k, v in out.items()]}
