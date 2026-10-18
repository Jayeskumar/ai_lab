"""Skeptic checks for cycle C12 (relational one-heap games), independent of systems/ and lab/.

Usage: python3 c12_checks.py <part>      parts: step3 | step2 | divisor | coprime | misc | split
Each part writes out/c12_<part>.json.
"""
import json
import math
import random
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)


def mex(s):
    v = 0
    while v in s:
        v += 1
    return v


def v2(n):
    return (n & -n).bit_length() - 1


# ---------------------------------------------------------------- G03 closed form (from the claim text)
def F(n):
    if n == 0 or n % 2:
        return 0
    a = v2(n)
    m = n >> a
    if m >= 17:
        return a
    if m == 1:
        return 2 if a == 4 else (0 if a % 2 else a - 1)
    if m == 3:
        return [None, 2, 3, 4, 3, 6][a] if a <= 5 else a - 2
    if m == 5:
        return [None, 1, 3, 4, 3, 6][a] if a <= 5 else a + 2
    if m in (7, 9, 11, 15):
        return a if a <= 2 else a + 1
    if m == 13:
        return a if a <= 3 else a + 1
    raise AssertionError


def divisors_from_factorisation(fac):
    ds = [1]
    for p, e in fac.items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds


def factor_small(m):
    fac, p = {}, 2
    while p * p <= m:
        while m % p == 0:
            fac[p] = fac.get(p, 0) + 1
            m //= p
        p += 1
    if m > 1:
        fac[m] = fac.get(m, 0) + 1
    return fac


def g03_option_values(a, m_fac):
    """F-values of all G03 options of n = 2^a m (m odd, given by its factorisation)."""
    m = 1
    for p, e in m_fac.items():
        m *= p ** e
    n = (1 << a) * m
    vals = []
    for e in divisors_from_factorisation(m_fac):
        for i in range(a + 1):
            d = (1 << i) * e
            if 1 < d < n:
                vals.append(F(n - d))
    return vals


def part_step3():
    """Theorem 8, step 3: mex equation for F at n = 2^a m, m <= 15, and shift invariance of the offsets."""
    res = {"mex_failures": [], "offset_sets": {}, "offset_invariance_failures": []}
    AMAX = 400
    for m in range(1, 16, 2):
        fac = factor_small(m) if m > 1 else {}
        ref = {}
        for a in range(6, AMAX + 1):
            vals = set(g03_option_values(a, fac))
            mx = mex(vals)
            if mx != F((1 << a) * m):
                res["mex_failures"].append([m, a, mx, F((1 << a) * m)])
            if a >= 13:
                # offsets of values >= a - 4, presence of 0, and whether 1..a-5 are all present
                key = (tuple(sorted(v - a for v in vals if v >= a - 4)), 0 in vals,
                       all(v in vals for v in range(1, a - 4)))
                par = a % 2
                if par not in ref:
                    ref[par] = key
                    res["offset_sets"][f"m={m},parity={par}"] = {"offsets_ge_-4": list(key[0]), "zero": key[1],
                                                                 "all_1_to_a-5_present": key[2],
                                                                 "mex_minus_a": mx - a}
                elif ref[par] != key:
                    res["offset_invariance_failures"].append([m, a])
    res["range"] = f"m odd <= 15, a = 6..{AMAX} (mex), a = 13..{AMAX} (offsets)"
    return res


