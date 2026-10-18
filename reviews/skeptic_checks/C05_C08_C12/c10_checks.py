"""Skeptic checks for cycle C10 (cost of counting), independent of systems/counting_cost.py.

Usage: python3 c10_checks.py <part>   parts: classical | zeckendorf | exchange
Writes out/c10_<part>.json.
"""
import itertools
import json
import math
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"


def hamming(a, b):
    L = max(len(a), len(b))
    a = list(a) + [0] * (L - len(a))
    b = list(b) + [0] * (L - len(b))
    return sum(x != y for x, y in zip(a, b))


def base(n, b):
    d = []
    while n:
        n, r = divmod(n, b)
        d.append(r)
    return d


def negabin(n):
    d = []
    while n:
        r = n % 2          # n = q*(-2) + r with r in {0,1}
        d.append(r)
        n = (n - r) // -2
    return d


def balanced3(n):
    d = []
    while n:
        r = ((n + 1) % 3) - 1     # in {-1,0,1}
        d.append(r)
        n = (n - r) // 3
    return d


def factorial_digits(n):
    d, k = [], 2
    while n:
        n, r = divmod(n, k)
        d.append(r)
        k += 1
    return d


def gray(n):
    g = n ^ (n >> 1)
    return [(g >> i) & 1 for i in range(g.bit_length())]


FIBW = [1, 2]
while FIBW[-1] < 10 ** 12:
    FIBW.append(FIBW[-1] + FIBW[-2])


def zeck(n):
    d = [0] * len(FIBW)
    for k in range(len(FIBW) - 1, -1, -1):
        if FIBW[k] <= n:
            d[k] = 1
            n -= FIBW[k]
    while d and d[-1] == 0:
        d.pop()
    return d


def skew_increment(d):
    """canonical skew binary increment on a digit list (weights 2^(k+1)-1); returns new list."""
    d = list(d)
    nz = [i for i, x in enumerate(d) if x]
    if nz and d[nz[0]] == 2:
        i = nz[0]
        d[i] = 0
        if i + 1 == len(d):
            d.append(0)
        d[i + 1] += 1
    else:
        if not d:
            d = [0]
        d[0] += 1
    while d and d[-1] == 0:
        d.pop()
    return d


def part_classical(N=10 ** 6):
    systems = {"binary": lambda n: base(n, 2), "ternary": lambda n: base(n, 3), "decimal": lambda n: base(n, 10),
               "negabinary": negabin, "balanced_ternary": balanced3, "factorial": factorial_digits, "gray": gray,
               "zeckendorf": zeck}
    pred = {"binary": 2, "ternary": 1.5, "decimal": 10 / 9, "negabinary": 2, "balanced_ternary": 1.5,
            "factorial": math.e - 1, "gray": 1, "zeckendorf": 2}
    res = {}
    for name, f in systems.items():
        prev = f(0)
        tot = worst = 0
        for n in range(1, N + 1):
            cur = f(n)
            c = hamming(prev, cur)
            tot += c
            worst = max(worst, c)
            prev = cur
        # sanity: representations are correct
        res[name] = {"average_n_lt_N": tot / N, "predicted": pred[name], "worst": worst}
    # value checks of the digit functions
    assert all(sum(d * (-2) ** i for i, d in enumerate(negabin(n))) == n for n in range(2000))
    assert all(sum(d * 3 ** i for i, d in enumerate(balanced3(n))) == n for n in range(2000))
    assert all(sum(d * math.factorial(i + 1) for i, d in enumerate(factorial_digits(n))) == n for n in range(2000))
    # skew binary: own increment, check canonical value and worst case / average
    d, tot, worst, with2 = [], 0, 0, 0
    W = [2 ** (k + 1) - 1 for k in range(64)]
    for n in range(N):
        e = skew_increment(d)
        c = hamming(d, e)
        tot += c
        worst = max(worst, c)
        d = e
        assert sum(x * W[i] for i, x in enumerate(d)) == n + 1
    res["skew_binary"] = {"average_n_lt_N": tot / N, "worst": worst}
    # exact average over complete blocks [0, 2^(k+1) - 1): cost = 1 + [rep(n) contains a 2]
    block = {}
    for k in (10, 16, 20):
        M = 2 ** (k + 1) - 1
        block[k] = (2 * M - 2 ** k) / M if False else None
    res["skew_binary_count_argument"] = "numbers 0..2^(k+1)-2 with k-digit reps: 2^k without a digit 2, 2^k - 1 with one"
    return res


