"""EXP-C12-02: verification of closed forms and structure theorems for relational games."""

import json
import random

import numpy as np

from lab.paths import RESULTS
from systems.relational_games import (big_omega_table, grundy_options, grundy_split, grundy_subtraction,
                                      prime_index_of_spf_table, smallest_prime_factor, v2)

META = {
    "id": "EXP-C12-02",
    "cycle": "C12",
    "title": "Closed forms for relational games: verification against exact Grundy values",
    "agent": "Formal Verifier",
    "question": "Do the conjectured closed forms hold on the whole computed range, and do the general structure "
                "theorems (power-of-k reduction, splitting parity) hold on new instances?",
    "hypothesis": "G01 = v2(n); G02 = v2(n)+1; G03 P-positions = odd numbers and 2^(2j+1); G04 = Omega(n); "
                  "G05 = index of the smallest prime factor (and 'subtract k coprime to n' is the same game); "
                  "G06: g(2k) = k-1, g(odd m) <= (m-1)/2, P-positions = {1} and the primes; subtract-a-power-of-k "
                  "= the subtraction game {1, k}; any splitting game in which every heap >= 2 has an allowed split "
                  "has g(n) = [n even]; G13 = popcount; G19 = floor(log2((n+1)/3)) + 1 (n >= 2); "
                  "G20 = floor(log2 n).",
    "assumptions": ["exact Grundy values from EXP-C12-01 (n <= 1e5 / 5e3 / 2e4)", "power-of-k games recomputed for "
                    "k = 2..20, n <= 2e4", "40 random splitting relations (each n >= 2 keeps the split 1 + (n-1) "
                    "plus random others), n <= 1500; seed 12"],
    "methodology": "Compare each closed form term by term with the exact values; count mismatches.",
    "falsification": "Any mismatch.",
    "seed": 12,
}


def popcount(n):
    return bin(n).count("1")


def run():
    seqs = json.load(open(RESULTS / "artifacts" / "EXP-C12-01" / "grundy_sequences.json"))
    res = {}

    def check(name, pred, start=1):
        g = seqs[name]
        bad = [n for n in range(start, len(g)) if g[n] != pred(n)]
        res[name] = {"range": [start, len(g) - 1], "mismatches": len(bad), "first_mismatch": bad[:3]}

    check("G01 subtract a divisor d<n", v2)
    check("G02 subtract any divisor", lambda n: v2(n) + 1)
    om = big_omega_table(100_000)
    check("G04 move to a proper divisor", lambda n: om[n])
    pidx = prime_index_of_spf_table(5_000)
    check("G05 move to a smaller coprime", lambda n: pidx[n])
    check("G13 move to a proper binary submask", popcount)
    check("G16 split into coprime parts", lambda n: 1 - n % 2)
    check("G17 split into dividing parts", lambda n: 1 - n % 2)
    check("G19 move to a remainder", lambda n: 0 if n < 2 else ((n + 1) // 3).bit_length())
    check("G20 move to a quotient", lambda n: n.bit_length() - 1)
    # G03: P-positions
    g3 = seqs["G03 subtract a nontrivial proper divisor"]
    P3 = {n for n in range(1, len(g3)) if g3[n] == 0}
    pred3 = {n for n in range(1, len(g3)) if n % 2 == 1 or (n & (n - 1) == 0 and (n.bit_length() - 1) % 2 == 1)}
    res["G03 P-positions = odd numbers and 2^(2j+1)"] = {"range": [1, len(g3) - 1],
                                                         "mismatches": len(P3 ^ pred3)}
    # G06
    g6 = seqs["G06 move to a smaller non-coprime"]
    spf = smallest_prime_factor(len(g6))
    even_bad = [n for n in range(2, len(g6), 2) if g6[n] != n // 2 - 1]
    odd_bad = [m for m in range(1, len(g6), 2) if g6[m] > (m - 1) // 2]
    P6 = {n for n in range(1, len(g6)) if g6[n] == 0}
    pred6 = {1} | {n for n in range(2, len(g6)) if spf[n] == n}
    res["G06 g(2k)=k-1, g(odd m)<=(m-1)/2, P = {1} and primes"] = {
        "even_mismatches": len(even_bad), "odd_bound_violations": len(odd_bad), "P_mismatches": len(P6 ^ pred6),
        "max_ratio_odd": max(g6[m] / m for m in range(3, len(g6), 2))}
    # G05 equals 'subtract k coprime to n' (1 <= k < n): recompute the latter directly on n <= 1500
    from math import gcd
    g7 = grundy_options(1500, lambda n: [n - k for k in range(1, n) if gcd(k, n) == 1])
    res["G07 subtract a coprime = G05"] = {"mismatches": sum(1 for n in range(1501) if g7[n] != seqs[
        "G05 move to a smaller coprime"][n])}
    # powers of k versus the finite game {1, k}
    pk = {}
    for k in range(2, 21):
        N = 20_000
        powers = [1]
        while powers[-1] * k <= N:
            powers.append(powers[-1] * k)
        a = grundy_subtraction(N, powers)
        b = grundy_subtraction(N, [1, k])
        if k % 2 == 0:
            pat = [2 if r == k else r % 2 for r in range(k + 1)]
            pred = [pat[n % (k + 1)] for n in range(N + 1)]
        else:
            pred = [n % 2 for n in range(N + 1)]
        pk[str(k)] = {"equal_to_{1,k}_game": a == b, "matches_pattern": a == pred}
    res["subtract a power of k vs {1,k}"] = pk
    # random splitting relations in which every n >= 2 can be split
    rng = random.Random(META["seed"])
    split_bad = 0
    for trial in range(40):
        salt = rng.randrange(1 << 30)
        thr = rng.random()

        def allowed(a, b, salt=salt, thr=thr):
            h = (a * 1000003 + b * 9176 + salt) % 1000
            return (a == 1) | (h < thr * 1000)
        g = grundy_split(1500, allowed)
        split_bad += sum(1 for n in range(1, 1501) if g[n] != 1 - n % 2)
    res["random splitting relations (every n>=2 splittable)"] = {"relations": 40, "mismatches": split_bad}
    total_bad = sum(v.get("mismatches", 0) for v in res.values() if isinstance(v, dict) and "mismatches" in v)
    total_bad += res["G06 g(2k)=k-1, g(odd m)<=(m-1)/2, P = {1} and primes"]["even_mismatches"]
    total_bad += res["G06 g(2k)=k-1, g(odd m)<=(m-1)/2, P = {1} and primes"]["odd_bound_violations"]
    total_bad += res["G06 g(2k)=k-1, g(odd m)<=(m-1)/2, P = {1} and primes"]["P_mismatches"]
    pk_bad = sum(1 for v in pk.values() if not (v["equal_to_{1,k}_game"] and v["matches_pattern"]))
    return {"checks": res, "total_mismatches": total_bad, "power_of_k_failures": pk_bad,
            "summary": [f"closed-form mismatches over all checks: {total_bad}; power-of-k failures (k=2..20): {pk_bad}"] +
                       [f"{k}: {v}" for k, v in res.items() if k != "subtract a power of k vs {1,k}"]}