def part_step2():
    """Theorem 8, step 2 (odd part >= 17): random large n with known factorisation, and every odd part
    17 <= m <= 3001 for a = 1..60."""
    rng = random.Random(20261018)
    small_primes = [p for p in range(3, 200) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    fails, tested = [], 0
    for _ in range(3000):
        fac = {}
        for _ in range(rng.randint(1, 4)):
            p = rng.choice(small_primes)
            fac[p] = fac.get(p, 0) + 1
        m = 1
        for p, e in fac.items():
            m *= p ** e
        if m < 17:
            continue
        a = rng.randint(1, 200)
        tested += 1
        vals = set(g03_option_values(a, fac))
        if mex(vals) != a or F((1 << a) * m) != a:
            fails.append([m, a])
    exhaustive_fail = []
    for m in range(17, 3002, 2):
        fac = factor_small(m)
        for a in range(1, 61):
            if mex(set(g03_option_values(a, fac))) != a:
                exhaustive_fail.append([m, a])
    return {"random_tested": tested, "random_failures": fails,
            "exhaustive_m_17_to_3001_a_1_to_60_failures": exhaustive_fail}


# ---------------------------------------------------------------- divisibility games (CLM-C12-01)
def part_divisor(N=300000):
    t0 = time.time()
    divs = [[] for _ in range(N + 1)]
    for d in range(1, N + 1):
        for k in range(d, N + 1, d):
            divs[k].append(d)
    g01 = [0] * (N + 1)
    g02 = [0] * (N + 1)
    g04 = [0] * (N + 1)
    for n in range(1, N + 1):
        g01[n] = mex({g01[n - d] for d in divs[n] if d < n})
        g02[n] = mex({g02[n - d] for d in divs[n]})
        g04[n] = mex({g04[d] for d in divs[n] if d < n})
    # Omega by trial division using a spf sieve
    spf = list(range(N + 1))
    for p in range(2, int(N ** 0.5) + 1):
        if spf[p] == p:
            for k in range(p * p, N + 1, p):
                if spf[k] == k:
                    spf[k] = p
    Om = [0] * (N + 1)
    for n in range(2, N + 1):
        Om[n] = Om[n // spf[n]] + 1
    bad = {"G01": [n for n in range(1, N + 1) if g01[n] != v2(n)][:10],
           "G02": [n for n in range(1, N + 1) if g02[n] != v2(n) + 1][:10],
           "G04": [n for n in range(1, N + 1) if g04[n] != Om[n]][:10]}
    # H-C12-1 counterexamples quoted in CLM-C12-10
    quoted = {"G01(2),G01(3)": [g01[2], g01[3]], "G02(2),G02(3)": [g02[2], g02[3]]}
    return {"N": N, "mismatches_first10": bad, "quoted_values": quoted, "seconds": round(time.time() - t0, 1)}


# ---------------------------------------------------------------- coprimality games (CLM-C12-02)
def part_coprime(N=6000):
    t0 = time.time()
    g05 = [0] * (N + 1)
    g06 = [0] * (N + 1)
    g07 = [0] * (N + 1)
    for n in range(1, N + 1):
        co = [m for m in range(1, n) if math.gcd(m, n) == 1]
        g05[n] = mex({g05[m] for m in co})
        g07[n] = mex({g07[n - k] for k in co})
        g06[n] = mex({g06[m] for m in range(1, n) if math.gcd(m, n) > 1})
    primes = [p for p in range(2, N + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    idx = {p: i + 1 for i, p in enumerate(primes)}

    def spf(n):
        for p in primes:
            if n % p == 0:
                return p

    bad05 = [n for n in range(2, N + 1) if g05[n] != idx[spf(n)]][:10]
    bad07 = [n for n in range(1, N + 1) if g07[n] != g05[n]][:10]
    bad06_even = [n for n in range(2, N + 1, 2) if g06[n] != n // 2 - 1][:10]
    bad06_odd = [n for n in range(1, N + 1, 2) if 2 * g06[n] > n - 1][:10]
    P06 = [n for n in range(1, N + 1) if g06[n] == 0]
    bad06_P = sorted(set(P06) ^ ({1} | set(primes)))[:10]
    ratio = max(g06[m] / m for m in range(3, N + 1, 2))
    # Iannucci-Larsson: SG(n) = floor((n+1)/4) for n = 3 mod 6 (their SG = our g + 1 for n >= 2)
    il = [n for n in range(3, N + 1, 6) if g06[n] + 1 != (n + 1) // 4][:10]
    return {"N": N, "G05_vs_prime_index_bad": bad05, "G07_vs_G05_bad": bad07, "G06_even_bad": bad06_even,
            "G06_odd_bound_bad": bad06_odd, "G06_P_symmetric_difference": bad06_P,
            "G06_max_ratio_odd": ratio, "G06_IL_n_3_mod_6_check_bad": il,
            "seconds": round(time.time() - t0, 1)}


# ---------------------------------------------------------------- bitwise / quotient / powers of k (CLM-C12-05/06)
def part_misc():
    t0 = time.time()
    out = {}
    # G13 proper submasks, n < 2^14
    M = 1 << 14
    g13 = [0] * M
    for n in range(1, M):
        vals = set()
        s = (n - 1) & n
        while True:
            vals.add(g13[s])
            if s == 0:
                break
            s = (s - 1) & n
        g13[n] = mex(vals)
    out["G13_popcount_bad"] = [n for n in range(M) if g13[n] != bin(n).count("1")][:10]
    # G19 n -> n mod k (1 <= k < n), n <= 6000
    N = 6000
    g19 = [0] * (N + 1)
    for n in range(2, N + 1):
        g19[n] = mex({g19[n % k] for k in range(1, n)})

    def f19(n):
        if n < 2:
            return 0
        v = 0
        while 3 * 2 ** v - 1 <= n:   # g(n) = max{v : 3*2^(v-1) - 1 <= n}
            v += 1
        return v

    out["G19_formula_bad"] = [n for n in range(N + 1) if g19[n] != (math.floor(math.log2((n + 1) / 3)) + 1 if n >= 2 else 0)][:10]
    out["G19_formula_vs_threshold_form_bad"] = [n for n in range(N + 1) if g19[n] != f19(n)][:10]
    # G20 n -> floor(n/k), 2 <= k <= n, n <= 40000
    N2 = 40000
    g20 = [0] * (N2 + 1)
    for n in range(2, N2 + 1):
        vals, k = set(), 2
        while k <= n:
            q = n // k
            vals.add(g20[q])
            k = n // q + 1
        g20[n] = mex(vals)
    out["G20_bad"] = [n for n in range(1, N2 + 1) if g20[n] != n.bit_length() - 1][:10]
    # powers of k versus {1, k}
    bad_pk = []
    for k in range(2, 31):
        Nk = 20000
        S = []
        p = 1
        while p <= Nk:
            S.append(p)
            p *= k
        g = [0] * (Nk + 1)
        h = [0] * (Nk + 1)
        for n in range(1, Nk + 1):
            g[n] = mex({g[n - s] for s in S if s <= n})
            h[n] = mex({h[n - s] for s in (1, k) if s <= n})
        for n in range(Nk + 1):
            if k % 2:
                f = n % 2
            else:
                r = n % (k + 1)
                f = 2 if r == k else r % 2
            if g[n] != h[n] or g[n] != f:
                bad_pk.append([k, n])
                break
    out["powers_of_k_bad"] = bad_pk
    out["seconds"] = round(time.time() - t0, 1)
    return out


# ---------------------------------------------------------------- splitting games (CLM-C12-07)
def part_split():
    rng = random.Random(7)
    bad = []
    rels = []
    for trial in range(60):
        N = 200
        allowed = {}
        for n in range(2, N + 1):
            pairs = [(a, n - a) for a in range(1, n // 2 + 1)]
            keep = [pq for pq in pairs if rng.random() < 0.3]
            if not keep:
                keep = [rng.choice(pairs)]
            allowed[n] = keep
        g = [0] * (N + 1)
        for n in range(2, N + 1):
            g[n] = mex({g[a] ^ g[b] for a, b in allowed[n]})
        for n in range(1, N + 1):
            if g[n] != (1 if n % 2 == 0 else 0):
                bad.append([trial, n])
                break
    # G16 coprime parts, G17 a | b, Grundy's game (a != b) for comparison
    N = 1500
    out = {}
    for name, ok in (("G16", lambda a, b: math.gcd(a, b) == 1), ("G17", lambda a, b: b % a == 0),
                     ("G18_grundys_game", lambda a, b: a != b)):
        g = [0] * (N + 1)
        for n in range(2, N + 1):
            g[n] = mex({g[a] ^ g[n - a] for a in range(1, n // 2 + 1) if ok(a, n - a)})
        out[name + "_parity_bad"] = [n for n in range(1, N + 1) if g[n] != (1 - n % 2)][:5]
    return {"random_relations": 60, "random_relation_failures": bad, **out}


PARTS = {"step3": part_step3, "step2": part_step2, "divisor": part_divisor, "coprime": part_coprime,
         "misc": part_misc, "split": part_split}

if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = PARTS[part]()
    res["wall_seconds"] = round(time.time() - t0, 1)
    (OUT / f"c12_{part}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res)[:3000])
