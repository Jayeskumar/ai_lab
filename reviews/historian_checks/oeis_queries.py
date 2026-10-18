"""Historian check: OEIS look-ups (via lab.oeis, cached in cache/oeis)."""
import sys, json
sys.path.insert(0, '.')
from lab import oeis
sys.path.insert(0, 'reviews/historian_checks')
import seqs

queries = {
    "D(aab->ba) n>=1": [seqs.D_aab_ba(n) for n in range(1, 41)],
    "kappa(n) n>=1": [seqs.kappa(n) for n in range(1, 41)],
    "0.06 Grundy": seqs.octal_grundy([0, 6], 60)[:40],
    "0.6 Officers": seqs.octal_grundy([6], 60)[:40],
    "0.007 Treblecross": seqs.octal_grundy([0, 0, 7], 60)[:40],
    "0.07 Dawson Kayles": seqs.octal_grundy([0, 7], 60)[:40],
    "0.4": seqs.octal_grundy([4], 60)[:40],
}
N = 300
prods = set()
for a in range(1, N + 1):
    for b in range(a, N + 1):
        c = seqs.circ(a, b)
        if c <= N:
            prods.add(c)
queries["circle irreducibles"] = [n for n in range(1, N + 1) if n not in prods][:40]
queries["circle reducibles"] = sorted(prods)[:40]
queries["Zeckendorf step cost n>=0"] = [seqs.zeck_cost(n) for n in range(0, 40)]
for name, terms in queries.items():
    r = oeis.novelty_check(terms)
    print(name, "|", r.get("status"), "|", r.get("query"))
    for h in r.get("hits", [])[:6]:
        print("     ", h["anumber"], h["name"][:110])
