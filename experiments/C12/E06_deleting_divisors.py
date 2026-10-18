"""EXP-C12-06: the full Grundy function of G03 ("subtract a divisor d with 1 < d < n", Codeforces 'Deleting Divisors')."""

import random

from systems.relational_games import divisor_lists, grundy_options, mex, v2

META = {
    "id": "EXP-C12-06",
    "cycle": "C12",
    "title": "Grundy values of the deleting-divisors game G03: v2(n) except for odd parts <= 15",
    "agent": "Mathematical Explorer",
    "question": "The P-positions of G03 are known (CLM-C12-03), but its Grundy sequence matches nothing in the OEIS "
                "(EXP-C12-04). What is the Grundy function?",
    "hypothesis": "H-C12-3: g(n) = v2(n) whenever the odd part m of n is at least 17; for m <= 15, g(2^a m) = a + c_m "
                  "for all a >= a_m with (m: a_m, c_m) = (3: 6, -2), (5: 6, +2), (7, 9, 11, 15: 3, +1), (13: 4, +1); "
                  "g(2^a) = 0 for odd a and a - 1 for even a (except g(16) = 2); ten sporadic values in between.",
    "assumptions": ["exact Grundy values recomputed for n <= 1e5",
                    "closed form F from the table in proofs/paper/C12.md Theorem 8",
                    "inductive-step certificate: odd parts m <= 15, exponents 13 <= a <= 100",
                    "random spot checks of the mex equation for F: 3000 even n = 2^a m (17 <= m < 1e6, a <= 40) "
                    "and 1000 odd n < 1e8; seed 1206"],
    "methodology": "Compare g with F on [0, 1e5]; check F(n) = mex{F(n - d)} on the certificate range and on random "
                   "large n by enumerating divisors exactly.",
    "falsification": "Any n with g(n) != F(n), or any n where F violates the mex equation.",
    "seed": 1206,
}

N = 100_000

# (odd part m, exponent a) -> value, for the few positions before the eventual rule takes over
SPORADIC = {(1, 4): 2, (3, 1): 2, (3, 2): 3, (3, 3): 4, (3, 4): 3, (3, 5): 6,
            (5, 2): 3, (5, 3): 4, (5, 4): 3, (5, 5): 6}
# odd part m -> (a_m, c_m): g(2^a m) = a + c_m for a >= a_m
EVENTUAL = {3: (6, -2), 5: (6, 2), 7: (3, 1), 9: (3, 1), 11: (3, 1), 13: (4, 1), 15: (3, 1)}


def F(n):
    """Conjectured closed form of the Grundy function of G03."""
    if n == 0 or n % 2:
        return 0
    a = v2(n)
    m = n >> a
    if (m, a) in SPORADIC:
        return SPORADIC[(m, a)]
    if m == 1:
        return 0 if a % 2 else a - 1
    if m in EVENTUAL and a >= EVENTUAL[m][0]:
        return a + EVENTUAL[m][1]
    return a


def odd_divisors(m):
    """Divisors of an odd number m by trial factorisation."""
    divs = [1]
    p = 3
    while p * p <= m:
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            divs = [d * p ** k for d in divs for k in range(e + 1)]
        p += 2
    if m > 1:
        divs = [d * q for d in divs for q in (1, m)]
    return divs


def mex_of_options(a, m, divs_m):
    """mex of F over the G03 options of n = 2^a m (m odd, divs_m its divisors)."""
    n = (1 << a) * m
    vals = set()
    for i in range(a + 1):
        for e in divs_m:
            d = (1 << i) * e
            if 1 < d < n:
                vals.add(F(n - d))
    return mex(vals), vals


def run():
    divs = divisor_lists(N)
    g = grundy_options(N, lambda n: [n - d for d in divs[n] if 1 < d < n])
    mism = [n for n in range(N + 1) if g[n] != F(n)]
    exceptions = {}
    for n in range(2, N + 1, 2):
        if g[n] != v2(n):
            m = n >> v2(n)
            exceptions[str(m)] = exceptions.get(str(m), 0) + 1
    dev = max(abs(g[n] - v2(n)) for n in range(1, N + 1) if not ((n & (n - 1)) == 0 and v2(n) % 2 == 1))
    records, best = [], -1
    for n in range(N + 1):
        if g[n] > best:
            best = g[n]
            records.append([n, g[n]])

    # inductive-step certificate for odd parts m <= 15 (Theorem 8, step 3)
    cert_bad, offsets = [], {}
    for m in range(1, 16, 2):
        dm = odd_divisors(m)
        for a in range(13, 101):
            val, vals = mex_of_options(a, m, dm)
            if val != F((1 << a) * m):
                cert_bad.append([m, a, val, F((1 << a) * m)])
            if a in (13, 14):
                offsets[f"m={m},a={a}"] = {"mex_minus_a": val - a,
                                           "offsets>=-4": sorted(v - a for v in vals if v >= a - 4),
                                           "zero_present": 0 in vals}

    # random spot checks of the mex equation for F beyond the computed range
    rng = random.Random(META["seed"])
    even_bad = 0
    for _ in range(3000):
        m = rng.randrange(17, 10 ** 6) | 1
        a = rng.randrange(1, 41)
        if mex_of_options(a, m, odd_divisors(m))[0] != F((1 << a) * m):
            even_bad += 1
    odd_bad = 0
    for _ in range(1000):
        n = rng.randrange(3, 10 ** 8) | 1
        if any(F(n - e) == 0 for e in odd_divisors(n) if 1 < e < n):
            odd_bad += 1

    summary = [
        f"g = F on [0, {N}]: mismatches {len(mism)}; positions with g != v2: {sum(exceptions.values())} "
        f"(by odd part {exceptions})",
        f"max |g - v2| off the P-positions 2^(2j+1): {dev}; records (n, g): {records}",
        f"certificate m <= 15, 13 <= a <= 100: mismatches {len(cert_bad)}",
        f"random mex checks: even n {even_bad}/3000 failures, odd n {odd_bad}/1000 failures",
    ]
    return {"N": N, "mismatches": mism[:20], "exceptions_by_odd_part": exceptions, "max_dev_off_P": dev,
            "records": records, "certificate_failures": cert_bad, "offsets_a13_a14": offsets,
            "random_even_failures": even_bad, "random_odd_failures": odd_bad, "summary": summary}