def part_zeckendorf():
    res = {}
    G = [1, 2]
    while len(G) < 32:
        G.append(G[-1] + G[-2])
    # brute-force T_m for m <= 30 (G_30 ~ 2.2e6)
    T = []
    prev = zeck(0)
    tot = 0
    m = 0
    T.append(0)
    for n in range(1, G[30]):
        cur = zeck(n)
        tot += hamming(prev, cur)
        prev = cur
        while m + 1 <= 30 and n == G[m + 1] - 1:
            m += 1
            T.append(tot)
    res["T_m_bruteforce_m_le_30"] = T
    res["closed_form_ok"] = all(T[mm] == 2 * G[mm] - math.ceil(mm / 2) - 2 for mm in range(len(T)))
    res["recurrence_ok"] = all(T[mm + 1] == T[mm] + T[mm - 1] + math.ceil(mm / 2) + 1 for mm in range(1, len(T) - 1))
    # Historian's potential identity: d(n, n+1) = 2 + s(n) - s(n+1), s = number of ones
    bad = 0
    prev = zeck(0)
    for n in range(0, 10 ** 6):
        cur = zeck(n + 1)
        if hamming(prev, cur) != 2 + sum(prev) - sum(cur):
            bad += 1
        prev = cur
    res["potential_identity_violations_n_lt_1e6"] = bad
    return res


def stabilise(config, m, b):
    """full stabilisation (own): repeatedly fire any unstable level"""
    c = list(config)
    fired = 0
    changed = True
    while changed:
        changed = False
        for k in range(len(c)):
            if c[k] >= m:
                t = c[k] // m
                c[k] -= t * m
                fired += t
                for j, bj in enumerate(b, start=1):
                    if bj:
                        while len(c) <= k + j:
                            c.append(0)
                        c[k + j] += t * bj
                changed = True
    while c and c[-1] == 0:
        c.pop()
    return c, fired


def part_exchange(N=400_000):
    rules = [(m, b) for m in (2, 3, 4) for J in (1, 2, 3) for b in itertools.product(range(4), repeat=J)
             if b[-1] != 0 and sum(b) < m]
    res = {"n_rules": len(rules), "rows": []}
    for m, b in rules:
        B = sum(b)
        single = sum(1 for x in b if x) == 1
        c = [0] * 400
        tot_ch = tot_f = 0
        worst = 0
        single_viol = 0
        checkpoints = {}
        for n in range(1, N + 1):
            before = {0: c[0]}
            c[0] += 1
            f = 0
            stack = [0]
            while stack:
                k = stack.pop()
                while c[k] >= m:
                    c[k] -= m
                    f += 1
                    for j, bj in enumerate(b, start=1):
                        if bj:
                            if k + j not in before:
                                before[k + j] = c[k + j]
                            c[k + j] += bj
                            if c[k + j] >= m:
                                stack.append(k + j)
            ch = sum(1 for i, v in before.items() if c[i] != v)
            tot_ch += ch
            tot_f += f
            worst = max(worst, ch)
            if single and ch != f + 1:
                single_viol += 1
            if n in (N // 4, N // 2):
                checkpoints[n] = round(tot_ch / n - (1 + 1 / (m - B)), 5)
            if n <= 3000 and n % 97 == 0:
                full, _ = stabilise([n], m, b)
                cc = list(c)
                while cc and cc[-1] == 0:
                    cc.pop()
                assert full == cc, (m, b, n)
        row = {"m": m, "b": list(b), "single_offset": single, "avg_firings": tot_f / N,
               "pred_firings": 1 / (m - B), "avg_changes": tot_ch / N, "excess_over_1+1/(m-B)":
               tot_ch / N - (1 + 1 / (m - B)), "excess_at_N/4,N/2": checkpoints, "worst": worst,
               "single_offset_steps_with_cost_ne_firings+1": single_viol if single else None}
        res["rows"].append(row)
    res["max_firing_dev"] = max(abs(r["avg_firings"] - r["pred_firings"]) for r in res["rows"])
    res["single_offset_max_abs_excess"] = max(abs(r["excess_over_1+1/(m-B)"]) for r in res["rows"] if r["single_offset"])
    res["single_offset_total_violations"] = sum(r["single_offset_steps_with_cost_ne_firings+1"] for r in res["rows"] if r["single_offset"])
    res["multi_offset_min_excess"] = min(r["excess_over_1+1/(m-B)"] for r in res["rows"] if not r["single_offset"])
    return res


PARTS = {"classical": part_classical, "zeckendorf": part_zeckendorf, "exchange": part_exchange}

if __name__ == "__main__":
    part = sys.argv[1]
    t0 = time.time()
    res = PARTS[part]()
    res = {"part": part, "result": res, "wall_seconds": round(time.time() - t0, 1)}
    (OUT / f"c10_{part}.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, default=str)[:3000])
